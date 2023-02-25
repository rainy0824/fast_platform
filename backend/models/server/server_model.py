#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2022/2/23 16:29 
# ide： PyCharm
from  models.model_base import Base
from  sqlalchemy import Column,String,BigInteger,DateTime
from  datetime import datetime
class Server(Base):
     __tablename__ ='server'
     __table_args__ = {'extend_existing': True}
     server_id =Column(BigInteger(),primary_key=True,autoincrement=True,unique=True,index=True,comment='服务器id')
     server_name =Column(String(50),nullable=False,comment='服务器名称')
     server_desc =Column(String(500),nullable=False,comment='服务器名称描述')
     server_ip =Column(String(50),nullable=False,comment='服务器ip地址')
     server_port =Column(String(10),nullable=True,comment='服务器ip端口')
     server_login_name=Column(String(50),nullable=True,comment='服务器登录用户名')
     server_login_pwd =Column(String(50),nullable=True,comment='服务器登录密码')
     create_time = Column(DateTime(), default=datetime.now, comment='创建时间')
     update_time = Column(DateTime(), default=datetime.now, comment='修改时间')