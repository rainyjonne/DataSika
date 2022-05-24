# decompress 
- decompress function is used for decompressing **gzip data** and return the origin **decompressed content**.
- You don't need to specify any other special user inputs for this task. Jus make sure your task's **upstream task input** is an **compressed content**.

# Function Syntax
```yml
id: <task name (identical) (required)>
description: <task description (optional)>
type: transform 
function: decompress 
inputs:
  stage_inputs/task_inputs:
    - from: <upstream stage id (required)>/<upstream task id (required)> 
```

# An Example
```yml
id: decompress_file_str
description: "decompress file str"
type: transform
function: decompress
inputs:
  task_inputs:
    - from: request_listing_file
```

