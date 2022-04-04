# transform content function
## transform content based on user & task inputs
## NOTE: might need to think of some parrellal solutions for this function

import pandas as pd
from task_bypass.tasktypes.transform.decompress_content import decompress_content
from task_bypass.tasktypes.transform.transform_to_dataframe import transform_to_dataframe

def transform_content(task_id, inputs, function, _from_output):
    
    # bytes to string
    if function == "decompress":
        result_lists = []
        for single_df in _from_output:
            comp_str_obj = single_df[single_df.columns[0]]
            comp_df = pd.DataFrame([comp_str_obj])
            decom_df = decompress_content(comp_df)
            result_lists.append(decom_df)
        
        return {
            task_id:  result_lists
        }
    
    if 'task_inputs' in inputs:
        task_inputs = inputs['task_inputs']
        if len(task_inputs) == 1:
            task_input = task_inputs[0]
            
            
            if function == "transform-to-dataframe":
                str_type = task_input['str_type']
                result_lists = []
                for single_df in _from_output:
                    content = single_df[single_df.columns[0]][0]
                    result_df = transform_to_dataframe(content, str_type)
                    result_lists.append(result_df)
                
                return {
                    task_id: result_lists
                }
    return {}