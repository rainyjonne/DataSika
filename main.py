#!/usr/bin/env python

from IPython import embed
from task_bypass.run_stages import run_stages 
import yaml

with open("airbnb_pipeline.yaml", "r") as stream:
    process = yaml.safe_load(stream)


# get stages
stages = process['pipeline']['stages']
final_output = run_stages(stages)

embed()
# show the results
# final_output['filter_nan_rows']
