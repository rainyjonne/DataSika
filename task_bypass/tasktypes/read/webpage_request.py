# webpage request function
from lxml import html
import requests as reqs

def webpage_request(url, output_format):
    response = reqs.get(url)
    if output_format == "binary":
        result = html.fromstring(response.content)
    else:
        result = response
    return result
    
