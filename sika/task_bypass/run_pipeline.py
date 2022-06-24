# stages function
from itertools import cycle
from functools import reduce
import sqlite3
from sika.task_bypass.stage import Stage

# TODO: Refactor to make a Pipeline class?

def run_pipeline(stages, pipeline_name, db, restart_flag = False):
    if restart_flag:
        stage_names = [ stage['id'] for stage in stages ]
        for stage_name in stage_names:
            db.dropTable(stage_name)

    # Main stages loop - might be better way in the future (e.g. parallelisim)
    for stage_dict in stages:
        stage = Stage(stage_dict)

        # TODO NEXT: See if all these commented lines are needed for any of the tests
        
        # # check if it has something input from another stage
        # if stage.has_antecedent():
        #     upstream_stages = stage.antecedents()
            
        #     # if it's a merge stage
        #     if len(upstream_stages) > 1:
        #         done_stage = stage.run(db)

        #     # if user wants to cut tasks into smaller stages
        #     # need to add more codes to here in the future
        #     else:
        #         done_stage = stage.run(db)
        # else:
        #     done_stage = stage.run(db)
        done_stage = stage.run(db)

        # done_stages.update({stage.name(): done_stage})

        # record done stage
        db.updatePipelineStatus(stage.name())

    # return last stage's output
    return done_stage
