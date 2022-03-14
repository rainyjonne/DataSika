import pandas as pd
from io import StringIO

def transform_to_dataframe(input_string, params):
    result = pd.DataFrame()
    #print(params)
    if params['input_format'] == "str" and params['str_type'] == "csv":
        result = pd.read_csv(StringIO(input_string), sep=",")

    return result
