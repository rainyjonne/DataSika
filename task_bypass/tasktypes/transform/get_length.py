import json

def get_length(df, str_type, extract_field = None, preserve_origin_data = False):
    if extract_field:
        rows = df[extract_field]
    else:
        rows = df[0]

     
    response_list = []
    for resp in rows:
        if str_type == "json":
            json_str = json.loads(resp)
            length = len(json_str)
            response_list.append(length)
        
    if preserve_origin_data:
        df[extract_field] = response_list
    else:
        df = pd.DataFrame()
        df[extract_field] = response_list
        
    return df
    
        
