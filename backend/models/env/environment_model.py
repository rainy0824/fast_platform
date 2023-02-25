#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2022/8/5 17:06 
# ide： PyCharm
from  datetime import datetime
from models.model_base import Base
from sqlalchemy import BigInteger, String, DateTime, Column
class Environment(Base):
    __tablename__ = 'environment'
    __table_args__ = {'extend_existing': True}
    environment_id =Column(BigInteger,primary_key=True,unique=True,index=True,autoincrement=True,comment='环境id')
    environment_name =Column(String(50),nullable=False,comment='环境名称')
    environment_url =Column(String(50),nullable=False,comment='环境url')
    environment_desc =Column(String(50),nullable=True,comment='环境描述')
    create_time = Column(DateTime(), default=datetime.now, comment="创建时间")
    update_time = Column(DateTime(), default=datetime.now, onupdate=datetime.now, comment="最后一次更新时间")
