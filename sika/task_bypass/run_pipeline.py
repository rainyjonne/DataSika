# stages function
from itertools import cycle
from functools import reduce
import sqlite3
from sika.task_bypass.stage import Stage

# TODO: Refactor to make a Pipeline class?

def run_pipeline(stages, pipeline_name, db, restart_flag = False):
    if restart_flag:
        stage_names = stages.names()
        for stage_name in stage_names:
            db.dropTable(stage_name)

    # Main stages loop - might be better way in the future (e.g. parallelisim)
    for stage in stages.stages:

        done_stage = stage.run(db)

        # record done stage
        db.updatePipelineStatus(stage.name())

    # return last stage's output
    return done_stage
