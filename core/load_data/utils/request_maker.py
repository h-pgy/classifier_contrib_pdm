from requests import Session, Response
from typing import Dict, Any, Optional, Union, Literal
from ..exceptions import NoContentError
from ...types.json import JSON_TYPE

class RequestMaker:

    RESPONSE_TYPES: set[str] = {'json', 'text', 'content', 'raw'}

    def __init__(self, base_headers:Optional[Dict[str, Any]]=None)->None:

        self.session = Session()
        self.__set_base_headers(base_headers)

    def __set_base_headers(self, headers:Union[Dict[str, Any], None])->None:

        self.base_headers: Dict[str, Any] | None = headers
        if self.base_headers:
            self.session.headers = self.base_headers
    
    def __get_response(self, url:str, params:Optional[Dict[str,Any]]=None, headers:Optional[Dict[str, Any]]=None)->Response:

        with self.session.get(url=url, params=params, headers=headers) as r:
            r.raise_for_status()
            if r.status_code==204:
                raise NoContentError('No content')

            return r
        
    def __post_response(self, url:str, params:Optional[Dict[str,Any]]=None, headers:Optional[Dict[str, Any]]=None,
                        data:Optional[Dict[str, Any]]=None, json:Optional[Dict[str, Any]]=None)->Response:
        
        with self.session.post(url=url, params=params, headers=headers, data=data,
                               json=json) as r:
            r.raise_for_status()

            if r.status_code==204:
                raise NoContentError('No content')
            return r
        
    def __solve_response_type(self, response:Response, 
                              response_type: Literal["json", "text", "content", "raw"])->Union[JSON_TYPE, str, bytes, Response]:
        

        if response_type not in self.RESPONSE_TYPES:
            raise ValueError(F"Response type must be in {self.RESPONSE_TYPES}")

        if response_type == "json":
            return response.json()
        if response_type == "text":
            return response.text
        if response_type == "content":
            return response.content
        
        return response
    
    def get(self, url:str, 
            response_type: Literal["json", "text", "content", "raw"],
            params:Optional[Dict[str, Any]]=None, 
            headers:Optional[Dict[str, Any]]=None)->Union[JSON_TYPE, str, bytes, Response]:

        response: Response = self.__get_response(url, params, headers)
        
        return self.__solve_response_type(response, response_type)
    
    def post(self, url:str, 
                    response_type: Literal["json", "text", "content", "raw"],
                    params:Optional[Dict[str, Any]]=None,
                    headers:Optional[Dict[str, Any]]=None,
                    data:Optional[Dict[str, Any]]=None, 
                    json:Optional[Dict[str, Any]]=None)->Union[JSON_TYPE, str, bytes, Response]:


        response: Response = self.__post_response(url, params, headers, data=data, json=json)
        
        return self.__solve_response_type(response, response_type)
        

            

