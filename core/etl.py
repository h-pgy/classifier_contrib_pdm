from core.extract_data import extract_contributions
from core.parse_data import parse_data
from core.load_data import Loader

load_data = Loader(extract_contributions, parse_data)