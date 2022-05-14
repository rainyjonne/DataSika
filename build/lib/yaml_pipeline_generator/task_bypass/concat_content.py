## filter content based on user & task inputs
## NOTE: might need to think of some parrellal solutions for this function

import pandas as pd

## concat dataframes & store the result into sql file
## function variable is useless in concat case since we can use pandas package to handle this task

def concat_content(task_id, dataframes):
    final_df = pd.concat(dataframes)
    return {
        task_id: [final_df]
    }
