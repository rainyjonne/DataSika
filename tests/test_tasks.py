# this is the integration test for some sample tasks
# 
from .handler import tasks_handler
from . import configure
import yaml
import pytest
import pandas as pd
import vcr

db = configure()

def task_setup():
    with open('tests/test_yamls/test_run_tasks.yml', "r") as stream:
        file = yaml.safe_load(stream)
        stages = file['stages']

    tasks_infos = []
    file_idx = 1
    for stage in stages:
        stage_name = stage['id']
        tasks = stage['tasks']
        output_path = stage['output_path']
        output_df = pd.read_csv(output_path)
        tasks_infos.append((stage_name, tasks, db, output_df, file_idx))
        file_idx = file_idx + 1

    return tasks_infos
    
    

@pytest.mark.parametrize("stage_name, tasks, db, output_df, file_idx", task_setup())
@vcr.use_cassette("tests/cassettes/test_tasks.yml", record_mode="new_episodes")
def test_tasks(stage_name, tasks, db, output_df, file_idx):

    params = (stage_name, tasks, db)
    final_df = tasks_handler('allocate_stage_tasks', params) 

    # need to output to csv then read back because it will cause different length...
    # very strange bug... (can reproduce this bug by comment these three lines)
    compared_file_path = f'tests/test_csvs/outputs/run_tasks_compared_{file_idx}.csv'
    final_df.to_csv(compared_file_path, index=False) 
    final_df = pd.read_csv(compared_file_path)

    # because api return different message in different calling times
    # so use columns & length to do the test
    assert list(final_df.columns) == list(output_df.columns)
    assert len(final_df.reset_index().index) == len(output_df.reset_index().index)

