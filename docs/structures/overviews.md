# Define a whole yaml file for your data pipeline
- Here is the simple overview structure for you to design the whole data pipeline in your yaml file.
- The pipeline name will also become your output sqlite's file name.
- For more details, please refer to [Stages](stages.md) and [Tasks](tasks.md).

## Structure Syntax
```
name: <pipeline name>
pipeline:
  stages:
    - id: <stage name>
      description: <stage description>
      tasks:
        - id: <task name>
          description: <task description>
          type: <task type>
          function: <task function>
          inputs:
            ... 
```

## An Example
```
name: airbnb_uk_crime
pipeline:
  stages:
    - id: get_uk_airbnb_data 
      description: getting airbnb host listing data of uk 
      tasks:
        - id: webscrap_airbnb 
          description: a airbnb webscrap task
          type: read
          function: http-request 
          inputs:
            ... 
```
