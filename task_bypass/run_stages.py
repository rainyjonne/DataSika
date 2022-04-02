# stages function
from itertools import cycle
from functools import reduce
from task_bypass.allocate_stage_tasks import allocate_stage_tasks


def run_stages(stages, done_stages={}):
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
                unmerged_stages = list(map(lambda key: done_stages[key] if key in upstream_stages else None, done_stages))
                if None in unmerged_stages: unmerged_stages.remove(None)
                from_tasks = reduce(lambda a, b: {**a, **b}, unmerged_stages)
                done_stage = allocate_stage_tasks(stage['tasks'], from_tasks)
                # update the done stage list
                done_stages.update({stage['id']: done_stage})
                # remove done stage from waiting list
                stages.remove(stage)
                stages_cycle = cycle(stages)

            # if user wants to cut task into smaller stages
            # need to add more codes to here in the future
            else:
                continue

        else:
            # update the done stage list
            done_stage = allocate_stage_tasks(stage['tasks'])
            # update the done stage list
            done_stages.update({stage['id']: done_stage})
            # remove done stage from waiting list
            stages.remove(stage)
            stages_cycle = cycle(stages)

    # return last stage's output
    return done_stage
