# -*- coding: utf-8 -*-
# @Time    : 2022/12/21 23:03
# @Author  : sunxuan
# @Site    : 
# @File    : case_data_manage_model.py
from models.model_base import Base
from  sqlalchemy import Column,String,BigInteger,DateTime,Text,JSON
from sqlalchemy.dialects.mysql import LONGTEXT
from  datetime import  datetime

class DataManageModel(Base):
    '''测试数据ddt'''
    __tablename__ = 'data_manage'
    __table_args__ = {'extend_existing': True}
    data_id =Column(BigInteger(),primary_key=True,autoincrement=True,unique=True,index=True,comment='测试用例id')
    data_env_id =Column(BigInteger(),nullable=False,comment='对应环境配置id')
    data_name =Column(String(255),nullable=False,comment='测试数据场景')
    data_json =Column(JSON,nullable=False,comment='测试数据')
