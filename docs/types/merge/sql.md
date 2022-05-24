# sql (merge) 
- sql (merge) function is used for merging **tabular data**, such as **pandas dataframes**.
- For using sql function:
  - **field** is the only column that you need to fill in under the `user_input` section. You should **specify your syntax** in here, under the `user_input` section.
- Other notes:
  - **stage_inputs** are required for **grabbing different stage data** from upstreams, remember to specify those stage ids here. 
- Resources: you can see other supporting resource details from `sql (filter) document` [Ref](../../filter/sql.md)

## Function Syntax
```yml
id: <task name (identical) (required)>
description: <task description (optional)>
type: merge 
function: sql 
inputs:
  user_inputs:
    field: <sql syntax>
  stage_inputs:
    - from: <upstream stage_id (required)>
      ...
```

## Examples
```yml
id: combine_api_time_with_filtered_gem_data
description: "combined two data sources into a big dataframe"
type: merge
function: sql
inputs:
  user_input:
    field: "
      SELECT call_gem_api_stage.gem_name as gem_name,
      call_gem_api_stage.update_time as update_time,
      `downloads`, `version`, `version_downloads`,
      `platform`, `authors`, `info`,
      `licenses_transformed` as licenses, `metadata`,
      `sha`, `project_uri`, `gem_uri`, `homepage_uri`,
      `wiki_uri`, `documentation_uri`, `mailing_list_uri`,
      `source_code_uri`, `bug_tracker_uri`, `changelog_uri`
      FROM filter_gem_info_stage
      INNER JOIN  call_gem_api_stage
      ON (
      filter_gem_info_stage.gem_name = call_gem_api_stage.gem_name
      )
      "
  stage_inputs:
    - from: call_gem_api_stage 
    - from: filter_gem_info_stage
```

```yml
id: combine_airbnb_crime_data
description: "combined two data sources into a big dataframe"
type: merge
function: sql
inputs:
  user_input:
    field: "
      SELECT
      `id`, `listing_url`, `name`, `host_location`, airbnb_stage.latitude as `latitude`,
      airbnb_stage.longitude as `longitude`, `price`, `number_of_reviews`, 
      `review_scores_rating`, `review_scores_accuracy`, `review_scores_cleanliness`, 
      `review_scores_checkin`, `review_scores_communication`, `review_scores_location`, `review_scores_value`,
      `crime_incidents`, `unavailability_30`
      FROM airbnb_stage 
      INNER JOIN crime_stage
      ON (
      airbnb_stage.latitude = crime_stage.latitude
      AND
      airbnb_stage.longitude = crime_stage.longitude
      )
      "
  stage_inputs:
    - from: airbnb_stage 
    - from: crime_stage
```
