import yaml
import pytest
import pandas as pd
from task_bypass.tasktypes.transform.decompress_content import decompress_content 
from task_bypass.tasktypes.transform.flatten_lists_to_dataframe import flatten_lists_to_dataframe
from task_bypass.tasktypes.transform.split_dataframe_rows import split_dataframe_rows 
from task_bypass.tasktypes.transform.string_injecting import string_injecting 
from task_bypass.tasktypes.transform.rename_columns import rename_columns 
from task_bypass.tasktypes.transform.transform_to_dataframe import transform_to_dataframe, json_array_to_dataframe 


def transform_setup(function):
    # read in file infos
    with open("tests/test_yamls/test_transform.yml", "r") as stream:
        file_infos = yaml.safe_load(stream)

    if function == "decompress-content":
        extract_infos = [file_info for file_info in file_infos if file_info['function'] == "decompress-content"] 
        transform_infos = []
        for info in extract_infos:
            # get file infos
            input_file = info['input_file']
            output_file = info['output_file']
    
            # create input & output dfs
            f = open(input_file, "rb")
            binary_str = f.read()
            input_df = pd.DataFrame({0: [binary_str]})
            output_df = pd.read_csv(output_file)
            
            transform_infos.append((input_df, output_df))
    
        return transform_infos

    if function == "transform-to-dataframe":
        extract_infos = [file_info for file_info in file_infos if file_info['function'] == "transform-to-dataframe"] 
        transform_infos = []
        for info in extract_infos:
            # get file infos
            input_file = info['input_file']
            output_file = info['output_file']
            str_type = info['str_type']
    
            # create input & output dfs
            input_df = pd.read_csv(input_file)
            output_df = pd.read_csv(output_file)
            
            transform_infos.append((input_df, output_df, str_type))
    
        return transform_infos

    if function == "split-dataframe-rows":
        extract_infos = [file_info for file_info in file_infos if file_info['function'] == "split-dataframe-rows"] 
        transform_infos = []
        for info in extract_infos:
            # get file infos
            input_file = info['input_file']
            # create input & output dfs
            input_df = pd.read_csv(input_file, header=None)
            output_dfs = [pd.read_csv(output_df) for output_df in info['output_files']]

            transform_infos.append((input_df, output_dfs))
    
        return transform_infos

    if function == "flatten-lists-to-dataframe":
        extract_infos = [file_info for file_info in file_infos if file_info['function'] == "flatten-lists-to-dataframe"] 
        transform_infos = []
        for info in extract_infos:
            # get file infos
            input_file = info['input_file']
            output_file = info['output_file']
            extract_field = info['extract_field']
            preserve_origin_data = info['preserve_origin_data']

            # create input & output dfs
            input_df = pd.read_csv(input_file)
            output_df = pd.read_csv(output_file)

            transform_infos.append((input_df, output_df, extract_field, preserve_origin_data))

        return transform_infos


    if function == "string-injecting":
        extract_infos = [file_info for file_info in file_infos if file_info['function'] == "string-injecting"] 
        transform_infos = []
        for info in extract_infos:
            # get file infos
            input_file = info['input_file']
            output_file = info['output_file']

            # create input & output dfs
            input_df = pd.read_csv(input_file, names=[0, 'gem_name'])
            output_df = pd.read_csv(output_file)

            transform_infos.append((input_df, output_df))

        return transform_infos

    if function == "rename-columns":
        extract_infos = [file_info for file_info in file_infos if file_info['function'] == "rename-columns"] 
        transform_infos = []
        for info in extract_infos:
            # get file infos
            input_file = info['input_file']
            output_file = info['output_file']
            map_dict = info['rename_map']

            # create input & output dfs
            input_df = pd.read_csv(input_file)
            output_df = pd.read_csv(output_file)

            transform_infos.append((input_df, output_df, map_dict))

        return transform_infos


    if function == "json-array-to-dataframe":
        extract_infos = [file_info for file_info in file_infos if file_info['function'] == "json-array-to-dataframe"] 
        transform_infos = []
        for info in extract_infos:
            # get file infos
            input_file = info['input_file']
            output_file = info['output_file']
            headers = info['headers']
            extract_field = info['extract_field']

            # create input & output dfs
            input_df = pd.read_csv(input_file)
            output_df = pd.read_csv(output_file)

            transform_infos.append((input_df, output_df, extract_field, headers))

        return transform_infos



