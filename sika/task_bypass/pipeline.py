# stages function
from itertools import cycle
from functools import reduce
import sqlite3
from sika.task_bypass.stage import Stage

class Pipeline:
    def __init__(self, name, stages):
        self.name = name
        self.stages = stages

    def run(self, db, restart_flag = False):
        if restart_flag:
            stage_names = self.stages.names()
            for stage_name in stage_names:
                db.dropTable(stage_name)

        # Main stages loop - might be better way in the future (e.g. parallelisim)
        last_stage = self.stages.run(db)

        return last_stage
