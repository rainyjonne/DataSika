from pandasql import sqldf

def sql_merge(dataframes, query_syntax):
    for key, value in dataframes.items():
        globals()[key] = value
      
    merged_df = sqldf(query_syntax, globals())
    return merged_df
