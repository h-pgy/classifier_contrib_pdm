from typing import Dict, List, Union
from .basic import BASIC_TYPES

JSON_TYPE = Dict[str, Union[BASIC_TYPES, List["JSON_TYPE"], List[BASIC_TYPES]]]

JSON_LIST=List[JSON_TYPE]