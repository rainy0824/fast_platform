#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2021/12/2 17:06 
# ide： PyCharm
from  models.model_base import  Base
from  sqlalchemy import  BigInteger,String,DateTime,Column
from  datetime import  datetime
class Menu(Base):
    '''菜单表'''
    __tablename__ ='menu'
    __table_args__ = {'extend_existing': True}
    menu_id = Column(BigInteger, primary_key=True, index=True,unique=True, comment="菜单id",autoincrement=True)
    menu_name = Column(String(20), nullable=False, unique=True, comment="菜单名称")
    menu_flag = Column(String(20), nullable=False, comment="前端标识")
    parent_id = Column(BigInteger, comment="父级菜单id")
    create_time = Column(DateTime(), default=datetime.now, comment="创建时间")
    update_time = Column(DateTime(), default=datetime.now, onupdate=datetime.now, comment="最后一次更新时间")

    def __repr__(self):
        return f"Menu:{self.menu_name}"