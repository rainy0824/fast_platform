#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2022/8/11 17:16 
# ide： PyCharm
from datetime import datetime

from  pydantic import BaseModel
from typing import  Optional,List

class ModuleBase(BaseModel):
    '''模块模型'''
    parent_module_id:Optional[int]=0 #父模块id
    module_id:Optional[int]  #模块id
    module_name:str
    module_manager:Optional[str]
    module_desc:Optional[str]
    module_project_id:Optional[int]  #所属项目名称id
    module_project_name:str  #所属项目名称
    create_time: datetime

class ModuleList(BaseModel):
    totals: int
    modules:List[ModuleBase]

class CreateModule(BaseModel):
    parent_module_id:Optional[int]=0 #父模块id
    module_name:str
    module_manager:Optional[str]
    module_desc:Optional[str]
    module_project_id:int  #所属项目id

class UpdateMoule(BaseModel):
    parent_module_id:Optional[int]=0 #父模块id
    module_id: Optional[str]  # 模块id
    module_name:str
    module_manager:Optional[str]
    module_desc:Optional[str]
    module_project_id:int  #所属项目id