#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2021/12/2 16:20 
# ide： PyCharm
#角色

from models.model_base import Base
from  sqlalchemy import Column,String,BigInteger,DateTime
from  datetime import  datetime
class Role(Base):
    '''角色模型'''
    __tablename__ ='role'
    __table_args__ = {'extend_existing': True}
    role_id = Column(BigInteger(),primary_key=True,autoincrement=True,unique=True,index=True,comment='角色id')
    role_name = Column(String(30),nullable=False,comment='角色名称')
    role_desc =Column(String(100),nullable=True,comment='角色描述')
    create_time =Column(DateTime(),default=datetime.now,comment='创建时间')
    update_time =Column(DateTime(),default=datetime.now,onupdate=datetime.now,comment='最后一次更新时间')
    def __repr__(self):
        return f'role_name:{self.role_name}'

class RoleUserRelation(Base):
    '''角色用户关联表'''
    __tablename__ ='role_user'
    __table_args__ = {'extend_existing': True}
    id = Column(BigInteger(),primary_key=True,index=True,unique=True)
    role_id =Column(BigInteger(),comment='角色id')
    user_id =Column(BigInteger(),comment='用户id')

class RoleMenuRelation(Base):
    '''角色菜单关联表'''
    __tablename__ ='role_menu'
    __table_args__ = {'extend_existing': True}
    id = Column(BigInteger(),primary_key=True,index=True,unique=True)
    role_id =Column(BigInteger(),comment='角色id')
    menu_id =Column(BigInteger(),comment='菜单id')
class RolePermissionRelation(Base):
    '''角色权限关联表'''
    __tablename__ = 'role_permission'
    __table_args__ = {'extend_existing': True}
    id = Column(BigInteger(),  primary_key=True, index=True, unique=True)
    role_id = Column(BigInteger(), comment='角色id')
    permission_id = Column(BigInteger(), comment='权限id')
