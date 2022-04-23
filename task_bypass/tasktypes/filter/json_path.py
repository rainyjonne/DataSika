import jsonpath2 as jp2
from jsonpath2.path import Path
import json
import pandas as pd
from IPython import embed

def json_path(df, syntax, extract_field = None, preserve_origin_data = False):
    if extract_field:
        column_name = extract_field
        rows = df[extract_field]
    else:
        column_name = 0
        rows = df[0]
    
    result_lists = []
    for row in rows:
        json_strs = json.loads(row)
        p = Path.parse_str(syntax)

        # if m.current_value's type is dictionary or list, turn it into json_str
        # else return original value
        ret = [json.dumps(m.current_value) if type(m.current_value) == list or type(m.current_value) == dict else m.current_value for m in p.match(json_strs)]

        # if it returns only one element then extract it
        # e.g. length()
        if len(ret) == 1:
            result_lists.append(ret[0])

        # else then return the text of the whole list 
        # if there are still some circumstances, change afterwards 
        else:
            result_lists.append(str(ret))

    if preserve_origin_data: 
        df[column_name] = result_lists
    else:
        df = pd.DataFrame({column_name: result_lists})

    return df
