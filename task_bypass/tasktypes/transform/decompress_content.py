import gzip
# input type: string, output type: string
def decompress_content(value):
    decom_str = gzip.decompress(value).decode('utf-8')
    return decom_str
