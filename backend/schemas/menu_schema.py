#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2021/12/3 17:53 
# ide： PyCharm
from  typing import Optional
from  pydantic import  BaseModel
class MenuBase(BaseModel):
    menu_name:str
    menu_flag:str
    parent_id:Optional[str]='0'
    menu_id: Optional[str]=None

