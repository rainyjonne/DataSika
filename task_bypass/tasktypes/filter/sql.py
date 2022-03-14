from pandasql import sqldf

def sql(_last_output_name, _from_output, value):
    globals()[_last_output_name] = _from_output
    query = value
    
    filtered_df = sqldf(query, globals())
    return filtered_df
