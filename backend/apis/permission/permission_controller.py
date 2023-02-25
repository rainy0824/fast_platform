#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2021/12/3 16:10 
# ide： PyCharm
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request,status

from sqlalchemy.orm import Session
from sqlalchemy.sql import or_,func
from starlette.responses import JSONResponse

from config.db import get_mysql_db

from apis.login.login_controller import get_current_user_isactive
from models.role.role_model import RolePermissionRelation, RoleUserRelation
from models.user.user_model import User
from models.permission.permisson_model import Permission
from  schemas.page_schema import  Pages
from schemas.permission_schema import PermFilterDatas
from schemas.role_schema import PermissionList,PermissionBase
perm_router = APIRouter()

def has_permission(interface: str):
    '''
    验证用户是否有权限
    :param interface:接口地址
    :return:
    '''
    def check_user_permission(currrent_user: User = Depends(get_current_user_isactive),
                              db: Session = Depends(get_mysql_db)):
        # 查询角色下的用户id 是否拥有权限
        # select role_user.id from role_user
        # join role_permission on role_user.role_id=role_permission
        # join pemission on role_permission.permission_id=permission.perm_id
        # where permission.perm_interface ='/xxxx'
        users = db.query(RoleUserRelation.user_id).join(RolePermissionRelation, RoleUserRelation
                                                        .role_id == RolePermissionRelation.role_id) \
            .join(Permission, Permission.perm_id == RolePermissionRelation.permission_id) \
            .filter(Permission.perm_interface == interface).all()
        #获取所有拥有xx权限接口的用户id
        users_id:list = [user.user_id for user in users]
        if currrent_user.user_id in users_id:
            return  currrent_user
        else:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail=f'用户没有{interface}权限')
    return check_user_permission

@perm_router.post('/perm_lists',response_model=PermissionList,name='获取权限列表信息')
async  def get_perm_lists_with_filterdata(pages:Pages,filterdata:PermFilterDatas=None,db:Session=Depends(get_mysql_db),
                                          current_user:User=Depends(has_permission('/perm/perm_lists'))):
    if filterdata.perm_name:
        totals = db.query(func.count(Permission.perm_id)).filter(
            or_(Permission.perm_name == filterdata.perm_name, Permission.perm_name == None)).scalar()

        perms = db.query(Permission).filter(or_(Permission.perm_name == filterdata.perm_name, Permission.perm_name == None),
                                 ).slice(
            pages.pagesize * (pages.pageno - 1), pages.pagesize * pages.pageno)
    else:
        totals = db.query(func.count(Permission.perm_id)).scalar()
        perms = db.query(Permission).slice(pages.pagesize * (pages.pageno - 1), pages.pagesize * pages.pageno)

    return PermissionList(**{
        "totals":totals,
        "perms":[PermissionBase(**{
                "perm_id":perm.perm_id,
                "perm_name":perm.perm_name,
                "perm_interface":perm.perm_interface
        })for perm in perms]
    })

@perm_router.post('/add_perm',name='添加权限')
async  def add_perm(perm:PermissionBase,db:Session=Depends(get_mysql_db),current_user:User=Depends(has_permission('/perm/add_perm'))):
        perm_info =db.query(Permission).filter(Permission.perm_name==perm.perm_name).first()
        if perm_info:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='权限名称已经存在，请重新输入')
        new_perm = Permission(**{
                "perm_name": perm.perm_name,
                "perm_interface":perm.perm_interface
            })
        db.add(new_perm)
        db.commit()
        return JSONResponse(content={'message': '权限添加成功', 'code': 200})


@perm_router.post('/edit_perm/{perm_id}',name='修改权限')
async  def edit_perm(perm_id:str,edit_perm:PermissionBase,db:Session=Depends(get_mysql_db),current_user:User=Depends(has_permission('/perm/edit_perm'))):
        perm_info =db.query(Permission).filter(Permission.perm_id==int(perm_id)).first()
        if not perm_info:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'权限id:{perm_id}不存在')
        is_exist_perm_name =db.query(Permission).filter(Permission.perm_name ==edit_perm.perm_name).first()
        if perm_info.perm_name !=edit_perm.perm_name:
            if is_exist_perm_name: #不为none
                    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'权限名称已存在，请重新输入')
            perm_info.perm_name =edit_perm.perm_name
        is_exist_perm_interface = db.query(Permission).filter(Permission.perm_interface == edit_perm.perm_interface).first()
        if perm_info.perm_interface !=edit_perm.perm_interface:
            if is_exist_perm_interface:  # 不为none
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'权限接口已存在，请重新输入')
            perm_info.perm_interface = edit_perm.perm_interface
        perm_info.update_time=datetime.now()
        db.add(perm_info)
        db.commit()
        return JSONResponse(content={'message': '权限修改成功', 'code': 200})