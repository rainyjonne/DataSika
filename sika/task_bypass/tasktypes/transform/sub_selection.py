import pandas as pd
from IPython import embed

# input: dataframe -> output: dataframe
def sub_selection(df, start_num, end_num):
    df = df[start_num:(end_num + 1)]
    df = df.reset_index()
    del df['index']

    return df
