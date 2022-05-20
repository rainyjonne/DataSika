# http request function
from datetime import datetime
from concurrent.futures import as_completed
from requests import Session 
from requests_futures.sessions import FuturesSession
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd
import numpy as np
import json
import ast
from IPython import embed


# set retries for avoiding request limits
def session_configure(retries, concurrent):
    # force retry when bumping into this code
    status_forcelist = [429]
    if concurrent:
        session = FuturesSession()
    else:
        session = Session() 
        
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        respect_retry_after_header=True,
        status_forcelist=status_forcelist,
    )

    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    return session


# input: dataframe -> output: dataframe
def http_request(db, stage_name, task_id, url_df, extract_field = 0, preserve_origin_data = False, concurrent = False):


    # extract_field default is 0
    rows = url_df[extract_field]

    response_list = []
        
    headers = None
    date_time_list = []
    status_code_list = []
    if "headers" in url_df.columns:
        # presume every row has same headers setting
        headers= json.loads(url_df['headers'][0])

    # set default retry for 3 times
    session = session_configure(3, concurrent)
    if concurrent:
        results = as_completed([session.get(url, headers=headers) for url in rows])
    else:
        results = rows
   
    resp_list = []
    for result in results:
        #NOTE: strongly suggest using concurrent on calling API contents
        # webscrapping might cause some character encoding problems
        if concurrent:
            future = result
            response = future.result()
            url = response.url
        else:
            url = result
            response = session.get(url, headers=headers) 
        date_time = str(datetime.now())
        
        status_code = response.status_code
        if status_code >= 400:
            level = "ERROR"
            error_message = response.text
        else:
            level = "INFO"
            error_message = ""

        # logging
        db.insert('_request_log', "?, ?, ?, ?, ?, ?, ?, ?", (level, status_code,stage_name, task_id, url, date_time, error_message, ''))

        content_type = response.headers['Content-Type']
        
        # NOTE: if it's webscrapping then return binary content
        if 'application/x-gzip' in content_type or 'text/html' in content_type:
            # return bytes if the file hasn't been decompress yet
            category = "binary"
            response_ret = response.content
        else:
            # otherwise return pure text
            category = "text"
            response_ret = response.text

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

    result_df = http_request(db, stage_name, task_id, request_df, 'base_url', preserve_origin_data, concurrent)

    return result_df


