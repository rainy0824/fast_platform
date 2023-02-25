#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2021/12/3 11:55 
# ide： PyCharm
from copy import deepcopy
from datetime import datetime

from fastapi.encoders import jsonable_encoder

from utils.response_code import resp_result
from utils.utils import time_handler
from fastapi import APIRouter, Depends, HTTPException, Request, status, Query, Body
from fastapi.responses import JSONResponse
from sqlalchemy.sql import or_, func
from backend.config.db import get_mysql_db
from sqlalchemy.orm import Session
from backend.models.user.user_model import User
from backend.schemas.user_schema import CreateUserIn, UserBase, AllUsers, UpdateUser, UserFilterDatas, CreateUserOut
from  backend.schemas.page_schema import Pages
from backend.models.menu.menu_model import Menu
from backend.models.role.role_model import RoleMenuRelation, RoleUserRelation
from apis.permission.permission_controller import has_permission
from pydantic import BaseModel
from typing import Set
from apis.login.login_controller import get_current_user_isactive

user_router = APIRouter()

@user_router.post('/create_user', name='添加用户',response_model=CreateUserIn,response_model_exclude={'password'})
async def create_user(user: CreateUserIn, db: Session = Depends(get_mysql_db),
                      current_user: User = Depends(has_permission('/users/create_user'))):
    '''
    添加用户信息
    :param request:
    :param user:  添加的用户信息
    :param db: session
    :param current_user: 当前登录用户
    :return:
    '''
    # 判断新用户是否已经存在
    userinfo = db.query(User).filter(or_(User.username == user.username, User.email == user.email)).first()
    if userinfo:  # 添加的用户信息已经存在
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='用户信息已经存在，请重新输入')
    user_dict = {
        'username': user.username,
        'email': user.email,
        'nickname': user.nickname,
        'avatar':user.avatar,
        'is_active': user.is_active
    }
    new_user = User(**user_dict)
    print(f'new_user:{new_user, type(new_user)}')
    new_user.hashed_password = new_user.general_hash_password(user.password)
    db.add(new_user)
    db.commit()
    # TODO: 添加操作记录
    # return JSONResponse(content={'message': '用户添加成功','code'=200},status_code=200)
    return  user
    # return  resp_result(code=200,data=jsonable_encoder(user),message='用户添加成功')
@user_router.get('/me', response_model=UserBase, name='获取当前用户详情')
async def get_me(user: User = Depends(get_current_user_isactive), db: Session = Depends(get_mysql_db)):
    menus_obj = db.query(Menu.menu_flag).join(RoleMenuRelation, RoleMenuRelation.menu_id == Menu.menu_id) \
        .join(RoleUserRelation, RoleMenuRelation.role_id == RoleUserRelation.role_id) \
        .filter(RoleUserRelation.user_id == user.user_id).all()
    menus = [menu.menu_flag for menu in menus_obj]
    print(f'menus:{menus}')
    user_dict = {
        'username': user.username,
        'email': user.email,
        'nickname': user.nickname,
        'is_active': user.is_active,
        'create_time':user.create_time,
        'menus': menus
    }
    return UserBase(**user_dict)


@user_router.get('/get_user_info', response_model=UserBase,response_model_exclude={"menus","create_time"}, name='获取指定用户信息')
async def get_userinfo(username: str, db: Session = Depends(get_mysql_db),
                       current_user: User = Depends(has_permission('/users/get_user_info'))):
    '''通过用户名获取用户信息
    :param request: request对象
    :param db: session 对象
    :param current_user: 操作人
    :return:
    '''
    user = db.query(User).filter(User.username == username).first()
    if user:
        user_dict = {
            'username': user.username,
            'email': user.email,
            'nickname': user.nickname,
            'is_active': user.is_active,
            'menus': [menu.menu_flag for menu in
                      db.query(Menu.menu_flag).join(RoleMenuRelation, RoleMenuRelation.menu_id == Menu.menu_id) \
                          .join(RoleUserRelation, RoleMenuRelation.role_id == RoleUserRelation.role_id) \
                          .filter(RoleUserRelation.user_id == user.user_id).all()],
            'create_time':user.create_time

        }
        return UserBase(**user_dict)
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='用户名不存在')


