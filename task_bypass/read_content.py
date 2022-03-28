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
                    result_df = http_request(row)
                    result = result_df[result_df.columns[0]][0]
                    result_lists.append(result)

                return {
                    task_id: pd.DataFrame(result_lists)
                }
    
    if 'task_inputs' in inputs:
        task_inputs = inputs['task_inputs']
        if len(task_inputs) == 1:
            task_input = task_inputs[0]
            if 'extract_field' in task_input and type(_from_output).__name__ == 'DataFrame':
                extract_value = _from_output[task_input['extract_field']][0]
                result_df = http_request(extract_value)
                
                return {
                    task_id: result_df
                }
                
                
                
                
                
                

    return {}

