# -*- coding: utf-8 -*-
# @Time    : 2022/12/21 23:09
# @Author  : sunxuan
# @Site    : 
# @File    : case_data_manage_schema.py

from typing import Optional
from pydantic import BaseModel, Field
class DataManageBase(BaseModel):
    data_id: Optional[int]
    data_env_id:Optional[int]=Field(title='对应环境id')
    data_name: Optional[str]
    data_json: Optional[dict]={}

class CreateDataManage(BaseModel):
    data_env_id:Optional[int]=Field(title='对应环境id')
    data_name: Optional[str]
    data_json: Optional[dict]={}

class UpdateDataManage(BaseModel):
    data_id: Optional[int]
    data_env_id:Optional[int]=Field(title='对应环境id')
    data_name: Optional[str]
    data_json: Optional[dict]={}


