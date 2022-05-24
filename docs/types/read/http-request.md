# http-request
- http-request function is used for getting data from base APIs.
- User can provide the information of base APIs through a **file** or **through other tasks** in the yaml file.
- For input file defined tasks:
  - **file_name** is the path for your path, can be relative path. **Don't specify a header** for your file content. Your file content should be only one column of urls.
  - **file_format** is the format of your input file, now only supports csv format.
- Special feature:
  - **concurrent** is a read type function's special flag. You can decide your http requesting task to run **concurrently or not**. **Default is false**, so if you want your task to be concurrent just simply add this flag under `inputs` section.
  - **NOTE: But your task inputs/stage inputs need to be only a list with only ONE dataframe, or your task will fail with `ERROR: concat those dataframes first`. Input file doesn't have this limitation because you would only be permitted to provide one column and one file in a task.**   

   
## Function Syntax
### Has no task inputs/stage inputs (first task of the pipeline)  
```yml
id: <task name (identical) (required)>
description: <task description (optional)>
type: read 
function: http-request 
inputs:
  user_input:
    file_name: <the file path of your input file>
    file_format: <the file format of your input file, now supporting csv file> 
```
### Has task inputs/stage inputs
```yml
id: <task name (identical) (required)>
description: <task description (optional)>
type: read 
function: http-request 
inputs:
  concurrent: <run the task concurrently (optinal) (default is false)> 
  task_inputs(optional)/stage_inputs(optional):
    - from: <upstream task_id (required)>/<upstream stage_id (required)>
      preserve_origin_data: <whether to preserve other columns of data from the task input or not (optional) (default is false)> 
      extract_field: <which column of data should be extracted (optional) (default column is 0)> 
```

## Examples 
### Has no task inputs/stage inputs (first task of the pipeline)
```yml
id: webscrap_airbnb
description: "get airbnb website page url"
type: read
function: http-request
inputs:
  concurrent: true
  user_input:
    file_name: 'examples/input.csv'
    file_format: csv
``` 
### Has task inputs/stage inputs
```yml
id: call_gem_apis  
description: "call gem apis"
type: read 
function: http-request
inputs:
  concurrent: true
  task_inputs:
    - from: replace_gem_name_in_apis
      ... 
```

