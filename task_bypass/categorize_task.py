# categorize the task based on the task type
from task_bypass.read_content import read_content
from task_bypass.filter_content import filter_content
from task_bypass.transform_content import transform_content
from task_bypass.concat_content import concat_content

def categorize_task(task, _from_output = None, _last_output_name = None):
    if task['type'] == 'read':
        result = read_content(task['id'], task['inputs'], task['function'], _from_output)
        return result

    if task['type'] == 'filter':
        result = filter_content(task['id'], task['inputs'], task['function'], _from_output, _last_output_name)
        return result

    if task['type'] == 'transform':
        result = transform_content(task['id'], task['inputs'], task['function'], _from_output)
        return result

    if task['type'] == 'concat':
        result = concat_content(task['id'],  _from_output)
        return result

    return {}
