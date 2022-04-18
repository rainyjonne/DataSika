# http request function
import requests as reqs
import pandas as pd
import json

# input: dataframe -> output: dataframe
def http_request(url_df, extract_field = None, preserve_origin_data = False):
    
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
        response = reqs.get(url, headers=headers)
            
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
def http_request_dynamic(params_df, preserve_fields = None, mapping_fields = None):
    request_df = pd.DataFrame()
    base_url = params_df['base_url'][0]
    # default doesn't preserve origin data
    preserve_origin_data = False
    # add question mark if not provided
    if base_url[-1] != "?":
        base_url = f"{base_url}?"

    for column in list(params_df.columns):
        if column == "headers" or column == "base_url":
            break
        base_url = f"{base_url}&{column}={params_df[column][0]}"

    if preserve_fields:
        request_df = params_df[preserve_fields]
        preserve_origin_data = True

    if mapping_fields:
        request_df = request_df.rename(columns=mapping_fields)

    request_df['base_url'] = base_url

    if "headers" in list(params_df.columns):
        request_df['headers'] = params_df['headers']

    # reduce request numbers
    request_df = request_df.drop_duplicates(ignore_index=True)

    result_df = http_request(request_df, 'base_url', preserve_origin_data)

    return result_df
