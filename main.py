#!/usr/bin/env python

from IPython import embed
import yaml
from task_bypass.allocate_stage_tasks import allocate_stage_tasks

with open("airbnb_pipeline.yaml", "r") as stream:
    process = yaml.safe_load(stream)


# get stages
stages = process['pipeline']['stages']

# test run
# test here
# each stage tasks can be output to a sqlite database
airbnb_stage_tasks = allocate_stage_tasks(stages[0]['tasks'][0:9])
covid_stage_tasks = allocate_stage_tasks(stages[1]['tasks'][0:3])
airbnb_stage_tasks.update(covid_stage_tasks)
merge_stage_tasks = allocate_stage_tasks(stages[2]['tasks'][0:3], airbnb_stage_tasks)
embed()
# show the results
# merge_stage_tasks['filter_nan_rows']