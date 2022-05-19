import sqlite3 

import os
import logging
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
            
