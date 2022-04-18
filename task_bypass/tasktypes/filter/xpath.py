
from lxml import html
import pandas as pd

def xpath(df, syntax, extract_field = None):

    if df.columns[0] == 'binary':
        bytes_str = df['binary']
    # default is pure text
    elif df.columns[0] == 'text' :
        output_str = df['text'][0]
        bytes_str = output_str.encode('utf-8')
    elif extract_field:
        output_str = df[extract_field][0]
        bytes_str = output_str.encode('utf-8')
    else:
        output_str = _from_output[0][0]
        bytes_str = output_str.encode('utf-8')


    tree = html.fromstring(bytes_str)
    filtered_result = tree.xpath(syntax)

    if filtered_result == []:
         return pd.DataFrame([None])

    # try to reduce codes
    # if it returns a html element after filtering than use html.tostring to transfer it to pure text, if it returns something else than use str() to turn it to pure text
    final_result = pd.DataFrame(list(map(lambda ele: html.tostring(ele).decode('utf-8') if type(ele).__name__ == 'HtmlElement' else str(ele), filtered_result)))

    return final_result
