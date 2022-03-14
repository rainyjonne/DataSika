from lxml import html
def xpath(_from_output, value):
    filtered_result = _from_output.xpath(value)
    if filtered_result == []:
        return [None]
    
    return filtered_result
