#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2022/8/17 16:48 
# ide： PyCharm

from datetime import datetime
from typing import Any, List, Optional, Union

from pydantic import BaseModel, Field
from common.enums.request_emus import BodyType


class TestCaseBase(BaseModel):
    case_id: Optional[int]
    case_name: str
    case_project_id: int
    case_project_name: Optional[str]
    case_module_id: int
    case_module_name:Optional[str]
    case_include_case_id: List[Union[str, int]] = Field(default=[], title='关联前置测试用例id')
    case_tag: Optional[str] = Field(default=None, title='用例标签')
    case_status: int = Field(default=1, title='用例状态 1生效 0失效')
    case_priority: Optional[int] = Field(default=3, title='用例优先级 ')
    request_type: Optional[int] = Field(default=1, title='case类型http 1 grap2xx')
    base_url: Optional[str]
    request_method: Optional[str]
    request_url: str
    request_body: Optional[Union[str]]
    request_body_type: BodyType = Field(default=BodyType.none, description='数据格式类型')
    request_headers: dict = {}
    extract: List[Union[Any]] = Field(default=[], title='提取参数')
    setup_hooks: List[Union[Any]] = Field(default=[], title='前置操作')
    teardown_hooks: List[Union[Any]] = Field(default=[], title='后置操作')
    variables: List[Union[Any]] = Field(default=[], title='变量参数')
    validators: List[Union[Any]] = Field(default=[], title='断言')
    create_time: Optional[datetime]=datetime.now()

class TestCaseList(BaseModel):
     totals: int=0
     case_list:List[TestCaseBase]

class CreateTestCase(BaseModel):
    case_name: str
    case_project_id: int
    case_module_id: int
    case_include_case_id: List[Union[str, int]] = Field(default=[], title='关联前置测试用例id')
    case_tag: Optional[str] = Field(default=None, title='用例标签')
    case_status: int = Field(default=1, title='用例状态 1生效 0失效')
    case_priority: Optional[int] = Field(default=3, title='用例优先级 ')
    request_type: Optional[int] = Field(default=1, title='case类型http 1 grap2xx')
    base_url: Optional[str]
    request_method: Optional[str]
    request_url: str
    request_body: Optional[Union[str]]
    request_body_type: BodyType = Field(default=BodyType.none, description='数据格式类型')
    request_headers: dict = {}
    extract: List[Union[Any]] = Field(default=[], title='提取参数')
    setup_hooks: List[Union[Any]] = Field(default=[], title='前置操作')
    teardown_hooks: List[Union[Any]] = Field(default=[], title='后置操作')
    variables: List[Union[Any]] = Field(default=[], title='变量参数')
    validators: List[Union[Any]] = Field(default=[], title='断言')


class UpdateTestCase(BaseModel):
    case_id: Optional[int]
    case_name: str
    case_project_id: int
    case_module_id: int
    case_include_case_id: List[Union[str, int]] = Field(default=[], title='关联前置测试用例id')
    case_tag: Optional[str] = Field(default=None, title='用例标签')
    case_status: int = Field(default=1, title='用例状态 1生效 0失效')
    case_priority: Optional[int] = Field(default=3, title='用例优先级 ')
    request_type: Optional[int] = Field(default=1, title='case类型http 1 grap2xx')
    base_url: Optional[str]
    request_method: Optional[str]
    request_url: str
    request_body: Optional[Union[str]]
    request_body_type: BodyType = Field(default=BodyType.none, description='数据格式类型')
    request_headers: dict = {}
    extract: List[Union[Any]] = Field(default=[], title='提取参数')
    setup_hooks: List[Union[Any]] = Field(default=[], title='前置操作')
    teardown_hooks: List[Union[Any]] = Field(default=[], title='后置操作')
    variables: List[Union[Any]] = Field(default=[], title='变量参数')
    validators: List[Union[Any]] = Field(default=[], title='断言')
    update_time: Optional[datetime]=datetime.now()

