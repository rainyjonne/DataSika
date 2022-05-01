# http request function
from datetime import datetime
import requests as reqs
import pandas as pd
import numpy as np
import json
import ast
from IPython import embed

# input: dataframe -> output: dataframe
def http_request(db, stage_name, task_id, url_df, extract_field = None, preserve_origin_data = False):


    # for test
    if len(url_df.index) > 1000:
        url_df = url_df.sample(n=10)

    if extract_field:
        rows = url_df[extract_field]
    else:
        rows = url_df[0]

    response_list = []
        
    headers = None
    date_time_list = []
    status_code_list = []
    for url in rows:
        if "headers" in url_df.columns:
            # presume every row has same headers setting
            headers= json.loads(url_df['headers'][0])
            # clear caches for test
            headers.update({'Cache-Control': 'no-cache'})
        
        headers = {'Cache-Control': 'no-cache'}
        date_time = str(datetime.now())
        date_time_list.append(date_time)
        response = reqs.get(url, headers=headers)
        
        status_code = response.status_code
        status_code_list.append(status_code)
        if status_code >= 400:
            level = "ERROR"
        else:
            level = "INFO"
        error_mesg = f"{status_code}: {response.text}"


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
            response_list.append(response.content)
        else:
            # otherwise return pure text
            category = "text"
            response_list.append(response.text)

    # adding basic information for calling api
    url_df['update_time'] = date_time_list 
    url_df['status_code'] = status_code_list 
        
    if preserve_origin_data:
        url_df[category] = response_list
    else:
        url_df = pd.DataFrame()
        url_df[category] = response_list

    
    return url_df


# input: a param dataframe -> output: prepared url dataframe
def http_request_dynamic(db, stage_name, task_id, params_df, preserve_fields = None, mapping_fields = None, pagination = None):
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

    result_df = http_request(db, stage_name, task_id, request_df, 'base_url', preserve_origin_data)

    return result_df