@pytest.mark.parametrize("input_df, output_df", transform_setup("decompress-content"))
def test_decompress_content(input_df, output_df):
    transformed_df = decompress_content(input_df)

    # compare values
    assert (output_df.values ==  transformed_df.values).all()

    # compare columns
    assert [str(x) for x in list(output_df.columns)] == [str(x) for x in list(transformed_df.columns)]



@pytest.mark.parametrize("input_df, output_df, str_type", transform_setup("transform-to-dataframe"))
def test_transform_to_dataframe(input_df, output_df, str_type):
    transformed_df = transform_to_dataframe(input_df['0'][0], str_type)

    # round the values to decimal 2
    output_df = output_df.round(2)
    transformed_df = transformed_df.round(2)

    # replace NaN with None
    output_df = output_df.where(pd.notnull(output_df), None)
    transformed_df = transformed_df.where(pd.notnull(transformed_df), None)

    # compare values
    assert (output_df.values ==  transformed_df.values).all()

    # compare columns
    assert [str(x) for x in list(output_df.columns)] == [str(x) for x in list(transformed_df.columns)]



@pytest.mark.parametrize("input_df, output_dfs", transform_setup("split-dataframe-rows"))
def test_split_dataframe_rows(input_df, output_dfs):
    transformed_dfs = split_dataframe_rows(input_df, 'test')

    # deleted unneeded columns
    transformed_dfs = [df[[0]] for df in transformed_dfs]

    # sort both dfs
    output_dfs = sorted(output_dfs, key = lambda x: x.iloc[0,0])
    transformed_dfs = sorted(transformed_dfs, key = lambda x: x.iloc[0,0])

    for i in range(len(output_dfs)):
        # compare values
        assert (output_dfs[i].values ==  transformed_dfs[i].values).all()

    
@pytest.mark.parametrize("input_df, output_df, extract_field, preserve_origin_data", transform_setup("flatten-lists-to-dataframe"))
def test_flatten_lists_to_dataframe(input_df, output_df, extract_field, preserve_origin_data):
    transformed_df = flatten_lists_to_dataframe(input_df, extract_field, preserve_origin_data)

    # compare values
    assert (output_df.values ==  transformed_df.values).all()

    # compare columns
    assert [str(x) for x in list(output_df.columns)] == [str(x) for x in list(transformed_df.columns)]



@pytest.mark.parametrize("input_df, output_df", transform_setup("string-injecting"))
def test_string_injecting(input_df, output_df):
    transformed_df = string_injecting(input_df)

    # compare values
    assert (output_df.values ==  transformed_df.values).all()

    # compare columns
    assert [str(x) for x in list(output_df.columns)] == [str(x) for x in list(transformed_df.columns)]



@pytest.mark.parametrize("input_df, output_df, map_dict", transform_setup("rename-columns"))
def test_rename_columns(input_df, output_df, map_dict):
    transformed_df = rename_columns(input_df, map_dict)

    # compare values
    assert (output_df.values ==  transformed_df.values).all()

    # compare columns
    assert [str(x) for x in list(output_df.columns)] == [str(x) for x in list(transformed_df.columns)]



@pytest.mark.parametrize("input_df, output_df, extract_field, headers", transform_setup("json-array-to-dataframe"))
def test_json_array_to_dataframe(input_df, output_df, extract_field, headers):
    transformed_df = json_array_to_dataframe(input_df[extract_field], headers)

    # replace NaN with None
    output_df = output_df.where(pd.notnull(output_df), None)
    transformed_df = transformed_df.where(pd.notnull(transformed_df), None)

    # compare values
    assert (output_df.values ==  transformed_df.values).all()

    # compare columns
    assert [str(x) for x in list(output_df.columns)] == [str(x) for x in list(transformed_df.columns)]
