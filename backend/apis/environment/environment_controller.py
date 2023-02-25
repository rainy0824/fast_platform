#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2022/8/5 11:22 
# ide： PyCharm
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status,Body
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.sql import or_, func

from schemas.env_schema import CreateEnv, EnvList, EnvBase, UpdateEnv
from schemas.page_schema import Pages
from models.user.user_model import User
from models.env.environment_model import Environment
from starlette.responses import JSONResponse
from apis.permission.permission_controller import has_permission
from config.db import get_mysql_db
from utils.response_code import resp_result

environment_router = APIRouter()

@environment_router.post('/environment_list',response_model=EnvList,name='获取环境列表')
async  def get_environment_lists(pages:Pages,db: Session=Depends(get_mysql_db),
                                              user:User=Depends(has_permission('/env/get_env_lists'))):
    totals = db.query(func.count(Environment.environment_id)).scalar()
    envs = db.query(Environment).slice(pages.pagesize * (pages.pageno - 1), pages.pagesize * pages.pageno)
    env_lists=EnvList(**{
        "totals":totals,
        "envs":[EnvBase(**{
            "environment_id": env.environment_id,
            "environment_name":env.environment_name,
            "environment_desc":env.environment_desc,
            "environment_url":env.environment_url,
            "create_time":env.create_time
    }) for env in envs ]
    })
    return  env_lists


@environment_router.post('/add_environment',response_model=CreateEnv,name='添加环境')
async  def add_env(add_env:CreateEnv,db:Session=Depends(get_mysql_db),user:User=Depends(has_permission('/env/add_env'))):
    env_info =db.query(Environment).filter(or_(Environment.environment_name==add_env.environment_name)).first()
    if env_info:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='环境已存在,请重新输入')
    new_env =Environment(**{
        'environment_name':add_env.environment_name,
        'environment_url':add_env.environment_url,
        'environment_desc':add_env.environment_desc,

    })
    db.add(new_env)
    db.commit()
    return resp_result(code=200, data=jsonable_encoder(add_env), message='环境添加成功')

@environment_router.post('/update_environment',response_model=UpdateEnv,name='修改环境')
async  def update_env(update_env:UpdateEnv,env_id:int=Body(...),db:Session=Depends(get_mysql_db),user:User=Depends(has_permission('/env/update_env'))):
    env_info =db.query(Environment).filter(or_(Environment.environment_id==env_id)).first()
    if not env_info:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'id:{env_id}不存在')
    if update_env.environment_name is not None:
            env_info.environment_name = update_env.environment_name
    if update_env.environment_url is not None:
            env_info.environment_url = update_env.environment_url
    env_info.environment_desc=update_env.environment_desc
    env_info.update_time =datetime.now()
    db.add(env_info)
    db.commit()
    return  resp_result(code=200, data=jsonable_encoder(update_env), message='环境修改成功')

@environment_router.delete('/del_environment',name='删除环境')
async  def del_env(env_id:int,db:Session=Depends(get_mysql_db),user:User=Depends(has_permission('/env/del_env'))):
    env_info =db.query(Environment).filter(Environment.environment_id ==env_id).first()
    if not  env_info:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'id:{env_id}不存在')
    db.delete(env_info)
    db.commit()
    return  JSONResponse(content={'message': "数据删除成功", 'code': 200})

