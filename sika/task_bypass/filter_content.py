## filter content based on user & task inputs
## NOTE: might need to think of some parrellal solutions for this function

import pandas as pd 
from sika.task_bypass.tasktypes.filter.xpath import xpath
from sika.task_bypass.tasktypes.filter.sql import sql
from sika.task_bypass.tasktypes.filter.json_path import json_path

def filter_content(task_id, inputs,  function, _from_output, _last_output_name):
    # presetting
    user_input = inputs['user_input']

    if 'stage_inputs' in inputs:
        task_input = inputs['stage_inputs'][0]
    else:
        task_input = inputs['task_inputs'][0]

    extract_field = None
    if 'extract_field' in task_input:
        extract_field = task_input['extract_field']

    preserve_origin_data = False 
    if 'preserve_origin_data' in task_input:
        preserve_origin_data = task_input['preserve_origin_data']

    # only one field value
    if "field" in user_input:
        syntax = user_input['field']
        if function == "xpath":
            result_lists = []
            for single_df in _from_output:
                # each of dataframe from last task will produce a dataframe in return
                result_df = xpath(single_df, syntax, extract_field)
                # add to list of dataframes
                result_lists.append(result_df)
            return {
                task_id: result_lists
            }
        if function == "sql":
            result_lists = []
            for single_df in _from_output:
                # each of dataframe from last task will produce a dataframe in return
                filtered_df = sql(_last_output_name, single_df, syntax)
                # add to list of dataframes
                result_lists.append(filtered_df)
            
            return {
                task_id: result_lists
            }
    
        if function == "json-path":
            result_lists = []
            for single_df in _from_output:
                # each of dataframe from last task will produce a dataframe in return
                filtered_df = json_path(single_df, syntax, extract_field, preserve_origin_data)
                # add to list of dataframes
                result_lists.append(filtered_df)
            
            return {
                task_id: result_lists
            }    
  
        
    # fields for making a dataframe 
    if "fields" in user_input:
        fields = user_input['fields']
        columns = [field['name'] for field in fields]
        values = [[field['value'] for field in fields]]
        input_df = pd.DataFrame(values, columns=columns)
   
    
        if function == "xpath":
            final_result_lists = []
            for single_df in _from_output:
                result_df = pd.DataFrame(columns=columns)
                ## NOTE
                # turn to list
                rows = list(single_df[0])
                for idx, row in enumerate(rows):
                    row_result_lists = []
                    for column in columns:
                        row_df = pd.DataFrame([row])
                        row_result = xpath(row_df, input_df[column][0])
                        # get the string content inside the dataframe
                        row_result_lists.append(row_result[0][0])
                
                    result_df.loc[idx] = row_result_lists
                    
                # add a ready dataframe into final dataframe lists   
                final_result_lists.append(result_df)
                
            
                
            return {
                task_id: final_result_lists
            }    
                


    return {}

