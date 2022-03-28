## filter content based on user & task inputs
## NOTE: might need to think of some parrellal solutions for this function

import pandas as pd 
from task_bypass.tasktypes.filter.xpath import xpath
from task_bypass.tasktypes.filter.sql import sql


def filter_content(task_id, inputs,  function, _from_output, _last_output_name):
    user_input = inputs['user_input']

    # only one field value
    # input: string -> output: string
    if "field" in user_input:
        pattern = user_input['field']
        if function == "xpath":
            ## NOTE: here presume there is only one element in output section
            ## NOTE: taken one output content from a dataframe
            rows = xpath(_from_output[0][0], pattern)
            return {
                task_id: pd.DataFrame(rows)
            }
        if function == "sql":
            filtered_df = sql(_last_output_name, _from_output, pattern)
            
            return {
                task_id: filtered_df
            }
            
            
        
    # fields for making a dataframe 
    # input: string -> output: dataframe
    if "fields" in user_input:
        fields = user_input['fields']
        columns = [field['name'] for field in fields]
        values = [[field['value'] for field in fields]]
        input_df = pd.DataFrame(values, columns=columns)
        result_df = pd.DataFrame(columns=columns)
        # turn to list
        output_list = list(_from_output[0])
        if function == "xpath":
            ## NOTE
            for idx, single_output in enumerate(output_list):
                result_lists = []
                for column in columns:
                    result = xpath(single_output, input_df[column][0])
                    # get the string content inside the dataframe
                    result_lists.append(result[0][0])
                
                result_df.loc[idx] = result_lists
            return {
                task_id: result_df
            }    
                


    return {}

