#!/usr/bin/env python

import argparse
from IPython import embed
from sika.task_bypass.pipeline import Pipeline
from sika.task_bypass.pipeline_syntax import PipelineSyntax
from sika.db.sql_db_handler import sql_db 
import sqlite3
import sys, yaml
import time
import os

def setting_args():
    parser = argparse.ArgumentParser(prog = 'sika', description = 'Build a simple pipeline by a yaml file')
    parser.add_argument('-i', '--input', help="put in an input yaml file path", type=str)
    parser.add_argument('-o', '--output', help="put a path for your output db", default='.', type=str)
    parser.add_argument('-r', '--restart', help="restart the whole pipeline again, delete all data tables in your db file", action='store_true')
    parser.add_argument('-int', '--interactive', help="put users into interactive mode when pipeline tasks finish", action='store_true')
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    return parser.parse_args()

def main():
    args = setting_args()
    
    start_time = time.time()
    yaml_file_name = args.input
    restart_flag = args.restart
    interactive_flag = args.interactive
    
    with open(yaml_file_name, "r") as stream:
        file = yaml.safe_load(stream)
        pipeline_syntax = PipelineSyntax(file)
        pipeline = pipeline_syntax.build_entity()
        _stages = pipeline.stages
    
    # Create your db connection.
    db_name = f'{pipeline.name}.db'
    if db_name in args.output:
        if os.path.isfile(args.output):
            db_path = args.output
    else:
        db_path = os.path.join(args.output, db_name)

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
    # Create pipeline status table for recording the most recent done stage
    pipeline_status_table_structure = """
                'done_stage' TEXT
                """
    db.createTable('_pipeline_status', pipeline_status_table_structure)

    # Check if users want to restart the whole pipeline
    stage_names = pipeline.stages.names()

    if restart_flag: # if restarting a previously stopped pipeline from beginning
        db.deleteRows('_pipeline_status')
        waited_stages = _stages
    else:            # if starting or continuing a new pipeline
        df = db.readTableToDf('_pipeline_status')
        done_stages = list(df['done_stage'])
        unexecute_stages = [stage_name for stage_name in stage_names if stage_name not in done_stages]
        waited_stages = [stage for stage in _stages if stage.name in unexecute_stages] 

    
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
    if waited_stages:
        final_df = pipeline.run(db, restart_flag)
    else:
        # read the last stage defined in the yaml file as the last output
        final_df = db.readTableToDf(stage_names[-1]) 
    
    duration = time.time() - start_time
    
    # get some information for the final df
    final_df.info()
    
    # can use .head to see some sample data
    # final_df.head()
    if interactive_flag:
        embed()

if __name__ == '__main__':
    main()
