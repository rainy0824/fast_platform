#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2022/8/11 15:46 
# ide： PyCharm
from models.model_base import Base
from  sqlalchemy import Column,String,BigInteger,DateTime
from  datetime import  datetime

class Module(Base):
    '''模块表'''
    __tablename__ ='module'
    __table_args__ = {'extend_existing': True}
    module_id =Column(BigInteger(),primary_key=True,autoincrement=True,unique=True,index=True,comment='模块id')
    module_name=Column(String(100),nullable=False,comment='模块名称')
    parent_module_id = Column(BigInteger, comment="父级模块id")
    module_project_id =Column(BigInteger(),nullable=False,comment='项目id')
    module_manager=Column(String(50),nullable=True,comment='测试负责人')
    module_desc =Column(String(200),nullable=True,comment='描述信息')
    create_time = Column(DateTime(), default=datetime.now, comment='创建时间')
    update_time = Column(DateTime(), default=datetime.now, comment='最后一次更新时间')
class ModuleProjectRelation(Base):
    '''模块项目关联表'''
    __tablename__ ='module_project'
    __table_args__ = {'extend_existing': True}
    id =Column(BigInteger(),primary_key=True,autoincrement=True,unique=True,index=True)
    module_id =Column(BigInteger(),comment='模块id')
    project_id =Column(BigInteger(),comment='项目id')

