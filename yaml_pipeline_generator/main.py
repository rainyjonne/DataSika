#!/usr/bin/env python

import argparse
from IPython import embed
from yaml_pipeline_generator.task_bypass.run_stages import run_stages 
from yaml_pipeline_generator.task_bypass.allocate_stage_tasks import allocate_stage_tasks 
from yaml_pipeline_generator.db.sql_db_handler import sql_db 
import sqlite3
import sys, yaml
import time

def setting_args():
    parser = argparse.ArgumentParser(prog = 'yaml-pipeline-generator', description = 'Build a simple pipeline by a yaml file')
    parser.add_argument('--input', help="put in an input yaml file path", type=str) 
    return parser.parse_args()

def main():
    args = setting_args()
    
    start_time = time.time()
    yaml_file_name = args.input
    
    with open(yaml_file_name, "r") as stream:
        file = yaml.safe_load(stream)
        my_stages = file['pipeline']['stages']
        pipeline_name = file['name']
    
    # Create your db connection.
    db = sql_db(f'yaml_pipeline_generator/db/outputs/{pipeline_name}.db')
    table_structure = """
                'level' TEXT NOT NULL,
                'stage_name' TEXT NOT NULL,
                'task_name' TEXT NOT NULL,
                'date_time' TEXT NOT NULL,
                'error_message' TEXT,
                'other_info' TEXT
                """
    # Create logging table
    db.createTable('_log', table_structure) 
    
    
    # get stages
    final_output = run_stages(my_stages, pipeline_name, db)
    
    duration = time.time() - start_time
    
    # get final_df
    final_df = list(final_output.values())[0][0]
    
    # get some information for the final df
    final_df.info()
    
    # can use .head to see some sample data
    # final_df.head()
    embed()
    # show the results
    # final_output['concat_final_dataframes'][0]
