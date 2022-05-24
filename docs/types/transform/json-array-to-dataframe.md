# json-array-to-dataframe 
- json-array-to-dataframe function is used for **turning your json-array rows (which often produced by json-path tasks) into a dataframe**.
  - e.g. You have 3 input rows of data: ['John', 'male', 24], ['May', 'female', 18], ['Karen', 'female', 27] -> it will returns as a dataframe with your feed in **ordered headers** 
- For function usage:
  - **headers** is a series of **ordered headers** that will become your dataframe column names. The order **must match the order that you used in your upstream json-path task**.
  - **NOTE: headers content should be like this: `'["<column_name>"]'`, instead of this: `"['<column_name>']"`** 

# Function Syntax
```yml
id: <task name (identical) (required)>
description: <task description (optional)>
type: transform 
function: json-array-to-dataframe 
inputs:
  stage_inputs/task_inputs:
    - from: <upstream stage id (required)>/<upstream task id (required)> 
      headers: <the ordered headers> 
```

# An Example
```yml
id: read_json_path_str_to_table
description: "read json str to dataframe"
type: transform
function: json-array-to-dataframe
inputs:
  task_inputs:
    - headers:  '["gem_name", "downloads", "version", "version_downloads", "platform", "authors", "info", "licenses", "metadata", "sha", "project_uri", "gem_uri", "homepage_uri", "wiki_uri", "documentation_uri", "mailing_list_uri", "source_code_uri", "bug_tracker_uri", "changelog_uri"]'
      from: filter_gem_infos
``` 
