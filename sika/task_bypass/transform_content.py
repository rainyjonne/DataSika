# transform content function
## transform content based on user & task inputs
## NOTE: might need to think of some parrellal solutions for this function

import pandas as pd
import json
from functools import reduce
from sika.task_bypass.tasktypes.transform.decompress_content import decompress_content
from sika.task_bypass.tasktypes.transform.transform_to_dataframe import transform_to_dataframe, json_array_to_dataframe
from sika.task_bypass.tasktypes.transform.rename_columns import rename_columns
from sika.task_bypass.tasktypes.transform.sampling import sampling 
from sika.task_bypass.tasktypes.transform.sub_selection import sub_selection 
from sika.task_bypass.tasktypes.transform.split_dataframe_rows import split_dataframe_rows 
from sika.task_bypass.tasktypes.transform.flatten_lists_to_dataframe import flatten_lists_to_dataframe 
from sika.task_bypass.tasktypes.transform.string_injecting import string_injecting 

def transform_content(task_id, inputs, function, _from_output):
    # presetting
    if 'stage_inputs' in inputs:
        task_input = inputs['stage_inputs'][0]
    else:
        task_input = inputs['task_inputs'][0]

    # default not preserving origin data
    extract_field = None
    preserve_origin_data = False
    if 'extract_field' in task_input:
        extract_field = task_input['extract_field']

    if 'preserve_origin_data' in task_input:
        preserve_origin_data = task_input['preserve_origin_data']

    if function == "split-dataframe-rows":
        result_lists = []
        for single_df in _from_output:
            split_df_rows = split_dataframe_rows(single_df, task_id)
            result_lists.extend(split_df_rows)
        return {
            task_id:  result_lists
        }

    # bytes to string
    if function == "decompress":
        result_lists = []
        for single_df in _from_output:
            if extract_field:
                comp_str_obj = single_df[extract_field]
            else:
                comp_str_obj = single_df[single_df.columns[0]]
            comp_df = pd.DataFrame([comp_str_obj])
            decom_df = decompress_content(comp_df)
            result_lists.append(decom_df)

        return {
            task_id:  result_lists
        }

    if function == "sampling":
        user_input = inputs['user_input']
        sampling_nums = user_input["nums"]
        seed = None
        if 'seed' in user_input:
            seed = user_input['seed']
        result_lists = []
        for single_df in _from_output:
            result_df = sampling(single_df, sampling_nums, seed)
            result_lists.append(result_df)

        return {
            task_id: result_lists
        }

    if function == "sub-selection":
        user_input = inputs['user_input']
        start_idx = user_input['start_idx']
        end_idx = user_input['end_idx']
        result_lists = []
        for single_df in _from_output:
            result_df = sub_selection(single_df, start_idx, end_idx)
            result_lists.append(result_df)

        return {
            task_id: result_lists
        }


    if function == "rename-columns":
        user_input = inputs['user_input']
        mappings = user_input["fields"]
        map_dict = reduce(lambda a, b: {**a, **b}, mappings)
        result_lists = []
        for single_df in _from_output:
            result_df = rename_columns(single_df, map_dict)
            result_lists.append(result_df)

        return {
            task_id: result_lists
        }



    if  function == "transform-to-dataframe":
        str_type = task_input['str_type']
        result_lists = []
        for single_df in _from_output:
            # if user identify extract_field
            if extract_field:
                # only take the content from index 0
                content = single_df[extract_field][0]
            else:
                content = single_df[single_df.columns[0]][0]
            result_df = transform_to_dataframe(content, str_type)
            result_lists.append(result_df)

        return {
            task_id: result_lists
        }

    if  function == "json-array-to-dataframe":
        result_lists = []
        for single_df in _from_output:
            # if user identify extract_field
            if extract_field:
                content = single_df[extract_field]
            else:
                content = single_df[single_df.columns[0]]

            headers = task_input['headers']
            result_df = json_array_to_dataframe(content, headers)
            result_lists.append(result_df)

        return {
            task_id: result_lists
        }


    if  function == "flatten-lists-to-dataframe":

        result_lists = []
        for single_df in _from_output:
            result_df = flatten_lists_to_dataframe(single_df, extract_field, preserve_origin_data)
            result_lists.append(result_df)

        return {
            task_id: result_lists
        }

    if  function == "string-injecting":
        user_input = inputs['user_input']
        base_str = user_input['base_str']
        base_df = pd.DataFrame()

        mapping_items = user_input['inject_str']

        mapping_fields = {}
        result_lists = []
        for single_df in _from_output:
            for item in mapping_items:
                injecting_nums = len(single_df[item['value']])
                base_df = base_df.append([base_str]*injecting_nums, ignore_index=True)
                base_df[item['name']] = list(single_df[item['value']])
                mapping_fields[item['name']] = item['value']
                
            result_df = string_injecting(base_df)
            result_lists.append(result_df)

        return {
            task_id: result_lists
        }



    return {}
