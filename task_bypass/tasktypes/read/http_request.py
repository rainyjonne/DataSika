# http request function
import requests as reqs

def http_request(url, output_format):
    response = reqs.get(url)
    if output_format == "binary":
        result = response.content
    else:
        result = response
    return result
