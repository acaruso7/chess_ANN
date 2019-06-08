#!/home/acaruso/anaconda3/bin/python
import pandas as pd

df = pd.DataFrame({})
for year in ['2016']:
    df = pd.concat([df, pd.read_csv(f'./data/clean/{year}_5k.csv', sep=',', header=None)], axis=0)
    
print(len(df))