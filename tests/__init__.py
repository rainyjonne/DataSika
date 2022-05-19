from sika.db.sql_db_handler import sql_db 


def configure():
    # Create your db connection.
    db = sql_db(f'sika/db/test.db')
    # Drop tables inside test db
    db.dropAllTables()
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

    return db


DB = configure() 
