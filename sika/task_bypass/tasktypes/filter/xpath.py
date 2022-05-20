
from lxml import html
import pandas as pd
from IPython import embed

def xpath(df, syntax, extract_field = None):
    
    # using decoding utf-8 to prevent some special character problems on web-scrapping
    if df.columns[0] == 'binary':
        output_str = df['binary'][0].decode('utf-8')
    # default is pure text
    elif df.columns[0] == 'text' :
        output_str = df['text'][0]
    elif extract_field:
        output_str = df[extract_field][0]
    else:
        output_str = _from_output[0][0]


    tree = html.fromstring(output_str)
    filtered_result = tree.xpath(syntax)

    if filtered_result == []:
         return pd.DataFrame([None])

    # try to reduce codes
    # if it returns a html element after filtering than use html.tostring to transfer it to pure text, if it returns something else than use str() to turn it to pure text
    final_result = pd.DataFrame(list(map(lambda ele: html.tostring(ele).decode('utf-8') if type(ele).__name__ == 'HtmlElement' else str(ele), filtered_result)))

    return final_result
