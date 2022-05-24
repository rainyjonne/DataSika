# sql (filter) 
- sql (filter) function is used for filtering **tabular data**, such as **pandas dataframes**.
- For using sql function:
  - **field** is the only column that you need to fill in under `user_input` section. You should **specify your syntax** in here, under the `user_input` section.
  - **NOTE: The table name for the SQL Query's `FROM` statement should be the upstream task/stage id.**
- Resources
  - [SQL Query Tutorial](https://www.w3schools.com/sql/)
  - [SQL Online IDE](https://sqliteonline.com/): You can click on the `File` button on the left up corner, then import your sqlite file in for playground testings.
    - [Load your DB file](images/load_db.jpg)
    - [Play SQL Query with your data](images/sqlite_playground.jpg)

## Function Syntax
```yml
id: <task name (identical) (required)>
description: <task description (optional)>
type: filter 
function: sql 
inputs:
  user_inputs:
    field: <sql syntax>
  task_inputs/stage_inputs:
    - from: <upstream task_id (required)>/<stage_id (required)>
      ...
```

## Examples
```yml
id: transform_license
description: "transform license format"
type: filter 
function: sql 
inputs:
  user_input:
    field: "
      SELECT *, REPLACE(REPLACE(REPLACE(licenses, '[', ''), ']', ''), ' ' ,'') as licenses_transformed 
      FROM read_json_path_str_to_table 
    "
  task_inputs:
    - from: read_json_path_str_to_table 
```

```yml
id: transform_price
description: "transform price"
type: filter
function: sql
inputs:
  user_input:
    field: "
      SELECT `id`, `listing_url`, `host_location`, `name`, `unavailability_30`, `latitude`, `longitude`,
      CAST(REPLACE(REPLACE(REPLACE(price, '$', ''), '.00', ''), ',' ,'') AS INT) as price,
      `number_of_reviews`, `review_scores_rating`, `review_scores_accuracy`, `review_scores_cleanliness`, 
      `review_scores_checkin`, `review_scores_communication`, `review_scores_location`,
      `review_scores_value`, `crime_incidents`
      FROM combine_airbnb_crime_data
      "
  task_inputs:
    - from: combine_airbnb_crime_data
```

```yml
- id: filter_transform_listing
  description: "filter & transform fields by sql syntax"
  type: filter
  function: sql
  inputs:
    user_input:
      field: "
        SELECT
        `id`, `listing_url`, `host_location`, `name`, `latitude`, `longitude`, `price`, `number_of_reviews`, 
        `review_scores_rating`, `review_scores_accuracy`, `review_scores_cleanliness`, 
        `review_scores_checkin`, `review_scores_communication`, `review_scores_location`,
        `review_scores_value`,  (30-availability_30) as unavailability_30, 1 as key
        FROM read_csv_str_to_table
        WHERE has_availability = 't' 
        AND ((90-availability_90) != 90 OR (365-availability_365) != 365)
        "
    task_inputs:
      - from: read_csv_str_to_table
- id: filter_nan_rows
  description: "filter NaN rows"
  type: filter
  function: sql
  inputs:
    user_input:
      field: "
        SELECT *
        FROM filter_transform_listing
        WHERE `unavailability_30` IS NOT NULL AND `latitude` IS NOT NULL AND `longitude` IS NOT NULL AND
        `number_of_reviews` IS NOT NULL AND `review_scores_rating` IS NOT NULL AND `review_scores_accuracy` IS NOT NULL AND 
        `review_scores_cleanliness` IS NOT NULL AND `review_scores_checkin` IS NOT NULL AND `review_scores_communication` IS NOT NULL AND 
        `review_scores_location` IS NOT NULL AND `review_scores_value` IS NOT NULL AND `price` IS NOT NULL;
        "
    task_inputs:
      - from: filter_transform_listing
```
