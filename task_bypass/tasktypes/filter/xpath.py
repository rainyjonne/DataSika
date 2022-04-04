
from lxml import html
import pandas as pd

def xpath(_from_output, value):
    if _from_output.columns[0] == 'binary':
        bytes_str = _form_output['binary']
    # default is pure text   
    elif _from_output.columns[0] == 'text' :
        output_str = _from_output['text'][0]
        bytes_str = output_str.encode('utf-8')
    else:
        output_str = _from_output[0][0]
        bytes_str = output_str.encode('utf-8')
    
    tree = html.fromstring(bytes_str)
    filtered_result = tree.xpath(value)
        
    if filtered_result == []:
         return pd.DataFrame([None])
    
    # try to reduce codes
    # if it returns a html element after filtering than use html.tostring to transfer it to pure text, if it returns something else than use str() to turn it to pure text
    final_result = pd.DataFrame(list(map(lambda ele: html.tostring(ele).decode('utf-8') if type(ele).__name__ == 'HtmlElement' else str(ele), filtered_result)))
    
    return final_result
    
