# http request function
from datetime import datetime
import asyncio, aiohttp
from aiohttp_retry import RetryClient, ExponentialRetry
import pandas as pd
import numpy as np
import json
import ast
from IPython import embed
import nest_asyncio
nest_asyncio.apply()

def session_configure():
    # set default retry for 3 times
    retry_options = ExponentialRetry(attempts=3)
    retry_session = RetryClient(raise_for_status=False, retry_options=retry_options)
    return retry_session
    
session = session_configure()
async def call_request(url, headers):
    return await session.get(url, headers=headers) 


# input: dataframe -> output: dataframe
async def http_request(db, stage_name, task_id, url_df, extract_field = 0, preserve_origin_data = False, concurrent = False):

    #embed(using='asyncio')
    # for test
    if len(url_df.index) > 1000:
        #url_df = url_df.sample(n=10)
        url_df = url_df[0:10]

    # extract_field default is 0
    rows = url_df[extract_field]

    response_list = []
        
    headers = None
    date_time_list = []
    status_code_list = []
    if "headers" in url_df.columns:
        # presume every row has same headers setting
        headers= json.loads(url_df['headers'][0])

    if concurrent: 
        responses = await asyncio.gather(*[call_request(url, headers) for url in rows])
    else:
        loop = asyncio.get_event_loop()
        responses  = [call_request(url, headers) for url in rows]
   
    resp_list = []
    for response in responses:
        if not concurrent:
            response = loop.run_until_complete(response)  

        url = str(response.url)
        date_time = str(datetime.now())
        
        status_code = response.status
        if status_code >= 400:
            level = "ERROR"
        else:
            level = "INFO"
        error_mesg = f"{status_code}: {response.text()}"


        table_values = f""" 
            '{level}',
            '{stage_name}',
            '{task_id}',
            '{date_time}',
            '{error_mesg}',
            ''
        """
        db.insert('_log', "?, ?, ?, ?, ?, ?",(level, stage_name, task_id, date_time, error_mesg, ''))

        content_type = response.headers['Content-Type']
    
        ##REMINDER:
        if 'application/x-gzip' in content_type:
            # return bytes if the file hasn't been decompress yet
            category = "binary"
            response_ret = await response.read()
        else:
            # otherwise return pure text
            category = "text"
            response_ret = await response.text()

        filtered_resp = (url, response_ret, status_code, date_time)
        resp_list.append(filtered_resp)

    resp_df = pd.DataFrame(resp_list, columns=[extract_field, "response", "status_code", "update_time"])
    # rename dataframe columns
    resp_df.rename(columns={"response": category}, inplace=True)
        
    if preserve_origin_data:
        # join back to the original url df
        final_df = url_df.merge(resp_df, how="inner", on=extract_field) 
    else:
        final_df = url_df.merge(resp_df, how="inner", on=extract_field) 
        final_df = final_df[[category]]

    session.close() 
    return final_df


# input: a param dataframe -> output: prepared url dataframe
def http_request_dynamic(db, stage_name, task_id, params_df, preserve_fields = None, mapping_fields = None, pagination = None, concurrent = False):
    request_df = pd.DataFrame()
    base_url = params_df['base_url'][0]
    # default doesn't preserve origin data
    preserve_origin_data = False
    # add question mark if not provided
    if base_url[-1] != "?":
        params_df['base_url'] = f"{base_url}?"

    columns = list(params_df.columns)
    if "headers" in columns:
        request_df['headers'] = params_df['headers']
        # remove headers & base url column
        columns.remove("headers")
    columns.remove("base_url")

    for column in columns:
        if column == pagination:
            continue
        params_df['base_url'] = params_df['base_url'].map(str) + f"&{column}=" + params_df[column].map(str)


    if preserve_fields:
        request_df = params_df[preserve_fields]
        preserve_origin_data = True

    if mapping_fields:
        request_df = request_df.rename(columns=mapping_fields)

    request_df['base_url'] = params_df['base_url']

    # add pagination logic  
    if pagination:
        [start, end] = ast.literal_eval(params_df[pagination][0])
        pages = list(range(start, end+1))
        # replicate dataframe rows
        temp_df = pd.DataFrame()
        replicated_df = temp_df.append([request_df]*len(pages), ignore_index=True)
        replicated_df[pagination] = pages
        replicated_df['base_url'] = replicated_df['base_url'].map(str) + f"&{pagination}=" + replicated_df[pagination].map(str)
        replicated_df = replicated_df.drop([pagination], axis=1)
        request_df = replicated_df

    # reduce request numbers
    request_df = request_df.drop_duplicates(ignore_index=True)

    result_df = asyncio.run(http_request(db, stage_name, task_id, request_df, 'base_url', preserve_origin_data, concurrent=concurrent))

    return result_df


