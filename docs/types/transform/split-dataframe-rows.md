# split-dataframe-rows
- split-dataframe-rows function is used for **turning your dataframe rows into list of dataframes**.
  - e.g. there are 4 rows in your dataframe ('apple', 'banana', 'orange', 'guava') -> turn to **list of 4 dataframes** and each dataframe **contains a row of a fruit kind**
- You don't need to specify any other special user inputs for this task. 


# Function Syntax
```yml
id: <task name (identical) (required)>
description: <task description (optional)>
type: transform 
function: split-dataframe-rows 
inputs:
  stage_inputs/task_inputs:
    - from: <upstream stage id (required)>/<upstream task id (required)> 
```

```yml
id: create_city_dataframes
description: "put different city data into different dataframes"
type: transform
function: split-dataframe-rows
inputs:
  task_inputs:
    - from: extract_content
```
