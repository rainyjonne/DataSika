# transform-to-dataframe 
- transform-to-dataframe function is used for **turning your dataframe rows into list of dataframes**.
- For function usage:
  - **str_type** is the **read in content's type** that you want to transform to a dataframe. Sika now supports well-formated **csv** and **json** strings.
  - **NOTE: Make sure your upstream task input ONLY have one column and one row for this function to read in.**

# Function Syntax
```yml
id: <task name (identical) (required)>
description: <task description (optional)>
type: transform 
function: transform-to-dataframe 
inputs:
  stage_inputs/task_inputs:
    - from: <upstream stage id (required)>/<upstream task id (required)> 
      str_type: <the read in content type> 
```

# An Example
```yml
id: read_csv_str_to_table
description: "read csv str to dataframe"
type: transform
function: transform-to-dataframe
inputs:
  task_inputs:
    - str_type: csv
      from: decompress_file_str
```
