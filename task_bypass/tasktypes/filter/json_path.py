from jsonpath import jsonpath
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
        result = json.dumps(jsonpath(json_strs, syntax)[0])
        result_lists.append(result)
        
    df[column_name] = result_lists

    return df
