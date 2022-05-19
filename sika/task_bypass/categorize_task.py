# categorize the task based on the task type
from sika.task_bypass.read_content import read_content
from sika.task_bypass.filter_content import filter_content
from sika.task_bypass.transform_content import transform_content
from sika.task_bypass.concat_content import concat_content

def categorize_task(db, stage_name, task, _from_output = None, _last_output_name = None):
    if task['type'] == 'read':
        result = read_content(db, stage_name, task['id'], task['inputs'], task['function'], _from_output)
        return result

    if task['type'] == 'filter':
        #result = filter_content(db, stage_name, task['id'], task['inputs'], task['function'], _from_output, _last_output_name)
        result = filter_content(task['id'], task['inputs'], task['function'], _from_output, _last_output_name)
        return result

    if task['type'] == 'transform':
        #result = transform_content(db, stage_name, task['id'], task['inputs'], task['function'], _from_output)
        result = transform_content(task['id'], task['inputs'], task['function'], _from_output)
        return result

    if task['type'] == 'concat':
        #result = concat_content(db, stage_name, task['id'],  _from_output)
        result = concat_content(task['id'],  _from_output)
        return result

    return {}
