from task_bypass.tasktypes.merge.sql_merge import sql_merge


def merge_tasks(task_id, task_inputs, done_tasks, value):
  dataframes = {}
  for input in task_inputs:
    _from = input['from']
    dataframe = {_from: done_tasks[_from]}
    dataframes.update(dataframe)

  output = sql_merge(dataframes, value)

  return {
      task_id: output
  }