#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2022/8/16 16:48 
# ide： PyCharm
from models.model_base import Base
from  sqlalchemy import Column,String,BigInteger,DateTime,Text,JSON
from sqlalchemy.dialects.mysql import LONGTEXT
from  datetime import  datetime

class TestCase(Base):
    '''测试用例、配置'''
    __tablename__ = 'test_case'
    __table_args__ = {'extend_existing': True}
    case_id=Column(BigInteger(),primary_key=True,autoincrement=True,unique=True,index=True,comment='测试用例id')
    case_name =Column(String(100),nullable=False,comment='测试用例名称',index=True)
    case_project_id=Column(BigInteger(),nullable=False,comment='所属项目')
    case_module_id =Column(BigInteger(),nullable=False,comment='所属模块')
    case_include_case_id =Column(JSON,nullable=True,comment='关联前置测试用例id')
    case_tag = Column(String(255), nullable=True, comment='用例标签')
    case_status = Column(BigInteger(), nullable=True, comment='用例状态 1生效 0失效', default=1)
    case_priority = Column(BigInteger(), nullable=False, comment='用例优先级', default=3)
    request_type =Column(BigInteger(),nullable=True,comment='http1 grpc2 dubbo3 websocket4',default=1)
    base_url =Column(String(255),nullable=True,comment='base_path')
    request_method=Column(String(100),nullable=True,comment='请求method')
    request_url=Column(String(255),nullable=False,comment='请求url')
    request_body=Column(LONGTEXT,nullable=True,comment='请求body内容')
    request_body_type=Column(BigInteger(),comment='请求body类型/none 0/json 1/form_data 2/x_form 3')
    request_headers =Column(JSON,default={},comment='请求头')
    setup_hooks = Column(JSON, nullable=True, comment='前置操作')
    teardown_hooks = Column(JSON, nullable=True, comment='后置操作')
    variables = Column(JSON,nullable=True,comment='变量参数')
    extract = Column(JSON,nullable=True,comment='提取参数')
    validators = Column(JSON, nullable=True, comment='断言规则')
    create_time = Column(DateTime(), default=datetime.now, comment='创建时间')
    update_time = Column(DateTime(), default=datetime.now, comment='最后一次更新时间')
