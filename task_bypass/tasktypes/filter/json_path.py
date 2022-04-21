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
        result_lists.append(ret[0])
        
    df[column_name] = result_lists

    return df
