# read content function
## read content based on user & task inputs
## NOTE: might need to think of some parrellal solutions for this function
import pandas as pd
from task_bypass.tasktypes.read.http_request import http_request

def read_content(task_id, inputs, _from_output = None):
    # for now all the read_content will do http_request, so there isn't any input as http_request function

    result_lists = []
    if 'user_input' in inputs:
        user_input = inputs['user_input']
        if user_input['file_format'] == 'csv':
            input_df = pd.read_csv(user_input['file_name'], header=None)
            # only one field
            if len(input_df.columns) == 1:
                rows = input_df[0]
                ## NOTE
                for row in rows:
                    # each of url df will produce a str df in return
                    row_df = pd.DataFrame([row])
                    result_df = http_request(row_df)
                    # add dataframe into lists (produce list of dataframes)
                    result_lists.append(result_df)

                return {
                    task_id: result_lists 
                }
    
    if 'task_inputs' in inputs:
        task_inputs = inputs['task_inputs']
        if len(task_inputs) == 1:
            task_input = task_inputs[0]
            result_lists = []
            for single_df in _from_output:
                if 'extract_field' in task_input and type(single_df).__name__ == 'DataFrame':
                    extract_df = pd.DataFrame([single_df[task_input['extract_field']][0]])
                    # each of extract df will produce a df in return
                    result_df = http_request(extract_df)
                    # add dataframe into lists (produce list of dataframes)
                    result_lists.append(result_df)
                
            return {
                task_id: result_lists
            }
                
                
                
                
                
                

    return {}

