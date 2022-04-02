# transform content function
## transform content based on user & task inputs
## NOTE: might need to think of some parrellal solutions for this function

import pandas as pd
from task_bypass.tasktypes.transform.decompress_content import decompress_content
from task_bypass.tasktypes.transform.transform_to_dataframe import transform_to_dataframe

def transform_content(task_id, inputs, function, _from_output):
    
    # bytes to string
    if function == "decompress":
        comp_str = _from_output[_from_output.columns[0]][0]
        decom_str = decompress_content(comp_str)
        decom_df = pd.DataFrame([decom_str])
        
        
        return {
            task_id:  decom_df
        }
    
    if 'task_inputs' in inputs:
        task_inputs = inputs['task_inputs']
        if len(task_inputs) == 1:
            task_input = task_inputs[0]
            
            
            if function == "transform-to-dataframe":
                str_type = task_input['str_type']
                content = _from_output[_from_output.columns[0]][0]
                result = transform_to_dataframe(content, str_type)
                
                return {
                    task_id: result
                }
    return {}
