# http request function
from datetime import datetime
import requests as reqs
import pandas as pd
import numpy as np
import json

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
    for url in rows:
        if "headers" in url_df.columns:
            # presume every row has same headers setting
            headers= json.loads(url_df['headers'][0])
        date_time = str(datetime.now())
        response = reqs.get(url, headers=headers)
       
        if response.status_code >= 400:
            level = "ERROR"
        else:
            level = "INFO"
        error_mesg = f"{response.status_code}: {response.text}"


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
        
    if preserve_origin_data:
        url_df[category] = response_list
    else:
        url_df = pd.DataFrame()
        url_df[category] = response_list
    
    return url_df


# input: a param dataframe -> output: prepared url dataframe
def http_request_dynamic(db, stage_name, task_id, params_df, preserve_fields = None, mapping_fields = None):
    request_df = pd.DataFrame()
    base_url = params_df['base_url'][0]
    # default doesn't preserve origin data
    preserve_origin_data = False
    # add question mark if not provided
    if base_url[-1] != "?":
        params_df['base_url'] = f"{base_url}?"

    columns = list(params_df.columns)
    # remove headers & base url column
    if 'headers' in columns:
        columns.remove("headers")
    columns.remove("base_url")

    for column in columns:
        params_df['base_url'] = params_df['base_url'].map(str) + f"&{column}=" + params_df[column].map(str)

    if preserve_fields:
        request_df = params_df[preserve_fields]
        preserve_origin_data = True

    if mapping_fields:
        request_df = request_df.rename(columns=mapping_fields)

    request_df['base_url'] = params_df['base_url']

    if "headers" in list(params_df.columns):
        request_df['headers'] = params_df['headers']

    # reduce request numbers
    request_df = request_df.drop_duplicates(ignore_index=True)

    result_df = http_request(db, stage_name, task_id, request_df, 'base_url', preserve_origin_data)

    return result_df
