import pandas as pd
import ast
from IPython import embed

# input: dataframe -> output: dataframe
def flatten_lists_to_dataframe(df, extract_field = None, preserve_origin_data = False):
    if extract_field:
        column = extract_field
        rows = df[extract_field]
    else:
        column = 0 
        rows = df[0]

    # turn dataframe series into list
    rows = list(rows) 
    # turn list strings into lists
    list_of_lists = [ast.literal_eval(row) for row in rows]
    # turn list of lists into flat list
    flat_list = [item for sublist in list_of_lists for item in sublist]

    # preserve origin data will return flat_list strings for every column
    if preserve_origin_data:
        df[column] = str(flat_list)
        result_df = df
    else:
        # turn into a multiple rows dataframe
        result_df = pd.DataFrame().append(flat_list)

    return result_df
