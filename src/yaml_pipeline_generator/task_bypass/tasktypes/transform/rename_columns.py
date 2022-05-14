def rename_columns(df, map_dict):
    df = df.rename(columns=map_dict, errors="raise")
    return df
