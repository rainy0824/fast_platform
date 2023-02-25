#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2022/2/23 16:28 
# ide： PyCharm
from pydantic import  BaseModel,Field
from typing import  Optional,List
from  datetime import datetime
class ServerBase(BaseModel):
    server_id: Optional[str]=None
    server_name: str
    server_ip: str
    server_port:Optional[str]=22
    server_desc: str
    create_time: datetime = None
    server_login_name:Optional[str]=None
    server_login_pwd:Optional[str]=None

class UpdateServer(BaseModel):
    server_name: Optional[str]=None
    server_ip:Optional[str]=None
    server_port:Optional[str]=None
    server_desc: Optional[str]=None
    server_login_name:Optional[str]=None
    server_login_pwd:Optional[str]=None


class ServerList(BaseModel):
     #服务器列表
     totals: int =Field(title='列表总数')
     servers: List[ServerBase]


class ServerFilterdata(BaseModel):
    server_name:Optional[str]=None
    server_ip:Optional[str]=None
