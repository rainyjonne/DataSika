# json-path 
- json-path function is used for filtering **json data** which comes from **API calling tasks**.
- For using json-path function:
  - **field** is the only column that you need to fill in under `user_input` section. You should **specify your syntax** in here, under the `user_input` section.
- Resources
  - [Simple JsonPath tutorial](https://support.smartbear.com/alertsite/docs/monitors/api/endpoint/jsonpath.html)
  - [Free Online Testing Tool](https://codebeautify.org/jsonpath-tester): You can test the requesting link and your syntax here.
  - **NOTE: Sika uses jsonpath-ng as its json-path supporting pacakge, so there are some syntaxes might be different to the online tool. For example, getting length you should use '$.`len`' in your yaml file while you use '$.length' in the online testing website.**


## Function Syntax
```yml
id: <task name (identical) (required)>
description: <task description (optional)>
type: filter 
function: json-path 
inputs:
  user_inputs:
    field: <json-path syntax>
  task_inputs(optional)/stage_inputs(optional):
    - from: <upstream task_id (required)>/<upstream stage_id (required)>
      ...
```

## Examples
```yml
id: getting_crime_numbers
description: "get crime statistic data"
type: filter 
function: json-path 
inputs:
  user_input:
    field: '$.`len`' 
  task_inputs:
    - from: request_uk_crime_data
      extract_field: text
      preserve_origin_data: true
```

```yml
id: filter_gem_names
description: "using jsonpath to filter out gem names"
type: filter
function: json-path 
inputs:
  user_input:
    field: '$..name' 
  task_inputs:
    - from: get_gem_basic_infos 
      extract_field: text
```

```yml
id: filter_gem_infos  
description: "get gem_infos"
type: filter 
function: json-path 
inputs:
  user_input:
    field: '$["name", "downloads", "version", "version_downloads", "platform", "authors", "info", "licenses", "metadata", "sha", "project_uri", "gem_uri", "homepage_uri", "wiki_uri", "documentation_uri", "mailing_list_uri", "source_code_uri", "bug_tracker_uri", "changelog_uri"]' 
  stage_inputs:
    - from: call_gem_api_stage 
      extract_field: body
```
