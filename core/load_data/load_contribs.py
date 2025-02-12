from .utils import RequestMaker, UrlBuilder
from typing import Dict, Optional, Any
from ..types import JSON_LIST, BASIC_TYPES

from urllib.parse import urljoin
from requests.exceptions import HTTPError, ChunkedEncodingError
import time

from .exceptions import NoContentError

class ContribLoader:

    DOMAIN: str = 'devolutiva.pdm.prefeitura.sp.gov.br'
    PATH='/api/v1'

    def __init__(self, headers:Optional[Dict[str, Any]]=None)->None:

        self.request = RequestMaker(headers)
        self.build_url = UrlBuilder()


    def __get_contribs(self, offset:int, limit:int, data:Optional[Dict[str, BASIC_TYPES]]=None)->JSON_LIST:

        endpoint = '/contribuicoes/pesquisar'

        req_data: Dict[str, BASIC_TYPES]={'offset' : offset,
                                        'limit' : limit}
        if data:
            req_data.update(data)

        url: str = self.build_url(self.DOMAIN, self.PATH, endpoint, req_data)

        return self.request.post(url, data=req_data, response_type='json') # type: ignore

  
    def __get_all_contribs_search(self, search_data:dict, initial_offset:int=0)->JSON_LIST:

        LIMIT = 100
        WAIT_SECONDS = 3
        offset: int = initial_offset

        all_contribs:JSON_LIST = []

        while True:
            
            try:

                contribs: JSON_LIST = self.__get_contribs(offset, data=search_data, limit=LIMIT)
                all_contribs.extend(contribs)
                offset+=len(contribs)

            # response header error - happens from time to time
            except ChunkedEncodingError as e:
                print(f'Incomplete read - waiting {WAIT_SECONDS} seconds')
                time.sleep(WAIT_SECONDS)

            except NoContentError as e:
                print('Finished - 204')
                break
            
            except HTTPError as e:

                #too many requests
                if e.response.status_code == 429:
                    print(f'Too many requests - waiting {WAIT_SECONDS} seconds')
                    time.sleep(WAIT_SECONDS)

                # not found
                if e.response.status_code == 404:
                    print('Finished - 404')
                    break

        return all_contribs
    
    def __get_categories(self)->JSON_LIST:

        endpoint = '/categorias'
        url: str = self.build_url(self.DOMAIN, self.PATH, endpoint)

        return self.request.get(url, response_type='json') # type: ignore
    
    def __get_all_contribs_by_categorie(self, cat_id:int, initial_offset:int=0)->JSON_LIST:

        search_data: Dict[str, int] = {'idCategoria' : cat_id}

        return self.__get_all_contribs_search(search_data, initial_offset=initial_offset)
    
    def get_all_contribs(self, initial_offset:int=0)->Dict[str, JSON_LIST]:

        categories: JSON_LIST = self.__get_categories()
        all_data: Dict[str, JSON_LIST] = {}
        for cat in categories:
            
            cat_id: int = cat['id'] #type: ignore
            cat_name: str = cat['nome'] #type: ignore
            contribs: JSON_LIST = self.__get_all_contribs_by_categorie(cat_id, initial_offset)
            all_data[cat_name] = contribs
        
        return all_data