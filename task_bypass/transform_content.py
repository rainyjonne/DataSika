# transform content function
## transform content based on user & task inputs
## NOTE: might need to think of some parrellal solutions for this function

import pandas as pd
from task_bypass.tasktypes.transform.decompress_content import decompress_content
from task_bypass.tasktypes.transform.transform_to_dataframe import transform_to_dataframe

def transform_content(task_id, inputs, function, _from_output):
    
    # bytes to string
    if function == "decompress":
        decom_str = decompress_content(_from_output)
        
        return {
            task_id:  decom_str
        }
    
    if 'task_inputs' in inputs:
        task_inputs = inputs['task_inputs']
        if len(task_inputs) == 1:
            task_input = task_inputs[0]
            
            
            if function == "transform-to-dataframe":
                str_type = task_input['str_type']
                result = transform_to_dataframe(_from_output, str_type)
                
                return {
                    task_id: result
                }
    return {}
