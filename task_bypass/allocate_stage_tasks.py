# stage(tasks) function 
from itertools import cycle
from task_bypass.categorize_task import categorize_task

def allocate_stage_tasks(tasks):
    tasks_cycle= cycle(tasks)
    global done_tasks
    done_tasks = {}
    # might be better way in the future
    # using a while loop to keep tracking if the tasks are done or not
    while(tasks):
        task = next(tasks_cycle)
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
                    _from_output = done_tasks[_from]['result']
                    _output_name = done_tasks[_from]['name']
                    # check the input matches the output of last task
                    if task_inputs[0]['type'] == type(_from_output).__name__.lower():
                        done_task = categorize_task(task, _from_output, _output_name)
                        done_tasks.update(done_task)
                        tasks.remove(task)
                        tasks_cycle= cycle(tasks)
                    else:
                        print("output type not right")
                        print("here are the tasks that have been done:")
                        # return done_tasks
                else:
                    continue
            else:
                # do something for merging stage
                continue
    print("========================================")
    print("tasks that have done:")
    print("-----------------------------------------------------------------")
    print(done_tasks)
    print("========================================")
    print("the last output:")
    print("-----------------------------------------------------------------")
    
    return done_task
