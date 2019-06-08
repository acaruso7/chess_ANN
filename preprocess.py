#!/home/acaruso/anaconda3/bin/python
import pandas as pd

df = pd.DataFrame({})
X_col_idxs = range(768)
dtypes = {idx: 'uint8' for idx in X_col_idxs} #set dtypes beforehand to save memory
dtypes[768] = 'str'

for year in ['2016', '2017','2018']:
    df = pd.concat([df, pd.read_csv(f'./data/clean/{year}_5k.csv', sep=',', header=None, dtype=dtypes, memory_map=True)], axis=0)
    
#####
# clean and normalize response variable here, then write to csv
#####

# df.to_csv('15k_games.csv', sep=',', header=False, index=False)