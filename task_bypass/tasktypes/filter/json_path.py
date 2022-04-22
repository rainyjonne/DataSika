import jsonpath2 as jp2
from jsonpath2.path import Path
import json

def json_path(df, syntax, extract_field = None):
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
        ret = [m.current_value for m in p.match(json_strs)]
        # if it returns only one element then extract it
        if len(ret) == 1:
            result_lists.append(ret[0])
        # else then return the text of the whole list 
        # if there are still some circumstances, change afterwards 
        else:
            result_lists.append(str(ret))

        
    df[column_name] = result_lists

    return df
