import sqlite3 
from IPython import embed
import os
import logging
import pandas as pd
logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG)

class sql_db:
    def __init__(self, databaseName):
      #  try:
      #      path = f"../{folderName}"
      #      logging.info(path)
      #      if not os.path.isdir(path):
      #          os.mkdir(path)
      #          logging.info(f"mkdir {path} successfully")
        try:
            self.conn = sqlite3.connect(databaseName, timeout=10)
            self.c = self.conn.cursor()
            logging.info("Opened database successfully")
        except Exception as e:
            logging.warning(f"Opened database Failed! Error message: {e}")
      #  except:
      #      logging.error("mkdir Failed. Do you remember import os?")

    def returnConnection(self):
        return self.conn

    def createTable(self, tableName, tableStructure):
        try:
            self.c.execute(f"CREATE TABLE IF NOT EXISTS {tableName} ({tableStructure});")
            logging.info("Table created successfully")
            return 1
        except Exception as e:
            logging.info(f"CreateTable Error! Error message: {e}")
            return 0

    def insert(self, tableName, question_marks, replace_content):
        self.dbsql = f"INSERT INTO {tableName} VALUES ({question_marks})"
        logging.info(f"DB sql: {self.dbsql} & {replace_content}")
        self.c.execute(self.dbsql, replace_content)
        result = self.conn.commit()
        return result

    def readTableToDf(self, tableName):
        self.dbsql = f"SELECT * FROM {tableName}"
        logging.info(f"GETTING STAGE DATA FROM - {tableName}")
        query = self.conn.execute(self.dbsql)
        cols = [column[0] for column in query.description]
        results = pd.DataFrame.from_records(data = query.fetchall(), columns = cols)
        return results

    def checkEmpty(self, tableName):
        # check if the table is empty or not
        self.dbsql = f"SELECT count(*) from {tableName}"
        self.c.execute(self.dbsql)
        result = self.conn.commit()
        if result != 0:
            return False
        else:
            return True

    def checkStatusRecordExist(self, stageName): 
        # check if the status exists or not 
        self.dbsql = "SELECT count(*) FROM _pipeline_status WHERE done_stage = ?"
        self.c.execute(self.dbsql, (stageName,))
        result,  = self.c.fetchall()[0]
        if result == 0:
            return False 
        else:
            return True 

    # only for update pipeline status
    def updatePipelineStatus(self, stageName):
        try:
            # if the table is empty then insert one none record
            if not self.checkStatusRecordExist(stageName):
                self.insert('_pipeline_status', "?", (stageName, ))
                logging.info(f"Update Pipeline Status - {stageName}")
        except Exception as e:
            logging.info(f"Update Pipeline Status Error! Error message: {e}")
            return 0

    def deleteRows(self, tableName):
        self.dbsql = f"DELETE FROM {tableName}"
        logging.info(f"DELETE ROWS FROM - {tableName}")
        try:
            self.c.execute(self.dbsql)
            self.conn.commit()
            return 1 
        except Exception as e:
            logging.info(f"Delete Table Rows Error! Error message: {e}")
            return 0

    def dropTable(self, tableName):
        try:
            self.c.execute(f"DROP TABLE IF EXISTS {tableName}")
            logging.info(f"DROP EXISTING TABLE - {tableName}")
            return 1
        except Exception as e:
            logging.info(f"DropTable Error! Error message: {e}")
            return 0

    def dropAllTables(self):
        # get all tables
        self.c.execute("SELECT name FROM sqlite_schema WHERE type='table';")
        tables = self.c.fetchall()
        for (table, ) in tables:
            self.c.execute(f"DROP TABLE IF EXISTS {table}")
            
