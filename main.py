#!/usr/bin/env python

from IPython import embed
from task_bypass.run_stages import run_stages 
import yaml

with open("pipeline_syntax.yaml", "r") as stream:
    file = yaml.safe_load(stream)
    my_stages = file['pipeline']['stages']
    pipeline_name = file['name']

# get stages
final_output = run_stages(my_stages, pipeline_name)

embed()
# show the results
# final_output['concat_final_dataframes'][0]
