#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2022/8/11 15:42 
# ide： PyCharm
from datetime import datetime

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.sql import func, or_
from starlette.responses import JSONResponse

from apis.permission.permission_controller import has_permission
from backend.config.db import get_mysql_db
from models.module.module_model import Module
from models.project.project_model import Project
from models.user.user_model import User
from schemas.module_schema import CreateModule, ModuleBase, ModuleList, UpdateMoule
from schemas.page_schema import Pages
from utils.response_code import resp_result
from  common.funcs.common_func import  list_to_tree

module_router = APIRouter()


@module_router.post('/module_lists', name='获取所有模块列表')
async def get_module_lists(pages: Pages,filter_data:dict={}, db: Session = Depends(get_mysql_db),
                           user: User = Depends(has_permission('/module/module_lists'))):
    if len(filter_data)>0:
        query =db.query(Module)
        for attr,value in filter_data.items():
            query =query.filter(getattr(Module,attr)==value)
        modules =query.slice(pages.pagesize * (pages.pageno - 1), pages.pagesize * pages.pageno)
        totals =modules.with_entities(func.count(Module.project_id)).scalar()
    else:
        totals = db.query(func.count(Module.module_id)).scalar()
        modules = db.query(Module).slice(pages.pagesize * (pages.pageno - 1), pages.pagesize * pages.pageno)
    module_lists = ModuleList(**{
        "totals": totals,
        "modules": [ModuleBase(**{
            "module_id": module.module_id,
            "module_name": module.module_name,
            "module_manager": module.module_manager,
            "module_desc": module.module_desc,
            "module_project_id": module.module_project_id,
            "module_project_name": "".join([project_name for project_name in db.query(Project.project_name) \
                                           .join(Module, Module.module_project_id == Project.project_id) \
                                           .filter(Module.module_id == module.module_id).first()]),
            "parent_module_id":module.parent_module_id,
            "create_time": module.create_time
        }) for module in modules]
    })
    return module_lists
@module_router.get('/module_list_to_tree_list',name='生成树形结构模块')
async  def module_lists_to_tree_list(db: Session = Depends(get_mysql_db)):
     all_modules =db.query(Module).all()
     module_lists =[{"module_id":module.module_id,"module_name":module.module_name,"parent_module_id":module.parent_module_id} for module in all_modules]
     tree_lists =list_to_tree(module_lists)
     return JSONResponse({"code": 200, "module_tree_lists": tree_lists})

@module_router.post('/get_module_info',name='通过module_id获取模块信息')
async  def get_module_info(module_id:int ,db:Session=Depends(get_mysql_db)):
        module_info = db.query(Module).filter(Module.module_id==module_id).first()
        return module_info

@module_router.post('/get_module_info_by_project_id',name='通过project_id 获取模块')
async  def get_module_info_by_project_id(project_id:int,db:Session=Depends(get_mysql_db)):
    module_info =db.query(Module).filter(Module.module_project_id==project_id).all()
    return module_info

@module_router.post('/add_module', name='添加模块')
async def add_module(add_module: CreateModule, db: Session = Depends(get_mysql_db),
                     user: User = Depends(has_permission(('/module/add_module')))):
    module_info = db.query(Module).filter(or_(Module.module_name == add_module.module_name)).first()
    project_info = db.query(Project).filter(Project.project_id == add_module.module_project_id).first()
    if module_info:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='模块已经存在')
    if project_info is None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f'关联的项目id:{add_module.module_project_id}不存在')
    if add_module.parent_module_id != 0:  # 有父模块id 非一级模块
        if db.query(Module).filter(Module.module_id == add_module.parent_module_id).first():  # 有值则父模块存在
            new_module = Module(**{
                "parent_module_id": add_module.parent_module_id,
                "module_name": add_module.module_name,
                "module_manager": add_module.module_manager,
                "module_desc": add_module.module_desc,
                "module_project_id": add_module.module_project_id
            })
        else:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail=f'所选父id：{add_module.parent_module_id}不存在')
    else:  ##父模块id不存在 默认父模块id就为0 add_module.parent_module_id=0
        new_module = Module(**{
            "parent_module_id": add_module.parent_module_id,
            "module_name": add_module.module_name,
            "module_manager": add_module.module_manager,
            "module_desc": add_module.module_desc,
            "module_project_id": add_module.module_project_id
        })
    db.add(new_module)
    db.commit()
    return resp_result(code=200, data=jsonable_encoder(add_module), message='模块添加成功')


@module_router.post('/update_module', name='修改模块')
async def update_module(update_module: UpdateMoule, db: Session = Depends(get_mysql_db),
                        user: User = Depends(has_permission('/module/update_module'))):
    module_info = db.query(Module).filter(Module.module_id == int(update_module.module_id)).first()
    project_info = db.query(Project).filter(Project.project_id == update_module.module_project_id).first()
    if not module_info:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'id:{module_info.module_id}不存在')
    if module_info.module_id  == update_module.parent_module_id:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f'父id：{update_module.parent_module_id}不能与当前id:{module_info.module_id} 相同')
    if update_module.parent_module_id !=0: #模块为非一级菜单
        if db.query(Module).filter(
                Module.module_id == update_module.parent_module_id).first():  # 更新提交来的parent_module_id存在
            module_info.parent_module_id = update_module.parent_module_id
        else:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'所选父id:{update_module.parent_module_id}不存在')
    else: #模块为一级菜单parent_module_id=0
        module_info.parent_module_id = update_module.parent_module_id
    if module_info.module_name is not None:
        module_info.module_name = update_module.module_name
    if module_info.module_project_id is not None:
        if project_info is None:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail=f'关联的项目id:{update_module.module_project_id}不存在')
        module_info.module_project_id = update_module.module_project_id
    module_info.module_manager = update_module.module_manager
    module_info.module_desc = update_module.module_desc
    module_info.update_time = datetime.now()
    db.add(module_info)
    db.commit()
    return resp_result(code=200, data=jsonable_encoder(update_module), message='模块修改成功')


@module_router.delete('/del_module', name='删除模块')
async def del_module(module_id: str, db: Session = Depends(get_mysql_db),
                     user: User = Depends(has_permission('/module/del_module'))):
    module_info = db.query(Module).filter(Module.module_id == int(module_id)).first()
    if not module_info:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'id:{module_id}不存在')
    db.delete(module_info)
    db.commit()
    return JSONResponse(content={'message': "数据删除成功", 'code': 200})

