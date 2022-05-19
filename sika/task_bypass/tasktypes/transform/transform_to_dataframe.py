import pandas as pd
import json
import ast
from io import StringIO
from IPython import embed

# input: string -> output: dataframe
def transform_to_dataframe(input_string, str_type, result = None):

    if str_type == "csv":
        result = pd.read_csv(StringIO(input_string), sep=",")

    if str_type == "json":
    	result = pd.DataFrame(json.loads(input_string))

    if str_type == "json_array":
        a_series = pd.Series(ast.literal_eval(input_string), index=result.columns)
        result = result.append(a_series, ignore_index=True)


    return result


def json_array_to_dataframe(rows, headers = None):
    headers = ast.literal_eval(headers)
    result = pd.DataFrame(columns=headers)

    for row in rows:
        result = transform_to_dataframe(row, 'json_array', result)

    return result
