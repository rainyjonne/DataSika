import pandas as pd

# input: dataframe -> output: dataframe
def sampling(df, nums, seed = None):
    # takes inplace samplings
    if nums > len(df.index):
        df = df.sample(n=nums, replace=True, random_state=seed)
    else:
        df = df.sample(n=nums, random_state=seed)
        df = df.reset_index()
        del df['index']

    return df

