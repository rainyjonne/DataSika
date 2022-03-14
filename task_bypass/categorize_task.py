# categorize the task based on the task type
from .read_content import read_content
from .filter_content import filter_content
from .transform_content import transform_content

def categorize_task(task, _from_output = None, _output_name = None):
    if task['type'] == 'read':
        result = read_content(task['id'], task['inputs'], task['output'],  task['function'], _from_output)
        return result
    
    if task['type'] == 'filter':
        result = filter_content(task['id'], task['inputs'], task['output'], task['function'], _from_output, _output_name)
        return result
    
    if task['type'] == 'transform':
        result = transform_content(task['id'], task['inputs'], task['output'], task['function'], _from_output)
        return result
           
    return {}
