# xpath 
- xpath function is used for filtering **html/xml data** which comes from **webscrapping tasks**.
- For using xpath function:
  - **field** is the only column that you need to fill in under the `user_input` section. You should **specify your syntax** in here, under the `user_input` section.
- Resources
  - [Simple XPath tutorial](https://www.w3schools.com/xml/xpath_syntax.asp)
  - [Free Online Testing Tool](https://www.toolnb.com/tools/xpath.html): You can test the requesting link and your syntax here.


## Function Syntax
```yml
id: <task name (identical) (required)>
description: <task description (optional)>
type: filter 
function: xpath 
inputs:
  user_inputs:
    field: <xpath syntax>
  task_inputs(optional)/stage_inputs(optional):
    - from: <upstream task_id (required)>/<upstream stage_id (required)>
      ...
```

## An Example
```yml 
id: extract_content
description: "get file links by xpath syntax"
type: filter
function: xpath
inputs:
  user_input:
    field: "//a[contains(@href, 'listings.csv.gz')][contains(@href, 'http')][contains(@href, 'united-kingdom')]/@href"
  task_inputs:
    - from: webscrap_airbnb
```
