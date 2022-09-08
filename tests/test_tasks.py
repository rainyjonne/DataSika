# this is the integration test for some sample tasks
# 
from .handler import tasks_handler
from . import DB 
import yaml
import pytest
import pandas as pd
import vcr
from sika.task_bypass.stage import Stage


@vcr.use_cassette("tests/cassettes/test_tasks.yml", record_mode="new_episodes")
def test_tasks():
    with open('tests/test_yamls/test_run_tasks.yml', "r") as stream:
        file = yaml.safe_load(stream)
        stage = Stage(file)

    # modify tasks_handler test (instead of call a function, use obj as send in param to run the function of the object
    final_df = tasks_handler(stage, DB) 
    compared_df = pd.read_csv('tests/test_csvs/outputs/run_tasks.csv')

    # because api return different message in different calling times
    # so use columns & length to do the test
    assert list(final_df.columns) == list(compared_df.columns)
    assert len(final_df.index) == len(compared_df.index)

