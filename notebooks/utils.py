import pandas as pd
import os
from config import SAMPLE_STATE, DATA_DIR

def sample_series(series:pd.Series, size:int=1)->pd.Series:

    return series.sample(n=size, random_state=SAMPLE_STATE).values[0]


def save_df(df:pd.DataFrame, fname:str)->str:

    if not fname.endswith('.csv'):
        fname = fname+'.csv'

    fname = os.path.join(DATA_DIR, fname)

    df.to_csv(fname, sep=';')

    return fname

def read_df(fname:str, **read_kwargs)->pd.DataFrame:

    fpath: str = os.path.join(DATA_DIR, fname)

    df: pd.DataFrame = pd.read_csv(fpath, sep=';', **read_kwargs)

    if 'Unnamed: 0' in df.columns:
        df.drop('Unnamed: 0', axis=1, inplace=True)
    
    return df

def save_df_parquet(df:pd.DataFrame, fname:str)->str:

    if not fname.endswith('.parquet'):
        fname = fname+'.parquet'
    fpath: str = os.path.join(DATA_DIR, fname)

    df.to_parquet(fpath)

    return fpath

def read_df_parquet(fname:str)->pd.DataFrame:

    fpath: str = os.path.join(DATA_DIR, fname)

    return pd.read_parquet(fpath)