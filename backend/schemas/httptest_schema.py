# -*- coding: utf-8 -*-
# @Time    : 2022/11/18 20:38
# @Author  : sunxuan
# @Site    : 
# @File    : httptest_schema.py
from  pydantic import BaseModel,Field
from  typing import  Optional,Union
from datetime import  datetime
from common.enums.request_emus import BodyType
class HttpRequestBase(BaseModel):
    request_id:Optional[int]=Field(default=None,description='request id')
    request_method: str
    request_url:str
    request_body: Union[str]
    request_body_type: BodyType=Field(default=BodyType.none,description='数据格式类型')
    request_headers: dict={}
    update_time: Optional[datetime]

class CreateHttpRequest(BaseModel):
    method: str
    url:str
    body: Union[str]
    body_type: BodyType=Field(default=BodyType.none,description='数据格式类型')
    headers: dict={}

class UpdateHttpRequest(BaseModel):
    id:Optional[int] #request id
    method: str
    url:str
    body: Union[str]
    body_type: BodyType=Field(default=BodyType.none,description='数据格式类型')
    headers: dict={}
