from .handler import function_handler
import yaml
import pytest
import pandas as pd
import numpy as np
from packaging import version


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


    if function == "sampling":
        extract_infos = [file_info for file_info in file_infos if file_info['function'] == "sampling"] 
        transform_infos = []
        for info in extract_infos:
            # get file infos
            input_file = info['input_file']
            output_file = info['output_file']
            sampling_nums = info['nums']
            seed = info['seed']

            # create input & output dfs
            input_df = pd.read_csv(input_file)
            output_df = pd.read_csv(output_file)

            transform_infos.append((input_df, output_df, sampling_nums, seed))

        return transform_infos

    if function == "sub-selection":
        extract_infos = [file_info for file_info in file_infos if file_info['function'] == "sub-selection"] 
        transform_infos = []
        for info in extract_infos:
            # get file infos
            input_file = info['input_file']
            output_file = info['output_file']
            start_idx = info['start_idx']
            end_idx = info['end_idx']

            # create input & output dfs
            input_df = pd.read_csv(input_file)
            output_df = pd.read_csv(output_file)

            transform_infos.append((input_df, output_df, start_idx, end_idx))

        return transform_infos


@pytest.mark.parametrize("input_df, output_df", transform_setup("decompress-content"))
def test_decompress_content(input_df, output_df):
    params = (input_df, )
    transformed_df = function_handler('decompress_content', params)

    # compare values
    assert (output_df.values ==  transformed_df.values).all()

    # compare columns
    assert [str(x) for x in list(output_df.columns)] == [str(x) for x in list(transformed_df.columns)]



@pytest.mark.parametrize("input_df, output_df, str_type", transform_setup("transform-to-dataframe"))
def test_transform_to_dataframe(input_df, output_df, str_type):
    params = (input_df['0'][0], str_type)
    transformed_df = function_handler('transform_to_dataframe', params)

    # round the values to decimal 2
    output_df = output_df.round(2)
    transformed_df = transformed_df.round(2)

    # replace NaN with None
    if version.parse(pd.__version__) >= version.parse('1.3.0'):
        output_df = output_df.replace({np.nan: None})
        transformed_df = transformed_df.replace({np.nan: None})
    else:
        output_df = output_df.where(pd.notnull(output_df), None)
        transformed_df = transformed_df.where(pd.notnull(filtered_df), None)


    # compare values
    assert (output_df.values ==  transformed_df.values).all()

    # compare columns
    assert [str(x) for x in list(output_df.columns)] == [str(x) for x in list(transformed_df.columns)]



@pytest.mark.parametrize("input_df, output_dfs", transform_setup("split-dataframe-rows"))
def test_split_dataframe_rows(input_df, output_dfs):
    params = (input_df, 'test')
    transformed_dfs = function_handler('split_dataframe_rows', params)

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
    params = (input_df, extract_field, preserve_origin_data)
    transformed_df = function_handler('flatten_lists_to_dataframe', params)

    # compare values
    assert (output_df.values ==  transformed_df.values).all()

    # compare columns
    assert [str(x) for x in list(output_df.columns)] == [str(x) for x in list(transformed_df.columns)]



@pytest.mark.parametrize("input_df, output_df", transform_setup("string-injecting"))
def test_string_injecting(input_df, output_df):
    params = (input_df, )
    transformed_df = function_handler('string_injecting', params)

    # compare values
    assert (output_df.values ==  transformed_df.values).all()

    # compare columns
    assert [str(x) for x in list(output_df.columns)] == [str(x) for x in list(transformed_df.columns)]



@pytest.mark.parametrize("input_df, output_df, map_dict", transform_setup("rename-columns"))
def test_rename_columns(input_df, output_df, map_dict):
    params = (input_df, map_dict)
    transformed_df = function_handler('rename_columns', params)

    # compare values
    assert (output_df.values ==  transformed_df.values).all()

    # compare columns
    assert [str(x) for x in list(output_df.columns)] == [str(x) for x in list(transformed_df.columns)]



@pytest.mark.parametrize("input_df, output_df, extract_field, headers", transform_setup("json-array-to-dataframe"))
def test_json_array_to_dataframe(input_df, output_df, extract_field, headers):
    params = (input_df[extract_field], headers)
    transformed_df = function_handler('json_array_to_dataframe', params)

    # replace NaN with None
    if version.parse(pd.__version__) >= version.parse('1.3.0'):
        output_df = output_df.replace({np.nan: None})
        transformed_df = transformed_df.replace({np.nan: None})
    else:
        output_df = output_df.where(pd.notnull(output_df), None)
        transformed_df = transformed_df.where(pd.notnull(filtered_df), None)

    # compare values
    assert (output_df.values ==  transformed_df.values).all()

    # compare columns
    assert [str(x) for x in list(output_df.columns)] == [str(x) for x in list(transformed_df.columns)]


@pytest.mark.parametrize("input_df, output_df, sampling_nums, seed", transform_setup("sampling"))
def test_sampling(input_df, output_df, sampling_nums, seed):
    params = (input_df, sampling_nums, seed)
    transformed_df = function_handler('sampling', params)

    # compare values
    assert (output_df.values ==  transformed_df.values).all()

    # compare columns
    assert [str(x) for x in list(output_df.columns)] == [str(x) for x in list(transformed_df.columns)]


@pytest.mark.parametrize("input_df, output_df, start_idx, end_idx", transform_setup("sub-selection"))
def test_sub_selection(input_df, output_df, start_idx, end_idx):
    params = (input_df, start_idx, end_idx)
    transformed_df = function_handler('sub_selection', params)

    # compare values
    assert (output_df.values ==  transformed_df.values).all()

    # compare columns
    assert [str(x) for x in list(output_df.columns)] == [str(x) for x in list(transformed_df.columns)]

