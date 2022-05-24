# sub-selection 
- sub-selection function is used for **doing sub-selection of your original upstream task input**.
- For function usage:
  - **start_idx** is defined with **the starting row index** of your sub-selection.
  - **end_idx** is defined with **the ending row index** of your sub-selection.
  - e.g. for a 100 rows dataframe, I only want to get its **top 50 rows** -> `start_idx` should be 0, `end_idx` should be 49 (**NOTE: index starts with 0**)

# Function Syntax
```yml
id: <task name (identical) (required)>
description: <task description (optional)>
type: transform 
function: sub-selection 
inputs:
  user_input:
    start_idx: <the start row for sub-selection>
    end_idx: <the end row for sub-selection>
  stage_inputs/task_inputs:
    - from: <upstream stage id (required)>/<upstream task id (required)> 
```

# An Example
```yml
id: pick_sub_selections 
description: 'there are too many gems, so pick 60 samplings for example'
type: transform
function: sub-selection 
inputs:
  user_input:
    start_idx: 0
    end_idx: 59 
  task_inputs:
    - from: rename_to_gem_names
```
