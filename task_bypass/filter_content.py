## filter content based on user & task inputs
## NOTE: might need to think of some parrellal solutions for this function

import pandas as pd 
from task_bypass.tasktypes.filter.xpath import xpath
from task_bypass.tasktypes.filter.sql import sql

def filter_content(task_id, inputs, output, function, _from_output, _last_output_name):
    user_input = inputs['user_input']
    if 'name' not in output:
        output_name = None
    else:
        output_name = output['name']

    if user_input['type'] == "str":
        value = user_input['value']
        if function == "xpath":
            ## NOTE: here presume there is only one element in output section
            rows = xpath(_from_output[0], value)
            return {
                task_id: {
                    "name": output_name,
                    "result": rows
                }
            }
        if function == "sql":
            filtered_df = sql(_last_output_name, _from_output, value)
            
            return {
                task_id: {
                    "name": output_name,
                    "result": filtered_df
                }
            }
            
            
        
    # wait for the third task 
    elif user_input['type'] == "dataframe":
        fields = user_input['fields']
        columns = [field['name'] for field in fields]
        values = [[field['value'] for field in fields]]
        input_df = pd.DataFrame(values, columns=columns)
        result_df = pd.DataFrame(columns=columns)
        if function == "xpath":
            ## NOTE
            for idx, single_output in enumerate(_from_output):
                result_lists = []
                for column in columns:
                    result = xpath(single_output, input_df[column][0])[0]
                    result_lists.append(result)
                
                result_df.loc[idx] = result_lists
            return {
                task_id: {
                    "name": output_name,
                    "result": result_df
                }
            }    
                


    return {}

