# Define your own task
- A task is the **basic unit** of the data pipeline. You will define an **id (name)** and a **description** for this stage which represents this task. Also, your id **shouldn't contain special characters** (e.g. `$%^&-`), only **underline** (e.g. `_`) is permitted.
- You will also define a **function** and the **type** of the function you need. This function will be applied to your data based on the syntax you provides.
- Depending on the characteristics of those functions, you will need to define those tasks differently. Usually, there are **task_inputs**, **stage_inputs** and **user_input** in a task.
  - **task_inputs (defined when needed)** are used to specify the **dependencies** for the pipeline, which means that you will define **which task's output will become this task's input**. It will be defined when you are getting data from the task which comes from the **same stage**. You should specify a task id under the keyword `from` for Sika to know where to find your data.
  - **stage_inputs (defined when needed)** are used when your data comes from another stage. You should specify a stage id under the keyword `from` for Sika to know where to find your data.
  - **user_input (required)** is used to define user provided **syntaxes** which will be applied to `the data from task_inputs` or `read in data source from the syntaxes`

 
## Structure Syntax
```yml
tasks:
  - id: <task name (identical) (required)>
    description: <task description (optional)>
    type: <task type (required)>
    function: <task function (required)>
    inputs:
      user_input:
        ...
      task_inputs(optional)/stage_inputs(optional):
	- from: <task_id (required)>/<stage_id (required)> 
        ...
      ...
```
 
## An Example
###  read type task (http-request-dynamic) & filter type task (json-path)
```yml
tasks:
  - id: request_uk_crime_data
    description: "mapping request params"
    type: read
    function: http-request-dynamic
    inputs:
      concurrent: true
      user_input:
        base_url: "https://data.police.uk/api/crimes-street/all-crime"
        params_dynamic:
          - name: lat
            value: latitude
          - name: lng
            value: longitude
        params_fixed:
          - name: date
            value: '2022-03'
      stage_inputs:
        - from: airbnb_stage 
  - id: getting_crime_numbers
    description: "get crime statistic data"
    type: filter 
    function: json-path 
    inputs:
      user_input:
        field: '$.`len`' 
      task_inputs:
        - from: request_uk_crime_data
          extract_field: text
          preserve_origin_data: True
``` 
