#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2022/6/16 20:12 
# ide： PyCharm
from datetime import datetime

from  pydantic import  BaseModel
from  typing import  Optional,List,Union

# class Project_Filter_data(BaseModel):
#     project_name: Optional[str]
#     project_manager: Optional[str]
#     project_status: Optional[bool]

class ProjectBase(BaseModel):
    project_id: Optional[int]
    project_name: Optional[str]
    project_desc: Optional[str]
    project_manager: Optional[str]
    developer:Optional[str]
    tester: Optional[str]
    project_status : Optional[bool] = True
    create_time: Optional[datetime]

class CreateProject(BaseModel):
    '''添加项目'''
    project_name: str
    project_desc: Optional[str]
    project_manager: Optional[str]
    developer:Optional[str]
    tester: Optional[str]
    project_status : Optional[bool] = True
class UpdateProject(BaseModel):
    '''修改项目'''
    project_name: str
    project_desc: Optional[str]
    project_manager: Optional[str]
    developer:Optional[str]
    tester: Optional[str]
    project_status : Optional[bool] = True


class Project_List(BaseModel):
    totals: int=0
    projects: List[ProjectBase]