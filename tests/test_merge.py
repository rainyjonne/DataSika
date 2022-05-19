from .handler import function_handler
import yaml
import pytest
import pandas as pd
import numpy as np
from packaging import version


def merge_setup():
    # read in file infos
    with open("tests/test_yamls/test_sql_merge.yml", "r") as stream:
        file_infos = yaml.safe_load(stream)

    merge_infos = []
    for file_info in file_infos:
        # get file infos
        inputs = file_info['inputs']
        input_dfs = {}
        for _input in inputs:
            key = _input['from']
            value = pd.read_csv(_input['file_path'])
            input_dfs.update({key: value})

        output_file = file_info['output_file']
        syntax = file_info['syntax']
        output_df = pd.read_csv(output_file)

        merge_infos.append((input_dfs, output_df, syntax))
    
    return merge_infos


@pytest.mark.parametrize("input_dfs, output_df, syntax", merge_setup())
def test_sql_merge(input_dfs, output_df, syntax):
    params = (input_dfs, syntax)
    merged_df = function_handler('sql_merge', params)

    # replace NaN with None
    if version.parse(pd.__version__) >= version.parse('1.3.0'):
        output_df = output_df.replace({np.nan: None})
        merged_df = merged_df.replace({np.nan: None})
    else:
        output_df = output_df.where(pd.notnull(output_df), None)
        merged_df = merged_df.where(pd.notnull(filtered_df), None)

    # compare values
    assert (output_df.values ==  merged_df.values).all()

    # compare columns
    assert [str(x) for x in list(output_df.columns)] == [str(x) for x in list(merged_df.columns)]

