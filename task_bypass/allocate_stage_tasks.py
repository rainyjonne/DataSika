# stage(tasks) function 
from itertools import cycle
from task_bypass.categorize_task import categorize_task
from task_bypass.merge_tasks import merge_tasks
from task_bypass.helpers import task_length_sanity_check, concat_task_length_sanity_check, split_task_length_sanity_check

#NEW
# stage(tasks) function 
from itertools import cycle
from IPython import embed

def allocate_stage_tasks(tasks, done_tasks={}):
    tasks_cycle= cycle(tasks)
    # this is for testing
    # might be better way in the future
    # using a while loop to keep tracking if the tasks are done or not
    while(tasks):
        task = next(tasks_cycle)
        print(f"{task['id']} task starts!")
        # check if it's the first task
        if 'task_inputs' not in task['inputs']:
            done_task = categorize_task(task)
            # update the done task list
            done_tasks.update(done_task)
            # remove the tasks that are waiting to be done
            tasks.remove(task)
            tasks_cycle= cycle(tasks)
        else:
            task_inputs = task['inputs']['task_inputs']
            # if task inputs > 1, that means a merge type of task will happen
            if len(task_inputs) == 1:
                _from = task_inputs[0]['from']
                if _from in done_tasks:
                    _from_output = done_tasks[_from]
                    done_task = categorize_task(task, _from_output, _from)
                    # do sanity check
                    #NOTE: split & concat function has its own sanity check
                    if task['function'] == 'split_dataframe_rows':
                        pass
                    elif task['function'] == 'concat':
                        concat_task_length_sanity_check(done_task, task['id'])
                    else:
                        task_length_sanity_check(_from_output, done_task, task['id'])
                    done_tasks.update(done_task)
                    tasks.remove(task)
                    tasks_cycle= cycle(tasks)
                else:
                    continue

            else:
                # do something for merging stage
                done_task = merge_tasks(task['id'], task_inputs, done_tasks, task['inputs']['user_input']['field'])
                done_tasks.update(done_task)
                tasks.remove(task)
                tasks_cycle= cycle(tasks)
        print(f"{task['id']} task has done!")
    #print("========================================")
    #print("tasks that have done:")
    #print("-----------------------------------------------------------------")
    #print(done_tasks)
    #print("========================================")
    #print("the last output:")
    #print("-----------------------------------------------------------------")

    return done_task
