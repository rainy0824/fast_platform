#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2021/12/2 17:01 
# ide： PyCharm
from  sqlalchemy import BigInteger, Column,DateTime,String
from datetime import  datetime
from  models.model_base import Base
class Permission(Base):
    '''权限表'''
    __tablename__ ='permission'
    __table_args__ = {'extend_existing': True}
    perm_id = Column(BigInteger, autoincrement=True, index=True, primary_key=True, unique=True)
    perm_name = Column(String(20), nullable=False, unique=True, comment="权限名称")
    perm_interface = Column(String(100), nullable=False, unique=True, comment="权限对应的接口")
    create_time = Column(DateTime(), default=datetime.now, comment="创建时间")
    update_time = Column(DateTime(), default=datetime.now, onupdate=datetime.now, comment="最后一次更新时间")
    def __repr__(self):
        return f'perm_name:{self.perm_name}'
