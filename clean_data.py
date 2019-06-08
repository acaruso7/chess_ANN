#!/home/acaruso/anaconda3/bin/python
import pandas as pd

def read_data():
    """read and concatenate multiple CSV files generated from parser script"""
    df = pd.DataFrame({})
    X_col_idxs = range(768)
    dtypes = {idx: 'int8' for idx in X_col_idxs} #set dtypes beforehand to save memory
    dtypes[768] = 'str'

    for year in ['2016','2017','2018']:
        df = pd.concat([df, pd.read_csv(f'./data/clean/{year}_5k.csv', sep=',', header=None, dtype=dtypes, memory_map=True)], axis=0)
    return df
    
def clean_data(df):
    """clean response variable and drop duplicate rows"""
    # remove prepended # symbols
    df.iloc[:,-1] = df.iloc[:,-1].apply(lambda x : x[1:] if x.startswith("#") else x) 

    # remove prepended + and - symbols, and convert to float
    df.iloc[:,-1] = df.iloc[:,-1].apply(lambda x: float(x[1:]) if x.startswith('+') 
                          else (-float(x[1:]) if x.startswith('-') else float(x)))
    
    print('# rows with duplicates: ', len(df))
    df = df.drop_duplicates(keep='first')
    print('# rows without duplicates: ', len(df))

    return df


if __name__ == '__main__':
    df = read_data()
    clean_df = clean_data(df)
    clean_df.to_csv('15k_games.csv', sep=',', header=False, index=False, mode='a', chunksize=100000)



