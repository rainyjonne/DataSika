from task_bypass.tasktypes.filter.json_path import json_path
from task_bypass.tasktypes.filter.sql import sql 
from task_bypass.tasktypes.filter.xpath import xpath 
from task_bypass.tasktypes.read.http_request import http_request, http_request_dynamic
from task_bypass.tasktypes.merge.sql_merge import sql_merge 
from task_bypass.tasktypes.transform.decompress_content import decompress_content 
from task_bypass.tasktypes.transform.flatten_lists_to_dataframe import flatten_lists_to_dataframe
from task_bypass.tasktypes.transform.split_dataframe_rows import split_dataframe_rows 
from task_bypass.tasktypes.transform.string_injecting import string_injecting 
from task_bypass.tasktypes.transform.rename_columns import rename_columns 
from task_bypass.tasktypes.transform.transform_to_dataframe import transform_to_dataframe, json_array_to_dataframe 
from task_bypass.run_stages import run_stages 
from task_bypass.allocate_stage_tasks import allocate_stage_tasks 

def function_handler(function, params: tuple):
    resp_df = globals()[function](*params)
    return resp_df


def stages_handler(function, params: tuple):
    final_output = globals()[function](*params)
    final_df = final_output['concat_final_dataframes'][0]
    return final_df


def tasks_handler(function, params: tuple):
    final_output = globals()[function](*params)
    final_df = list(final_output.values())[0][0]
    return final_df

