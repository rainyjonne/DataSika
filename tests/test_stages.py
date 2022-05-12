# this is the acceptance test for a simple pipeline
from .handler import stages_handler
from . import DB 
import yaml
import pytest
import pandas as pd
import vcr



@vcr.use_cassette("tests/cassettes/test_stages.yml", record_mode="new_episodes")
def test_stages():
    with open('tests/test_yamls/test_run_stages.yml', "r") as stream:
        file = yaml.safe_load(stream)
        stages = file['pipeline']['stages']
        pipeline_name = file['name']

    params = (stages, pipeline_name, DB)
    final_df = stages_handler('run_stages', params) 

    compared_df = pd.read_csv('tests/test_csvs/outputs/run_stages.csv')

    # because api return different message in different calling times
    # so use columns & length to do the test
    assert list(final_df.columns) == list(compared_df.columns)
    assert len(final_df.index) == len(compared_df.index)

