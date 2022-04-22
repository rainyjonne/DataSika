#!/usr/bin/env python

from IPython import embed
from task_bypass.run_stages import run_stages 
from task_bypass.run_stages import allocate_stage_tasks 
from sql_db_handler import sql_db 
import sqlite3
import sys, yaml

yaml_file_name = sys.argv[1]

with open(yaml_file_name, "r") as stream:
    file = yaml.safe_load(stream)
    my_stages = file['pipeline']['stages']
    pipeline_name = file['name']

# Create your db connection.
db = sql_db(f'{pipeline_name}.db')
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
#final_output = run_stages(my_stages, pipeline_name, db)
final_output = allocate_stage_tasks(my_stages[0]['id'], my_stages[0]['tasks'], db)


embed()
# show the results
# final_output['concat_final_dataframes'][0]
