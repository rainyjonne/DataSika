# input: a dataframe -> output: list of dataframes
from sika.task_bypass.helpers import split_task_length_sanity_check

def split_dataframe_rows(df, task_id):
    split_df_rows = [v.reset_index() for k, v in df.groupby(0)]
    #NOTE: split function has its own sanity check
    split_task_length_sanity_check(df, split_df_rows, task_id)

    return split_df_rows
