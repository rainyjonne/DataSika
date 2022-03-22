# http request function
import requests as reqs

def http_request(url):
    response = reqs.get(url)
    
    ##REMINDER:
    # return bytes if the file hasn't been decompress yet
    if '.gz' in url:
        result = response.content
        return result
    
    # otherwise return pure text
    result = response.text
    return result
