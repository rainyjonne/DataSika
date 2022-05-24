# flatten-lists-to-dataframe
- flatten-lists-to-dataframe function is used for **flattening json-path return json lists to dataframe columns **.
  - e.g. ['dog', 'cat', 'turtle']
- You don't need to specify any other special user inputs for this task, but you need to make sure that the extract column of your **upstream task inputs should contains json lists content**. 


# Function Syntax
```yml
id: <task name (identical) (required)>
description: <task description (optional)>
type: transform 
function: flatten-lists-to-dataframe
inputs:
  stage_inputs/task_inputs:
    - from: <upstream stage id (required)>/<upstream task id (required)> 
```


# An Example
```yml
id: flatten_gem_lists 
description: "using flatten function to get a dataframe of gem names"
type: transform 
function: flatten-lists-to-dataframe 
inputs:
  task_inputs:
    - from: filter_gem_names 
      extract_field: text
```
