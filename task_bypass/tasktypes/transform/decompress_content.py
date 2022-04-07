import gzip
import pandas as pd

# input type: string, output type: string
def decompress_content(comp_df):
    comp_str = comp_df[0][0]
    decom_str = gzip.decompress(comp_str).decode('utf-8')
    decom_df = pd.DataFrame([decom_str])

    return decom_df
