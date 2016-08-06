import pandas as pd
ww=pd.read_csv("pisa2012.csv",chunksize=100)
qq=ww.get_chunk()
