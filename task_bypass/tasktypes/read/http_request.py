# http request function
import requests as reqs
import pandas as pd

# input: string -> output: dataframe
def http_request(url_df):
    url = url_df[0][0]
    response = reqs.get(url)
    content_type = response.headers['Content-Type']
    
    ##REMINDER:
    if 'application/x-gzip' in content_type:
        # return bytes if the file hasn't been decompress yet
        data = {"binary": response.content}
    else:
        # otherwise return pure text
        data = {"text": response.text}
    
    result = pd.DataFrame(data=data, index=[0])
    return result
