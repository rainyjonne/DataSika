from sika.task_bypass.tasktypes.merge.sql_merge import sql_merge
from sika.task_bypass.helpers import merge_sanity_check


def merge_tasks(db, stage_name, task_id, task_inputs, done_tasks, syntax):
    # pick out those needed stage first
    needed_done_tasks = {}
    for input in task_inputs:
        _from = input['from']
        done_task = {_from: done_tasks[_from]}
        needed_done_tasks.update(done_task)
    
    # check if all the done task output have same length (sanity check)
    merge_sanity_check(needed_done_tasks)
    
    # zip dictionary of lists into list of dictionaries
    zipped_dicts = [dict(zip(needed_done_tasks, t)) for t in zip(*needed_done_tasks.values())]
    
    # do the merged job
    result_lists = []
    for _dict in zipped_dicts:
        merged_df = sql_merge(_dict, syntax)
        result_lists.append(merged_df)
        


    return {
        task_id: result_lists
    }

