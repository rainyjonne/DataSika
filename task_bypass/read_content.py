# read content function
## read content based on user & task inputs
## NOTE: might need to think of some parrellal solutions for this function
import pandas as pd
from task_bypass.tasktypes.read.webpage_request import webpage_request
from task_bypass.tasktypes.read.http_request import http_request


def read_content(task_id, inputs, output, function, _from_output = None):
    if 'name' not in output:
        output_name = None
    else:
        output_name = output['name']

    result_lists = []
    if 'user_input' in inputs:
        user_input = inputs['user_input']
        if user_input['file_format'] == 'csv':
            input_df = pd.read_csv(user_input['file_name'])
            if user_input['one_field'] == True:
                rows = input_df[user_input['field']]
                ## NOTE
                for row in rows:
                    result = webpage_request(row, output['format'])
                    result_lists.append(result)

                return {
                    task_id: {
                        "name": output_name,
                        "result": result_lists
                    }
                }
    
    if 'task_inputs' in inputs:
        task_inputs = inputs['task_inputs']
        if len(task_inputs) == 1:
            task_input = task_inputs[0]
            if 'extract_field' in task_input and task_input['type'] == 'dataframe':
                extract_value = _from_output[task_input['extract_field']][0]
                result = http_request(extract_value, output['format'])
                
                return {
                    task_id: {
                        "name": output_name,
                        "result": result
                    }
                }
                
                
                
                
                
                

    return {}
