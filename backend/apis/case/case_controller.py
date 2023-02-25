#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2022/8/16 16:47 
# ide： PyCharm

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from apis.module.module_controller import get_module_info
from apis.permission.permission_controller import has_permission
from apis.project.project_controller import get_project_info
from backend.config.db import get_mysql_db
from backend.schemas.case_schema import CreateTestCase, TestCaseBase, TestCaseList, UpdateTestCase
from models.case.case_model import TestCase
from models.user.user_model import User
from schemas.page_schema import Pages
from utils.response_code import resp_result

case_router = APIRouter()


# 调用非fastapi的方法时，需要将session传入
async def get_module_name(module_id, db: Session):
    module_info = await get_module_info(module_id, db)
    return module_info.module_name


async def get_project_name(project_id, db: Session):
    project_info = await  get_project_info(project_id, db)
    return project_info.project_name


@case_router.post('/get_case_lists_by_filter_data', response_model=TestCaseList, name='获取所有case信息')
async def get_case_lists(pages: Pages=None, filter_data: dict = {}, db: Session = Depends(get_mysql_db),
                         user: User = Depends(has_permission('/testcase/get_case_list'))):
    if len(filter_data) > 0:
        query = db.query(TestCase)
        for attr, value in filter_data.items():
            query = query.filter(getattr(TestCase, attr) == value)
        if pages is not  None: #分页
            cases = query.slice(pages.pagesize * (pages.pageno - 1), pages.pagesize * pages.pageno)
            totals = cases.with_entities(func.count(TestCase.case_id)).scalar()
        else:
            cases =query.all()
            totals =len(cases)
    else:
        totals = db.query(func.count(TestCase.case_id)).scalar()
        cases = db.query(TestCase).slice(pages.pagesize * (pages.pageno - 1), pages.pagesize * pages.pageno)
    case_lists = TestCaseList(**{
        "totals": totals,
        "case_list": [TestCaseBase(**{
            "case_id": case.case_id,
            "case_name": case.case_name,
            "case_project_id": case.case_project_id,
            "case_project_name": await get_project_name(case.case_project_id, db),
            "case_module_id": case.case_module_id,
            "case_module_name": await get_module_name(case.case_module_id, db),
            "case_include_case_id": case.case_include_case_id,
            "case_tag": case.case_tag,
            "case_status": case.case_status,
            "case_priority": case.case_priority,
            "request_type": case.request_type,
            "base_url": case.base_url,
            "request_method": case.request_method,
            "request_url": case.request_url,
            "request_body": case.request_body,
            "request_body_type": case.request_body_type,
            "request_headers": case.request_headers,
            "extract": case.extract,
            "setup_hooks": case.setup_hooks,
            "teardown_hooks": case.teardown_hooks,
            "variables": case.variables,
            "validators": case.validators,
            "create_time": case.create_time
        }) for case in cases]
    })
    return resp_result(code=200, data=jsonable_encoder(case_lists))


@case_router.post('/add_case', name='添加case')
async def add_case(new_case: CreateTestCase, db: Session = Depends(get_mysql_db),
                   user: User = Depends(has_permission('/testcase/add_case'))):
    case_info = db.query(TestCase).filter(TestCase.case_name == new_case.case_name).first()
    if case_info:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='case名称已经存在')
    new_case_info = TestCase(**{
        "case_name": new_case.case_name,
        "case_status": new_case.case_status,
        "case_tag": new_case.case_tag,
        "case_priority": new_case.case_priority,
        "case_module_id": new_case.case_module_id,
        "case_project_id": new_case.case_project_id,
        "case_include_case_id": new_case.case_include_case_id,
        "request_type": new_case.request_type,
        "base_url": new_case.base_url,
        "request_method": new_case.request_method,
        "request_url": new_case.request_url,
        "request_body": new_case.request_body,
        "request_body_type": int(new_case.request_body_type),
        "request_headers": new_case.request_headers,
        "setup_hooks": new_case.setup_hooks,
        "teardown_hooks": new_case.teardown_hooks,
        "variables": new_case.variables,
        "extract": new_case.extract,
        "validators": new_case.validators
    })
    db.add(new_case_info)
    db.commit()
    return resp_result(code=200, data=jsonable_encoder(new_case), message='case添加成功')


@case_router.post('/update_case', name='修改case')
async def update_case(update_test_case: UpdateTestCase, db: Session = Depends(get_mysql_db),
                      user: User = Depends(has_permission('/testcase/update_case'))):
    case_info = db.query(TestCase).filter(TestCase.case_id == update_test_case.case_id).first()
    if not case_info:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='case不存在')
    case_info.case_name = update_test_case.case_name
    case_info.case_status = update_test_case.case_status
    case_info.case_tag = update_test_case.case_tag
    case_info.case_priority = update_test_case.case_priority
    case_info.case_module_id = update_test_case.case_module_id
    case_info.case_project_id = update_test_case.case_project_id
    case_info.case_include_case_id = update_test_case.case_include_case_id
    case_info.request_type = update_test_case.request_type
    case_info.base_url = update_test_case.base_url
    case_info.request_method = update_test_case.request_method
    case_info.request_url = update_test_case.request_url
    case_info.request_body = update_test_case.request_body
    case_info.request_body_type = int(update_test_case.request_body_type)
    case_info.request_headers = update_test_case.request_headers
    case_info.setup_hooks = update_test_case.setup_hooks
    case_info.teardown_hooks = update_test_case.teardown_hooks
    case_info.variables = update_test_case.variables
    case_info.extract = update_test_case.extract
    case_info.validators = update_test_case.validators
    case_info.update_time = datetime.now()
    db.add(case_info)
    db.commit()
    return resp_result(code=200, data=jsonable_encoder(update_test_case), message='case修改成功')
