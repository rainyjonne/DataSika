# stages function
from itertools import cycle
from functools import reduce
import sqlite3
from sika.task_bypass.allocate_stage_tasks import allocate_stage_tasks
from sika.task_bypass.stage import Stage


# REFACTOR TODO: make a Stage class: (1) execute stage (2) find last output of stage (...)

# execute any particular stage
def run_stage(stage, db):
    done_stage = allocate_stage_tasks(stage, db)
    # save dataframe to sqlite db
    list(done_stage.values())[0][0].to_sql(name=stage['id'], con=db.returnConnection())
    # update the done stage list
    return done_stage

def run_pipeline(stages, pipeline_name, db, restart_flag = False, done_stages={}):
    if restart_flag:
        stage_names = [ stage['id'] for stage in stages ]
        for stage_name in stage_names:
            db.dropTable(stage_name)

    # Main stages loop - might be better way in the future (e.g. parallelisim)
    for stage_dict in stages:
        stage = Stage(stage_dict)

        # check if it has something input from another stage
        if stage.has_antecedent():
            upstream_stages = stage.antecedents()
            
            # if it's a merge stage
            if len(upstream_stages) > 1:
                done_stage = run_stage(stage.stage_dict, db)

            # if user wants to cut tasks into smaller stages
            # need to add more codes to here in the future
            else:
                done_stage = run_stage(stage.stage_dict, db)
        else:
            done_stage = run_stage(stage.stage_dict, db)

        done_stages.update({stage.name(): done_stage})

        # record done stage
        db.updatePipelineStatus(stage.name())

    # return last stage's output
    return done_stage
