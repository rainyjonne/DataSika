# http-request-dynamic
- http-request function is used for getting data from a base API with other additional dynamic params.
- For task inputs/stage inputs and concurrent features, you can see details from http-request function document. [Ref](http-request.md)
- For the syntax definition in `user_inputs` section:
  - **base_url** is the base requesting link.
  - **params_fixed** are the params that has **fixed values**, which means that after mapping params with base requesting link you would get **the same values** as the other mapping links.
  - **params_dynamic** are the params that are mapped dynamically. You would get the input data from upstream task inputs/stage inputs. You would specify the param name with a corresponding `column name (the column you wanna pick for mapping param name)`, which means that after mapping params with base requesting link you would get **different values** as the other mapping links.
  - **pagination** is the special param only for getting **looping paging data**. It means that if you want to get the content from a paging requesting link, you only have to specify the **start (starting page number)** and the **end (ending page number)** in your task info then Sika will do the looping over for you. 



## Function Syntax
```yml
id: <task name (identical) (required)>
description: <task description (optional)>
type: read 
function: http-request-dynamic 
inputs:
  user_inputs:
    base_url: <the base url for requesting>
    params_dynamic:
      - name: <the param name>
        value: <the column name from the upstream task/stage inputs>
    params_fixed:
      - name: <the param name> 
        value: <the fixed param value> 
    pagination:
      name: <the param name for pagination> 
      start: <start page number>
      end: <end page number>
  concurrent: <run the task concurrently (optinal) (default is false)> 
  task_inputs(optional)/stage_inputs(optional):
    ...
```

## Examples
```yml 
id: request_uk_crime_data
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
```

```yml
id: get_gem_basic_infos  
description: "get basic infos for all gems"
type: read
function: http-request-dynamic
inputs:
  concurrent: true
  user_input:
    base_url: "https://rubygems.org/api/v1/search.json"
    pagination:
      name: page
      start: 1
      end: 5 
    params_fixed:
      - name: query
        value: '*'
```

## Simple Mapping Illustrations (corresponding to examples)
```
https://data.police.uk/api/crimes-street/all-crime?date=2021-11&lat=53.401&lng=-2.9
``` 
```
https://rubygems.org/api/v1/search.json?page=200&query=*
``` 
