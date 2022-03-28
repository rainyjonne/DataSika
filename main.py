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
done_tasks = allocate_stage_tasks(stages[0]['tasks'][0:9])
embed()
