import pandas as pd
from io import StringIO


def transform_to_dataframe(input_string, str_type):
    result = pd.DataFrame()

    if str_type == "csv":
        result = pd.read_csv(StringIO(input_string), sep=",")

    return result
