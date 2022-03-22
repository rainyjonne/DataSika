from lxml import html

def xpath(_from_output, value):
    bytes_str = _from_output.encode('utf-8')
    tree = html.fromstring(bytes_str)
    filtered_result = tree.xpath(value)
        
    if filtered_result == []:
         return None        
    if len(filtered_result) == 1:
        # if result after filter has only one output, return a str
        if type(filtered_result).__name__ == 'HtmlElement':
            final_result = html.tostring(filtered_result[0])
        else:
            final_result = str(filtered_result[0])
    else:
        #NOTE: might be more circumstances in the future
        # if result after filter is a list, return list of strings
        final_result = list(map(lambda ele: html.tostring(ele).decode('utf-8'), filtered_result))

    
    return final_result
