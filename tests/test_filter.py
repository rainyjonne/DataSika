from .handler import function_handler
import yaml
import pytest
import pandas as pd
import numpy as np
from packaging import version


def filter_setup(function):

    if function == "json-path":
        # read in file infos
        with open("tests/test_yamls/test_json_path.yml", "r") as stream:
            file_infos = yaml.safe_load(stream)
    
        filter_infos = []
        for file_info in file_infos:
            # get file infos
            input_file = file_info['input_file']
            output_file = file_info['output_file']
            syntax = file_info['syntax']
            extract_field = file_info['extract_field']
            preserve_origin_data = file_info['preserve_origin_data']
    
            # create input & output dfs
            input_df = pd.read_csv(input_file)
            output_df = pd.read_csv(output_file)
            
            filter_infos.append((input_df, output_df, syntax, extract_field, preserve_origin_data))
    
        return filter_infos

    if function == "xpath":
        # read in file infos
        with open("tests/test_yamls/test_xpath.yml", "r") as stream:
            file_infos = yaml.safe_load(stream)
    
        filter_infos = []
        for file_info in file_infos:
            # get file infos
            input_file = file_info['input_file']
            output_file = file_info['output_file']
            syntax = file_info['syntax']
            extract_field = file_info['extract_field']
    
            # create input & output dfs
            input_df = pd.read_csv(input_file)
            output_df = pd.read_csv(output_file)
            
            filter_infos.append((input_df, output_df, syntax, extract_field))
    
        return filter_infos

    if function == "sql":
        # read in file infos
        with open("tests/test_yamls/test_sql.yml", "r") as stream:
            file_infos = yaml.safe_load(stream)
    
        filter_infos = []
        for file_info in file_infos:
            # get file infos
            input_file = file_info['input_file']
            output_file = file_info['output_file']
            syntax = file_info['syntax']
            last_output_name = file_info['last_output_name']
    
            # create input & output dfs
            input_df = pd.read_csv(input_file)
            output_df = pd.read_csv(output_file)
            
            filter_infos.append((input_df, output_df, syntax, last_output_name))
    
        return filter_infos

@pytest.mark.parametrize("input_df, output_df, syntax, extract_field, preserve_origin_data", filter_setup("json-path"))
def test_json_path(input_df, output_df, syntax, extract_field, preserve_origin_data):
    params = (input_df, syntax, extract_field, preserve_origin_data)
    filtered_df = function_handler('json_path', params)

    # sort the values
    output_df.sort_values(by=[output_df.columns[0]], inplace=True, ignore_index=True)
    filtered_df.sort_values(by=[filtered_df.columns[0]], inplace=True, ignore_index=True)

    # compare values
    assert (output_df.values ==  filtered_df.values).all()

    # compare columns
    assert [str(x) for x in list(output_df.columns)] == [str(x) for x in list(filtered_df.columns)]


@pytest.mark.parametrize("input_df, output_df, syntax, extract_field", filter_setup("xpath"))
def test_xpath(input_df, output_df, syntax, extract_field):
    params = (input_df, syntax, extract_field)
    filtered_df = function_handler('xpath', params)

    # sort the values
    output_df.sort_values(by=[output_df.columns[0]], inplace=True, ignore_index=True)
    filtered_df.sort_values(by=[filtered_df.columns[0]], inplace=True, ignore_index=True)

    # compare values
    assert (output_df.values ==  filtered_df.values).all()

    # compare columns
    assert [str(x) for x in list(output_df.columns)] == [str(x) for x in list(filtered_df.columns)]


@pytest.mark.parametrize("input_df, output_df, syntax, last_output_name", filter_setup("sql"))
def test_sql(input_df, output_df, syntax, last_output_name):
    params = (last_output_name, input_df, syntax)
    filtered_df = function_handler('sql', params)

    # sort the values
    output_df.sort_values(by=[output_df.columns[0]], inplace=True, ignore_index=True)
    filtered_df.sort_values(by=[filtered_df.columns[0]], inplace=True, ignore_index=True)

    # round the values to decimal 2
    output_df = output_df.round(2)
    filtered_df = filtered_df.round(2)

    # replace NaN with None
    if version.parse(pd.__version__) >= version.parse('1.3.0'):
        output_df = output_df.replace({np.nan: None})
        filtered_df = filtered_df.replace({np.nan: None})
    else:
        output_df = output_df.where(pd.notnull(output_df), None)
        filtered_df = filtered_df.where(pd.notnull(filtered_df), None)

    # compare values
    assert (output_df.values ==  filtered_df.values).all()

    # compare columns
    assert [str(x) for x in list(output_df.columns)] == [str(x) for x in list(filtered_df.columns)]

