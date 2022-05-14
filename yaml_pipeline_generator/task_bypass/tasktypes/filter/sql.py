from pandasql import sqldf

# input: string & dataframe -> output: dataframe

def sql(_last_output_name, df, syntax):
    globals()[_last_output_name] = df
    filtered_df = sqldf(syntax, globals())
    return filtered_df
