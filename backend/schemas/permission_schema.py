#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2022/2/11 18:02 
# ide： PyCharm
from pydantic import BaseModel
from typing import  Optional
class PermFilterDatas(BaseModel):
    perm_name:Optional[str]=None

