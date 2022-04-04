

def task_length_sanity_check(_input, _output):
    # _input is a list of dataframes
    # _output is a dictionary, so need to take values out and transform to a list of dataframes then calculate the length
    if len(_input) == len(list(_output.values())[0]):
        return True
    else:
        raise ValueError("The input and output length of this task doesn't match, please check out what's wrong")


# ref: https://stackoverflow.com/questions/35791051/better-way-to-check-if-all-lists-in-a-list-are-the-same-length
def merge_sanity_check(done_tasks):
    # get dictionary values (each stage's last done_task's output list of dataframes)
    output_lists = list(done_tasks.values())
    it = iter(output_lists)
    the_len = len(next(it))
    # the_len is the length of  first element, use it to compare with other elements whether they have same length
    if not all(len(l) == the_len for l in it):
        raise ValueError("Not all stage's done task have same length! Please check that all stages should have SAME LENGTH OUTPUT.")