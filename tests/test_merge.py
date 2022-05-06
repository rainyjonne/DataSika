import yaml
import pytest
import pandas as pd
from task_bypass.tasktypes.merge.sql_merge import sql_merge 


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
    merged_df = sql_merge(input_dfs, syntax)

    # replace NaN with None
    output_df = output_df.where(pd.notnull(output_df), None)
    merged_df = merged_df.where(pd.notnull(merged_df), None)

    # compare values
    assert (output_df.values ==  merged_df.values).all()

    # compare columns
    assert [str(x) for x in list(output_df.columns)] == [str(x) for x in list(merged_df.columns)]

