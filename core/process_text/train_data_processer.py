from pandas.core.frame import DataFrame
from core.load_data import Loader
from .text_processer import Preprocesser
from typing import Literal, Optional

class DataProcesser:

    min_registers = 100
    category_column = 'categoria'
    text_column = 'excerto'

    def __init__(self, text_processer:Optional[Preprocesser]=None)->None:

        self.text_processer: Preprocesser = text_processer or Preprocesser()

    def identify_classes_with_low_registers(self, data:DataFrame)->list[str]:

        menos_que_minimo_mask= data[self.category_column].value_counts()<100
        categorias_menos_que_minino= list(data[self.category_column].value_counts().index[menos_que_minimo_mask])

        print(f'Categorias com menos que o minino: {categorias_menos_que_minino}')

        return categorias_menos_que_minino
    
    def transform_class_to_etc_class(self, data:DataFrame, to_be_transformed:list[str], transform_to:str)->DataFrame:
        
        data = data.copy()
        data[self.category_column] = data[self.category_column].apply(lambda x: x if x not in to_be_transformed else transform_to)

        return data
    

    def transform_classes_low_registers(self, data:DataFrame)->DataFrame:

        menos_que_minimo: list[str] = self.identify_classes_with_low_registers(data)
        to_transform = 'Outros temas'

        return self.transform_class_to_etc_class(data, menos_que_minimo, to_transform)
    
    def process_text(self, data:DataFrame)->DataFrame:

        data = data.copy()
        data['processed_text'] = data[self.text_column].apply(lambda x: self.text_processer(x))

        return data


    def pipeline(self, data:DataFrame)->DataFrame:

        data = data.copy()
        data = self.transform_classes_low_registers(data)
        data = self.process_text(data)
        
        return data
    
    def __call__(self, data:DataFrame)->DataFrame:

        return self.pipeline(data)
