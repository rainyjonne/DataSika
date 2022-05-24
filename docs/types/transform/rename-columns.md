# rename-columns
- rename-columns function is used for **renaming your dataframe columns**.
- For function usage:
  - **`<the old column name>`: `<the new column name>`**: you should use this syntax under **fields** section of `user_input` for specifying **the old columns (be replaced)** and **the new columns (replace)**. 
   

# Function Syntax
```yml
id: <task name (identical) (required)>
description: <task description (optional)>
type: transform 
function: rename-columns 
inputs:
  user_input:
    fields:
      - <the old column name>: <the new column name>
      - <the old column name>: <the new column name>
      ... 
  stage_inputs/task_inputs:
    - from: <upstream stage id (required)>/<upstream task id (required)> 
```


# An Example
```yml
id: rename_crime_columns
description: "renamed text column into crime_incidents"
type: transform
function: rename-columns
inputs:
  user_input:
    fields: 
      - text: crime_incidents
  task_inputs:
    - from: getting_crime_numbers
```

```yml
id: rename_to_gem_names
description: "renamed 0 column into gem_names"
type: transform
function: rename-columns
inputs:
  user_input:
    fields: 
      - 0: gem_names 
  task_inputs:
    - from: flatten_gem_lists
```
