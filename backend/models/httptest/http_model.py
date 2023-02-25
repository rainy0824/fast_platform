# -*- coding: utf-8 -*-
# @Time    : 2022/11/18 20:35
# @Author  : sunxuan
# @Site    : 
# @File    : http_model.py
from models.model_base import Base
from  sqlalchemy import Column,String,BigInteger,JSON,DateTime,Enum
from sqlalchemy.dialects.mysql import LONGTEXT
from datetime import datetime
class HttpRequestModel(Base):
    '''请求数据表'''
    __tablename__ = 'request_info'
    __table_args__ = {'extend_existing': True}
    request_id =Column(BigInteger(),primary_key=True,autoincrement=True,unique=True,index=True,comment='请求id')
    request_method=Column(String(100),nullable=False,comment='请求method')
    request_url=Column(String(255),nullable=False,comment='请求url')
    request_body=Column(LONGTEXT,nullable=True,comment='请求body内容')
    request_body_type=Column(BigInteger(),comment='请求body类型/none 0/json 1/form_data 2/x_form 3')
    request_headers =Column(JSON,default={},comment='请求头')
    create_time = Column(DateTime(), default=datetime.now, comment='创建时间')
    update_time = Column(DateTime(), default=datetime.now, comment='修改时间')

