from core.types import JSON_LIST
import pandas as pd


class Parser:

    def parse_data(self, data:dict[str, JSON_LIST])->pd.DataFrame:

        all_parsed_data: list[dict[str, str]] = []
        for contrib_list in data.values():
            for contrib in contrib_list:
                for sugestao in contrib['sugestoes']:
                    trecho: str = sugestao['conteudo']
                    categoria: str = sugestao['tema']['categoria']['nome']
                    parsed_data: dict[str, str] = {'excerto' : trecho,
                                'categoria' : categoria}
                    
                    all_parsed_data.append(parsed_data)

        
        df = pd.DataFrame(all_parsed_data)

        return df
    
    def remove_duplicates(self, df:pd.DataFrame)->pd.DataFrame:

        df = df.drop_duplicates(keep='first').reset_index(drop=True)

        return df
    
    def remove_duplicates_excert(self, df:pd.DataFrame)->pd.DataFrame:

        #em alguns casos os mesmos excertos foram utilizados para duas categorias

        df = df[~df['excerto'].duplicated(keep='first')].reset_index(drop=True)

        return df
    
    def __call__(self, data:dict[str, JSON_LIST])->pd.DataFrame:

        df = self.parse_data(data)
        df = self.remove_duplicates(df)
        df = self.remove_duplicates_excert(df)

        return df

