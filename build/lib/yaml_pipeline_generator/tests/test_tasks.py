# this is the integration test for some sample tasks
# 
from .handler import tasks_handler
from . import DB 
import yaml
import pytest
import pandas as pd
import vcr


@vcr.use_cassette("tests/cassettes/test_tasks.yml", record_mode="new_episodes")
def test_tasks():
    with open('tests/test_yamls/test_run_tasks.yml', "r") as stream:
        file = yaml.safe_load(stream)
        stage_name = file['id']
        tasks = file['tasks']

    params = (stage_name, tasks, DB)
    final_df = tasks_handler('allocate_stage_tasks', params) 
    compared_df = pd.read_csv('tests/test_csvs/outputs/run_tasks.csv')

    # because api return different message in different calling times
    # so use columns & length to do the test
    assert list(final_df.columns) == list(compared_df.columns)
    assert len(final_df.index) == len(compared_df.index)

