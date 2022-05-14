
def task_length_sanity_check(_input, _output, task_id):
    # _input is a list of dataframes
    # _output is a dictionary, so need to take values out by task id
    if len(_input) == len(_output[task_id]):
        return True
    else:
        raise ValueError(f"{task_id} has problems! The input and output length of this task doesn't match, please check out what's wrong")


def concat_task_length_sanity_check(_output, task_id):
    # only check if output is only "one dataframe" inside a list
    _output_len = len(_output[task_id])
    if _output_len == 1:
        return True
    else:
        raise ValueError(f"{task_id} has problems! The concat task didn't produce a 'one dataframe list', please check out what's wrong")


def split_task_length_sanity_check(_input, _output, task_id):
    # _input is a list of "one dataframe"
    # _output is a dictionary, so need to take values out by task id
    _input_len = len(_input.index)
    _output_len = len(_output)
    if _input_len == _output_len:
        return True
    else:
        raise ValueError(f"{task_id} has problems! This split task doesn't have consistent length before/after splitting, please check out what's wrong")


# ref: https://stackoverflow.com/questions/35791051/better-way-to-check-if-all-lists-in-a-list-are-the-same-length
def merge_sanity_check(done_tasks):
    # get dictionary values (each stage's last done_task's output list of dataframes)
    output_lists = list(done_tasks.values())
    it = iter(output_lists)
    the_len = len(next(it))
    # the_len is the length of  first element, use it to compare with other elements whether they have same length
    if not all(len(l) == the_len for l in it):
        raise ValueError("Not all stage's done task have same length! Please check that all stages should have SAME LENGTH OUTPUT.")
