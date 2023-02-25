#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2022/8/17 13:56 
# ide： PyCharm
#配置管理
from models.model_base import Base
from  sqlalchemy import Column,String,BigInteger,DateTime
from  datetime import  datetime

class ConfigManage(Base):
    __tablename__ = 'config_manage'
    __table_args__ = {'extend_existing': True}
