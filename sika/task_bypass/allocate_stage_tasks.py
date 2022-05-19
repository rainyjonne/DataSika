# stage(tasks) function 
from itertools import cycle
from sika.task_bypass.categorize_task import categorize_task
from sika.task_bypass.merge_tasks import merge_tasks
from sika.task_bypass.helpers import task_length_sanity_check, concat_task_length_sanity_check, split_task_length_sanity_check, logging_task_output_info

#NEW
# stage(tasks) function 
from itertools import cycle
from IPython import embed

def allocate_stage_tasks(stage_name, tasks, db, done_tasks={}):
    tasks_cycle= cycle(tasks)
    # this is for testing
    # might be better way in the future
    # using a while loop to keep tracking if the tasks are done or not
    while(tasks):
        task = next(tasks_cycle)
        print(f"{task['id']} task starts!")
        # default logging is true
        logging = True
        if 'logging' in task:
            logging = task['logging']

        # check if it's the first task of the pipeline
        if 'task_inputs' not in task['inputs'] and 'stage_inputs' not in task['inputs']:
            done_task = categorize_task(db, stage_name, task)
            # do the task logging (will do as default)
            if logging:
                logging_task_output_info(stage_name, task, done_task, db)
            # update the done task list
            done_tasks.update(done_task)
            # remove the tasks that are waiting to be done
            tasks.remove(task)
            tasks_cycle= cycle(tasks)
        # check if it's the first task of the stage
        elif 'stage_inputs' in task['inputs']:
            stage_inputs = task['inputs']['stage_inputs']
            if len(stage_inputs) == 1:
                table_name = stage_inputs[0]['from']
                _from_output = [db.readTableToDf(table_name)]
                # if the first task of the stage will do sql filter, then the use the stage name for the from statement
                done_task = categorize_task(db, stage_name, task, _from_output, stage_name)
                # do the task logging (will do as default)
                if logging:
                    logging_task_output_info(stage_name, task, done_task, db)
                done_tasks.update(done_task)
                tasks.remove(task)
                tasks_cycle= cycle(tasks)
            else:
                # do something for merging stage
                for stage_input in stage_inputs:
                    table_name = stage_input['from']
                    _from_output = db.readTableToDf(table_name)
                    done_tasks.update({table_name: [_from_output]})

                done_task = merge_tasks(db, stage_name, task['id'], stage_inputs, done_tasks, task['inputs']['user_input']['field'])
                # do the task logging (will do as default)
                if logging:
                    logging_task_output_info(stage_name, task, done_task, db)
                done_tasks.update(done_task)
                tasks.remove(task)
                tasks_cycle= cycle(tasks)
        else:
            task_inputs = task['inputs']['task_inputs']
            # if task inputs > 1, that means a merge type of task will happen
            if len(task_inputs) == 1:
                _from = task_inputs[0]['from']
                if _from in done_tasks:
                    _from_output = done_tasks[_from]
                    done_task = categorize_task(db, stage_name, task, _from_output, _from)
                    # do sanity check
                    #NOTE: split & concat function has its own sanity check
                    if task['function'] == 'split-dataframe-rows':
                        pass
                    elif task['function'] == 'concat':
                        concat_task_length_sanity_check(done_task, task['id'])
                    else:
                        task_length_sanity_check(_from_output, done_task, task['id'])
                    # do the task logging (will do as default)
                    if logging:
                        logging_task_output_info(stage_name, task, done_task, db)
                    done_tasks.update(done_task)
                    tasks.remove(task)
                    tasks_cycle= cycle(tasks)
                else:
                    raise ValueError(f"{task['id']} has problems! The upstream task_id not found! Please check you have set your tasks correctly without wording problems!")

#            else:
#                # do something for merging stage
#                done_task = merge_tasks(db, stage_name, task['id'], task_inputs, done_tasks, task['inputs']['user_input']['field'])
#                # do the task logging (will do as default)
#                if logging:
#                    logging_task_output_info(stage_name, task, done_task, db)
#                done_tasks.update(done_task)
#                tasks.remove(task)
#                tasks_cycle= cycle(tasks)
        print(f"{task['id']} task has done!")
    # clear the done tasks dict after stage finished
    done_tasks.clear()

    return done_task
