#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2022/8/8 15:20 
# ide： PyCharm
from datetime import datetime

from  pydantic import  BaseModel
from  typing import  Optional,List,Union

class EnvBase(BaseModel):
    environment_id: Optional[str]
    environment_name: str
    environment_desc: Optional[str]
    environment_url: str
    create_time: datetime

class CreateEnv(BaseModel):
    environment_name: str
    environment_desc: Optional[str]
    environment_url: str

class UpdateEnv(BaseModel):
    environment_name: str
    environment_desc: Optional[str]
    environment_url: str


class EnvList(BaseModel):
    totals: int
    envs: List[EnvBase]