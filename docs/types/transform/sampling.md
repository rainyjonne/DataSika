# sampling 
- sampling function is used for **taking samples from dataframes**.
- For function usage:
  - **nums** is **how many samplings you want to take**, if you set this number **higher than your upstream task input** than your sampling mechanism will use **replace mechanism**.
  - **seed** is an **optional flag**. If you want your sampling results to be different every time, you don't need to specify this param. If you want your sampling results to be the same every time, choose a number for this sampling task. 


# Function Syntax
```yml
id: <task name (identical) (required)>
description: <task description (optional)>
type: transform 
function: sampling 
inputs:
  user_input:
    nums: <how many samplings you want>
    seed: <you can specify a fixed number then everytime your sampling results will be the same (optional)>
  stage_inputs/task_inputs:
    - from: <upstream stage id (required)>/<upstream task id (required)> 
```

# An Example
```yml
id: pick_samplings
description: 'there are too many hostings, so each city pick 15 samplings (60 for all)'
type: transform
function: sampling 
inputs:
  user_input:
    nums: 15
    seed: 1
  task_inputs:
    - from: filter_nan_rows
```
