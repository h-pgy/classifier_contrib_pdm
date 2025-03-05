from typing import Literal, Optional, Dict, Any
from core.types import BASIC_TYPES
import re


class UrlBuilder:

    def __check_scheme(self, scheme:str)->None:

        if scheme not in {'http', 'https'}:
            raise ValueError(f'Unallowed scheme: {scheme}')
        
    def __clean_scheme(self, scheme:str)->str:

        return scheme.rstrip('://')
        
    def __clean_scheme_from_domain(self, domain:str)->str:

        return domain.lstrip('http://').lstrip('https://')
    
    def __clean_domain(self, domain:str)->str:

        domain = self.__clean_scheme_from_domain(domain)

        return domain.rstrip('/')

    def __check_domain(self, domain:str)->None:

        domain_regex = r"^(?:https?:\/\/)?(?:www\.)?([a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,})$"
        if not re.match(domain_regex, domain):
            raise ValueError(f'Invalid domain: {domain}')
        
    def __clean_path(self, path:str)->str:

        path = path.rstrip(r'/')

        if not path.startswith(r'/'):
            return f'/{path}'

        return path
    
    def __build_params_str(self, params:Dict[str, BASIC_TYPES])->str:


        param_lst: list[str] = [f'{key}={value}' for key, value in params.items()]
        param_str: str = '&'.join(param_lst)

        param_str = '?'+param_str

        return param_str

            
    def __build(self, scheme:str, domain:str, path:str, endpoint:str, params:Optional[Dict[str, BASIC_TYPES]]=None)->str:

        self.__check_scheme(scheme)
        scheme = self.__clean_scheme(scheme)

        self.__check_domain(domain)
        domain = self.__clean_domain(domain)

        path = self.__clean_path(path)

        
        param_str: str = self.__build_params_str(params) if params else ''

        url: str = f'{scheme}://{domain}/{path}/{endpoint}/{param_str}'

        return url
    
    def __call__(self, domain:str, path:str, endpoint:str, 
                 params:Optional[Dict[str, BASIC_TYPES]]=None,
                 scheme:str='https')->str:

        return self.__build(scheme, domain, path, endpoint, params)


