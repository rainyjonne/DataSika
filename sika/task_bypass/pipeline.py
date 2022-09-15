# stages function
from itertools import cycle
from functools import reduce
import sqlite3
from sika.task_bypass.stage import Stage

class Pipeline:
    def __init__(self, name, stages):
        self.name = name
        self.stages = stages

    def run(self, db, restart_flag = False, waited_stages = None):
        # if there are waited stages (not-done stages)
        # then change pipeline's initial stages (all stages) to waited stages
        if waited_stages:
            self.stages = waited_stages

        if restart_flag:
            stage_names = self.stages.names()
            for stage_name in stage_names:
                db.dropTable(stage_name)

        # Main stages loop - might be better way in the future (e.g. parallelisim)
        last_stage = self.stages.run(db)

        return last_stage

    def gather_last_result(self, db):
        # gather the last stage's dataframe of last time's pipeline execution
        stage_names = self.stages.names
        final_df = db.readTableToDf(stage_names[-1])

        return final_df 
