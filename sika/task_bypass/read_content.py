# read content function
## read content based on user & task inputs
## NOTE: might need to think of some parrellal solutions for this function
import pandas as pd
from sika.task_bypass.tasktypes.read.http_request import http_request, http_request_dynamic 
from IPython import embed

def read_content(db, stage_name, task_id, inputs, function, _from_output = None):
    # for now all the read_content will do http_request related jobs
    concurrent = False
    if 'concurrent' in inputs:
        concurrent = inputs['concurrent']

    # if has input dataframes
    dataframe_length = 1
    if _from_output:
        dataframe_length = len(_from_output)
    # your input should be only one dataframe to do the concurrent tasks
    # else would throw an error and prompt you to concat your list of dataframes to only list of only one dataframe
    if concurrent and dataframe_length != 1:
        raise ValueError(f"You can not run concurrent http request tasks on `list that contains over 1 dataframe`, please concat your dataframes first. #ref: {task_id}")


    task_input = None
    if 'stage_inputs' in inputs:
        task_input = inputs['stage_inputs'][0]
    if 'task_inputs' in inputs:
        task_input = inputs['task_inputs'][0]

    if task_input:
        if function == 'http-request':
            result_lists = []
            extract_field = 0
            if 'extract_field' in task_input:
                extract_field = task_input['extract_field']

            preserve_origin_data = None
            if 'preserve_origin_data' in task_input:
                preserve_origin_data = task_input['preserve_origin_data']

            for single_df in _from_output:
                result_df = http_request(db, stage_name, task_id, single_df, extract_field, preserve_origin_data, concurrent)


                # add dataframe into lists (produce list of dataframes)
                result_lists.append(result_df)

            return {
                task_id: result_lists
            }


        if function == "http-request-dynamic":
            user_input = inputs['user_input']
            params_df = pd.DataFrame({
                'base_url': [user_input['base_url']],
            })

            mapping_items = None
            if 'params_dynamic' in user_input:
                mapping_items = user_input['params_dynamic']
            fixed_items = user_input['params_fixed']
            param_dict = {}
            preserve_fields = []
            result_lists = []
            mapping_fields = {}
            for single_df in _from_output:
                for item in mapping_items:
                    param_dict[item['name']] = list(single_df[item['value']])
                    preserve_fields.append(item['name'])
                    mapping_fields[item['name']] = item['value']
                
                if param_dict:
                    params_df = pd.DataFrame(param_dict)

                for item in fixed_items:
                    params_df[item['name']] = item['value']

                params_df['base_url'] = user_input['base_url']

                if 'headers' in user_input:
                    params_df['headers'] = json.dumps(user_input['headers'])

                page_name = None
                if 'pagination' in user_input:
                    page_name = user_input['pagination']['name']
                    till = user_input['pagination']['till']
                    params_df[page_name] = till

                result_df = http_request_dynamic(db, stage_name, task_id, params_df, preserve_fields, mapping_fields, page_name, concurrent)

                result_lists.append(result_df)

            return {
                task_id: result_lists
            }

    result_lists = []
    if 'user_input' in inputs:
        user_input = inputs['user_input']
        extract_field = 0  
        if 'extract_field' in user_input:
            extract_field = user_input['extract_field']

        file_format = None
        if 'file_format' in user_input:
            file_format = user_input['file_format']
            file_name = user_input['file_name']

        base_url = None
        if 'base_url' in user_input:
            base_url = user_input['base_url']

        if function == 'http-request':
            if file_format == 'csv':
                if extract_field:
                    input_df = pd.read_csv(file_name)
                    rows = input_df[extract_field]
                else:
                    input_df = pd.read_csv(file_name, header=None)
                    # default take index 0 column as input
                    rows = input_df[0]
                ## NOTE
                for row in rows:
                    # each of url df will produce a str df in return
                    row_df = pd.DataFrame([row])
                    result_df = http_request(db, stage_name, task_id, row_df, concurrent=concurrent)
                    # add dataframe into lists (produce list of dataframes)
                    result_lists.append(result_df)

                return {
                    task_id: result_lists
                }

            if base_url:
                params_df = pd.DataFrame([base_url])
                result_df = http_request(db, stage_name, task_id, params_df, concurrent=concurrent)

                result_lists.append(result_df)

                return {
                    task_id: result_lists
                }

        if function == "http-request-dynamic":
            params_df = pd.DataFrame({
                'base_url': [base_url],
            })

            fixed_items = user_input['params_fixed']
            preserve_fields = []
            result_lists = []
            mapping_fields = {}

            for item in fixed_items:
                params_df[item['name']] = item['value']

            params_df['base_url'] = base_url 

            if 'headers' in user_input:
                params_df['headers'] = json.dumps(user_input['headers'])

            page_name = None
            if 'pagination' in user_input:
                page_name = user_input['pagination']['name']
                start = user_input['pagination']['start']
                end = user_input['pagination']['end']
                params_df[page_name] = f"[{start}, {end}]"

            result_df = http_request_dynamic(db, stage_name, task_id, params_df, preserve_fields, mapping_fields, page_name, concurrent)

            result_lists.append(result_df)

            return {
                task_id: result_lists
            }





    return {}