@user_router.post('/all_users_with_filterdata', response_model=AllUsers, name='根据查询条件获取用户列表信息')
async def get_all_users_with_filterdata(pages:Pages, filterdata: UserFilterDatas = Body(default=None),
                        db: Session = Depends(get_mysql_db),
                        current_user: User = Depends(has_permission('/users/all_users'))):
    '''
    :param pageno:当前页 第几页
    :param pagesize: 每页显示几条数据
    :param filterdata:查询参数
    :param db: session
    :param current_user: 当前登录用户
    :return: 1 10  2 10
    '''
    if filterdata:
        totals = db.query(func.count(User.user_id)).filter(
            or_(User.username == filterdata.username, filterdata.username == None ),
            or_(User.email == filterdata.email, filterdata.email == None),
            or_(User.nickname == filterdata.nickname, filterdata.nickname == None),
            or_(User.is_active == filterdata.is_active, filterdata.is_active == None)).scalar()

        users = db.query(User).filter(or_(User.username == filterdata.username, filterdata.username == None),
                                      or_(User.email == filterdata.email, filterdata.email == None),
                                      or_(User.nickname == filterdata.nickname, filterdata.nickname == None),
                                      or_(User.is_active == filterdata.is_active, filterdata.is_active == None)).slice(
            pages.pagesize * (pages.pageno - 1), pages.pagesize * pages.pageno)
        print(f'users对象类型:{type(users)}')
    else:
        totals = db.query(func.count(User.user_id)).scalar()
        users = db.query(User).slice(pages.pagesize * (pages.pageno - 1), pages.pagesize * pages.pageno)
    all_users =AllUsers(**{
        'totals': totals,
        'users': [UserBase(**{
            'username': user.username,
            'email': user.email,
            'nickname': user.nickname,
            'is_active': user.is_active,
            'menus': [menu.menu_flag for menu in
                      db.query(Menu.menu_flag).join(RoleMenuRelation, RoleMenuRelation.menu_id == Menu.menu_id) \
                           .join(RoleUserRelation, RoleMenuRelation.role_id == RoleUserRelation.role_id) \
                           .filter(RoleUserRelation.user_id == user.user_id).all()],
            'create_time':user.create_time
        }) for user in users]
    })
    return all_users


@user_router.get('/all_users', response_model=AllUsers, name='获取所有用户信息')
async def get_all_users(request:Request,pageno: int, pagesize: int, db: Session = Depends(get_mysql_db),
                        current_user: User = Depends(has_permission('/users/all_users'))):
    print(f'request信息:{request.url,request.query_params}')
    totals = db.query(func.count(User.user_id)).scalar()
    users = db.query(User).slice(pagesize * (pageno - 1), pagesize * pageno)
    print(f'时间类型：{type(users[0].create_time)},{users[0].create_time},')
    all_users = AllUsers(**{
        'totals': totals,
        'users': [UserBase(**{
            'username': user.username,
            'email': user.email,
            'nickname': user.nickname,
            'is_active': user.is_active,
            'create_time':user.create_time,
            'menus': [menu.menu_flag for menu in
                      db.query(Menu.menu_flag).join(RoleMenuRelation, RoleMenuRelation.menu_id == Menu.menu_id) \
                           .join(RoleUserRelation, RoleMenuRelation.role_id == RoleUserRelation.role_id) \
                           .filter(RoleUserRelation.user_id == user.user_id).all()]
        }) for user in users]
    })

    return all_users

@user_router.post('/update_user',name='修改用户信息')
async  def update_user(update_user:UpdateUser,db:Session=Depends(get_mysql_db),current_user:User=Depends(has_permission('/users/update_user'))):
        '''用户名不可以修改'''
        user=db.query(User).filter(User.username==update_user.username).first()
        if user:
            if update_user.password:
                user.general_hash_password(update_user.password)
            user.email =update_user.email
            user.is_active= update_user.is_active
            user.nickname=update_user.nickname
            user.update_time =datetime.now()
            db.add(user)
            db.commit()
            return JSONResponse(status_code=200,content={'message':"用户修改成功","code":200})
        else:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail='用户信息不存在')