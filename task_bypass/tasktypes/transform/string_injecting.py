import pandas as pd

def string_injecting(df):
    columns = list(df.columns)
    for column in columns:
        if column != 0:
            df[0] = df.apply(lambda x: x[0].replace(f'[{column}]', str(x[column])), axis=1)

    return df

