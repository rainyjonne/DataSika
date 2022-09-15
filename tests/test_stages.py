# this is the acceptance test for a simple pipeline
from . import DB 
import yaml
import pytest
import pandas as pd
import vcr
from sika.task_bypass.pipeline import Pipeline
from sika.task_bypass.pipeline_syntax import PipelineSyntax

@vcr.use_cassette("tests/cassettes/test_stages.yml", record_mode="new_episodes")
def test_stages():
    with open('tests/test_yamls/test_run_stages.yml', "r") as stream:
        file = yaml.safe_load(stream)
        pipeline_syntax = PipelineSyntax(file)
        pipeline = pipeline_syntax.build_entity()
        stages = pipeline.stages
        pipeline_name = pipeline.name

    final_df = pipeline.run(DB)

    compared_df = pd.read_csv('tests/test_csvs/outputs/run_stages.csv')

    # because api return different message in different calling times
    # so use columns & length to do the test
    assert list(final_df.columns) == list(compared_df.columns)
    #NOTE: not sure what kind of tests suit this situation the bests
    # casue each page shows 30 records before, so I tried to compare the number of the output
    # but ruby website turn showing records to 34, which resulting in errors
    # assert len(final_df.index) == len(compared_df.index)

