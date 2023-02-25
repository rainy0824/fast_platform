#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2022/2/7 16:33 
# ide： PyCharm  页面分页模型
from pydantic import BaseModel
from  typing import  Optional

class Pages(BaseModel):
    pageno: Optional[int] =1
    pagesize: Optional[int] =10

