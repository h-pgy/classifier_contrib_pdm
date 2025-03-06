from .train_data_processer import DataProcesser
from .text_processer import Preprocesser
from ..etl import load_data

process_training_data = DataProcesser()
process_text = Preprocesser()