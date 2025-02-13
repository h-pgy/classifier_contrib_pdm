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

def read_df(fname:str)->pd.DataFrame:

    fpath: str = os.path.join(DATA_DIR, fname)

    return pd.read_csv(fpath, sep=';')