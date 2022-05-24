# string-injecting 
- string-injecting function is used for **replacing certain substring inside the other string**.
- For function usage:
  - **base_str** is the string that has some `sub string` waiting for injection, the part that would be injected by other strings please surround them with **`[]`**
    - e.g. `My favorite fruit is [fav_fruit]` (will be injected with `mango`)
  - **inject_str**
    - **name** is the sub-string that would be replaced, for the example above, it would be `fav_fruit`
    - **value** is the sub-string that would be injected, for the example above, it would be `mango` 


# Function Syntax
```yml
id: <task name (identical) (required)>
description: <task description (optional)>
type: transform 
function: string-injecting 
inputs:
  user_input:
    base_str: <the string that has some part waiting for injection>
    inject_str:
      - name: <the sub-string that would be replaced>
        value: <the sub-string that will replace the original sub-string>
  stage_inputs/task_inputs:
    - from: <upstream stage id (required)>/<upstream task id (required)> 
```

# An Example
```yml
id: replace_gem_name_in_apis  
description: "replace text(gem name) inside another text(base url)"
type: transform
function: string-injecting 
inputs:
  user_input:
    base_str: "https://rubygems.org/api/v1/gems/[gem_name].json"
    inject_str:
      - name: gem_name 
        value: gem_names
  stage_inputs:
    - from: get_gems_stage 
```
