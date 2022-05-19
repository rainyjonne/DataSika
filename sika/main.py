#!/usr/bin/env python

import argparse
from IPython import embed
from sika.task_bypass.run_stages import run_stages 
from sika.task_bypass.allocate_stage_tasks import allocate_stage_tasks 
from sika.db.sql_db_handler import sql_db 
import sqlite3
import sys, yaml
import time
import os

def setting_args():
    parser = argparse.ArgumentParser(prog = 'sika', description = 'Build a simple pipeline by a yaml file')
    parser.add_argument('--input', help="put in an input yaml file path", type=str)
    parser.add_argument('--output', help="put a path for your output db", default='.', type=str)
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
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
    db_path = os.path.join(args.output, f'{pipeline_name}.db') 
    db = sql_db(db_path)
    # Create logging table for tasks
    task_logging_table_structure = """
                'level' TEXT NOT NULL,
                'stage_name' TEXT NOT NULL,
                'task_name' TEXT NOT NULL,
                'task_type' TEXT NOT NULL,
                'task_function' TEXT NOT NULL,
                'output_nums' INTEGER NOT NULL,
                'columns' TEXT NOT NULL,
                'row_nums' TEXT NOT NULL,
                'date_time' TEXT NOT NULL,
                'error_message' TEXT,
                'other_info' TEXT
                """
    db.createTable('_task_log', task_logging_table_structure) 
    # Create logging table for http requests
    request_logging_table_structure = """
                'level' TEXT NOT NULL,
                'status_code' INTEGER NOT NULL,
                'stage_name' TEXT NOT NULL,
                'task_name' TEXT NOT NULL,
                'base_url' TEXT NOT NULL,
                'date_time' TEXT NOT NULL,
                'error_message' TEXT,
                'other_info' TEXT
                """
    db.createTable('_request_log', request_logging_table_structure) 
    
    
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

if __name__ == '__main__':
    main()
