import pandas as pd
import json
from io import StringIO


def transform_to_dataframe(input_string, str_type):
    result = pd.DataFrame()

    if str_type == "csv":
        result = pd.read_csv(StringIO(input_string), sep=",")

    if str_type == "json":
    	result = pd.DataFrame(json.loads(input_string))


    return result
