# stages function
from itertools import cycle
from functools import reduce
import sqlite3
from sika.task_bypass.allocate_stage_tasks import allocate_stage_tasks


def run_stages(stages, pipeline_name, db, rerun_flag = False, done_stages={}):
    if rerun_flag:
        stage_names = [ stage['id'] for stage in stages ]
        for stage_name in stage_names:
            db.dropTable(stage_name)
    stages_cycle = cycle(stages)
    # this is for testing
    # might be better way in the future (e.g. parallelisim)
    # using a while loop to keep tracking if the stages are done or not
    while(stages):
        stage = next(stages_cycle)
        # check if it has something input from another stage
        if 'from' in stage:
            upstream_stages = stage['from']
            # if it's a merge stage
            if len(upstream_stages) > 1:
                done_stage = allocate_stage_tasks(stage['id'], stage['tasks'], db)
                # save dataframe to sqlite db
                list(done_stage.values())[0][0].to_sql(name=stage['id'], con=db.returnConnection())
                # update the done stage list
                done_stages.update({stage['id']: done_stage})
                stages.remove(stage)
                stages_cycle = cycle(stages)

            # if user wants to cut tasks into smaller stages
            # need to add more codes to here in the future
            else:
                done_stage = allocate_stage_tasks(stage['id'],stage['tasks'], db)
                # save dataframe to sqlite db
                list(done_stage.values())[0][0].to_sql(name=stage['id'], con=db.returnConnection())
                done_stages.update({stage['id']: done_stage})
                stages.remove(stage)
                stages_cycle = cycle(stages)
        else:
            # update the done stage list
            done_stage = allocate_stage_tasks(stage['id'], stage['tasks'], db)
            # save dataframe to sqlite db
            list(done_stage.values())[0][0].to_sql(name=stage['id'], con=db.returnConnection())
            done_stages.update({stage['id']: done_stage})
            stages.remove(stage)
            stages_cycle = cycle(stages)

        # record done stage
        db.updatePipelineStatus(stage['id'])

    # return last stage's output
    return done_stage
