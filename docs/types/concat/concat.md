# concat 
- concat function is used for **combining all your dataframes data together into only one big dataframe**.
- It will be used **in the end of one stage**, as a task that aggregating data together into a big table which will be stored in the sqlite file.
  - **NOTE: So if your last task of one stage isn't the concat type task, your pipeline will throw an error.**
- You don't need to specify any other special user inputs for this task.
 
## Function Syntax
```yml
id: <task name (identical) (required)>
description: <task description (optional)>
type: concat 
function: concat 
inputs:
  task_inputs:
    - from: <upstream task id (required)> 
```

## Examples
```yml
id: concat_final_dataframes
description: "concat list of final dataframes together"
type: concat
function: concat
inputs:
  task_inputs:
    - from: transform_price
``` 

```yml
id: concat_gem_names_dataframes 
description: "concat gem names dataframe"
type: concat 
function: concat
inputs:
  task_inputs:
    - from: pick_sub_selections
``` 
