| Features  | Description |
| ------------- | ------------- |
| **Pipeline Structure**  |
| [Overview](structures/overviews.md) | This is the overview structure of your yaml file. |
| [Stages](structures/stages.md) | This is the definition and usage of a stage. |
| [Tasks](structures/tasks.md)  | This is the definition and usage of a task. |
| **Functions** |
| **`Read Type Functions`** | 
| [http-request](types/read/http-request.md) | This function is used to call http request urls. |
| [http-request-dynamic](types/read/http-request-dynamic.md) | This function is used to call http request urls with several dynamic params. | 
| **`Filter Type Function`** |
| [xpath](types/filter/xpath.md) | This function is used for webscrapping tasks to do html/xml data filtering. | 
| [json-path](types/filter/json-path.md) | This function is used for api-requesting tasks to do json data filtering. | 
| [sql (filter)](types/filter/sql.md) | This function is used for tabular data filtering. | 
| **`Transform Type Function`** |
| [decompress](types/transform/decompress.md) | This function is used for decompressing gzip data and return the origin decompressed content. |
| [flatten-lists-to-dataframe](types/transform/flatten-lists-to-dataframe.md) | This function is used for flattening json-path return json lists to dataframe columns. |
| [json-array-to-dataframe](types/transform/json-array-to-dataframe.md) | This function is used for turning your json-array rows into a dataframe. |
| [rename-columns](types/transform/rename-columns.md) | This function is used for renaming your dataframe columns. |
| [sampling](types/transform/sampling.md) | This function is used for taking samples from dataframes. |
| [split-dataframe-rows](types/transform/split-dataframe-rows.md) | This function is used for turning your dataframe rows into list of dataframes. |
| [string-injecting](types/transform/string-injecting.md) | This function is used for replacing certain substring inside the other string. |
| [transform-to-dataframe](types/transform/transform-to-dataframe.md) | This function is used for turning your dataframe rows into list of dataframes. |
| [sub-selection](types/transform/sub-selection.md) | This function is used for doing sub-selection of your original upstream task input. | 
| **`Merge Type Function`** |
| [sql (merge)](types/merge/sql.md) | This function is used for tabular data merging. |
| **`Concat Type Function`** |
| [concat](types/concat/concat.md) | This function is used for the last task in a stage for concating several dataframes' data into a big dataframe. |
