# -*- coding: utf-8 -*-
# @Time    : 2023/1/14 12:27
# @Author  : sunxuan
# @Site    : 
# @File    : exec_script_schema.py

from pydantic import BaseModel,Field
from typing import Optional,Union,Any
class ScriptModel(BaseModel):
        hooks_code:str=Field(title='python代码')
        return_value:str=Field(title='存储执行代码返回值')
