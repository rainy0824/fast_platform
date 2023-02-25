#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2022/6/16 13:58 
# ide： PyCharm
from  models.model_base import Base
from  sqlalchemy import Column,String,BigInteger,DateTime,Boolean
from  datetime import  datetime

class Project(Base):
    __tablename__ ='project'
    __table_args__ = {'extend_existing': True}
    project_id = Column(BigInteger(),primary_key=True,unique=True,autoincrement=True,index=True,comment='项目id')
    project_name = Column(String(30),nullable=False,comment='项目名称')
    project_desc = Column(String(60),nullable=True,comment='项目描述')
    project_manager = Column(String(30),nullable=True,comment='项目负责人')
    developer = Column(String(30),nullable=True,comment='开发人员')
    tester = Column(String(30),nullable=True,comment='测试人员')
    project_status =Column(Boolean(),default=True,comment='项目状态')
    create_time = Column(DateTime(), default=datetime.now, comment='创建时间')
    update_time = Column(DateTime(), default=datetime.now, comment='修改时间')



