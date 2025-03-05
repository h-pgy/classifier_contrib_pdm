import pandas as pd
import os
from config import DATA_DIR
from typing import Dict, Literal
from ..extract_data.extract_contribs import ContribLoader
from ..parse_data.parser import Parser

from ..types import JSON_LIST

class Loader:

    def __init__(self, extractor:ContribLoader, parser:Parser):

        self.extract = extractor
        self.parse = parser

    def solve_fpath(self, fname:str)->str:

        if not os.path.exists(DATA_DIR):
            os.mkdir(DATA_DIR)

        fpath = os.path.join(DATA_DIR, fname)

        return fpath

    def save_df_csv(self, df:pd.DataFrame, fname:str)->str:

        fname = self.solve_file_extension(fname, '.csv')

        fpath = self.solve_fpath(fname)

        df.to_csv(fpath, sep=';', index=False)

        return fname
    
    def read_df_csv(self, fname:str, **read_kwargs)->pd.DataFrame:
        
        fname = self.solve_file_extension(fname, '.csv')

        fpath = self.solve_fpath(fname)

        df: pd.DataFrame = pd.read_csv(fpath, sep=';', **read_kwargs)

        if 'Unnamed: 0' in df.columns:
            df.drop('Unnamed: 0', axis=1, inplace=True)
        
        return df
    
    def save_df_parquet(self, df:pd.DataFrame, fname:str)->str:

        fname = self.solve_file_extension(fname, '.parquet')
        fpath: str = self.solve_fpath(fname)

        df.to_parquet(fpath)

        return fpath

    def read_df_parquet(self, fname:str)->pd.DataFrame:

        fname = self.solve_file_extension(fname, '.parquet')
        fpath: str = self.solve_fpath(fname)

        return pd.read_parquet(fpath)
    
    def solve_file_extension(self, fname:str, extension:str)->str:

        if not fname.endswith(extension):
            fname = fname + f'.{extension.replace('.', '')}'

        return fname
    

    def check_file_exists(self, fname:str, extension:str)->bool:

        fname = self.solve_file_extension(fname, extension)
        fpath = self.solve_fpath(fname)

        return os.path.exists(fpath)

    def build_data_pipeline(self)->pd.DataFrame:

        data: Dict[str, JSON_LIST] = self.extract()
        df: pd.DataFrame = self.parse(data)

        return df

    
    def load_data(self, fname:str, type:Literal['csv', 'parquet'], **read_kwargs)->pd.DataFrame:

        if type == 'csv':
            if self.check_file_exists(fname, 'csv'):
                return self.read_df_csv(fname, **read_kwargs)
            else:
                df:pd.DataFrame = self.build_data_pipeline()
                self.save_df_csv(df, fname)
                return self.read_df_csv(fname)
            
        if type == 'parquet':
            if self.check_file_exists(fname, 'parquet'):
                return self.read_df_parquet(fname, **read_kwargs)
            else:
                df:pd.DataFrame = self.build_data_pipeline()
                self.save_df_parquet(df, fname)
                return self.read_df_parquet(fname)
            
    def __call__(self, type:Literal['csv', 'parquet'], **read_kwargs)->pd.DataFrame:

        return self.load_data('original_data', type=type, **read_kwargs)