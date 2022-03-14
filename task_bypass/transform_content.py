# transform content function
## transform content based on user & task inputs
## NOTE: might need to think of some parrellal solutions for this function

import pandas as pd
from task_bypass.tasktypes.transform.decompress_content import decompress_content
from task_bypass.tasktypes.transform.transform_to_dataframe import transform_to_dataframe

def transform_content(task_id, inputs, output, function, _from_output):
    if 'name' not in output:
        output_name = None
    else:
        output_name = output['name']
    
    if function == "decompress":
        decom_str = decompress_content(_from_output)
        
        return {
            task_id: {
                "name": output_name,
                "result": decom_str
            }
        }
    if 'task_inputs' in inputs:
        task_inputs = inputs['task_inputs']
        if len(task_inputs) == 1:
            task_input = task_inputs[0]
            if function == "transform-to-dataframe":
                params = task_input['params']
                result = transform_to_dataframe(_from_output, params)
                
                return {
                    task_id: {
                        "name": output_name,
                        "result": result
                    }
                }
    return {}
