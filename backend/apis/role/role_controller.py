#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2021/12/3 16:10 
# ide： PyCharm
from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.responses import JSONResponse
from sqlalchemy.sql import or_, func
from backend.config.db import get_mysql_db
from sqlalchemy.orm import Session
from models.role.role_model import Role, RoleUserRelation, RoleMenuRelation, RolePermissionRelation
from models.user.user_model import User
from models.permission.permisson_model import Permission
from  models.menu.menu_model import Menu
from apis.permission.permission_controller import has_permission
from schemas.role_schema import RoleBase,RoleList,RoleUsers,RoleEditPermission,RoleEditUsers,RoleMenus,RoleEditMenus,RolePermission,RoleEditBase

role_router = APIRouter()


@role_router.get('/role_list/',response_model=RoleList,name='角色列表信息')
async def role_list(db: Session = Depends(get_mysql_db), current_user: User = Depends(has_permission(('/role/list')))):
    roles = db.query(Role, func.count(RoleUserRelation.user_id).label('user_counts')) \
        .outerjoin(RoleUserRelation, RoleUserRelation.role_id == Role.role_id) \
        .group_by(Role, Role.role_name).all()
    totals =db.query(func.count(Role.role_id)).scalar()
    role_lists = RoleList(**
        {
        "totals":totals,
        "roles": [
            RoleBase(
                **{"role_name": role.Role.role_name,
                   "role_desc": role.Role.role_name,
                   "role_id": role.Role.role_id,
                   "user_counts":role.user_counts
                   }) for role in roles
        ]
    }
    )
    return role_lists

@role_router.post('/add_role',name='添加角色')
async  def add_role(newrole:RoleBase,db:Session=Depends(get_mysql_db),current_user:User=Depends(has_permission('/role/add_role'))):
    # 判断角色是否存在
    role_info =db.query(Role).filter(or_(Role.role_name == newrole.role_name)).first()
    if role_info:
        raise  HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='角色已经存在，请重新输入')
    new_role =Role(**{
        "role_name":newrole.role_name,
        "role_desc":newrole.role_desc
    })
    db.add(new_role)
    db.commit()
    return JSONResponse(content={"code":200,"message":"角色添加成功"})

@role_router.get('/user_lists',response_model=RoleUsers,name='角色下用户管理')
async  def get_user_lists(role_id:str,db:Session=Depends(get_mysql_db),current_user:User=Depends(has_permission('/role/user_lists'))):
    #判断角色id是否存在
    role_info = db.query(Role).filter(Role.role_id == int(role_id)).first()  # 通过角色id查询role表是否存在该角色
    if not role_info:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'角色id:{role_id}不存在')
    #该role_idd下的用户
    role_bind_users =db.query(User.user_id).join(RoleUserRelation,RoleUserRelation.user_id==User.user_id).filter(RoleUserRelation.role_id ==int(role_id)).all()
    #所有用户
    role_users=[{"key":str(user.user_id),"label":user.username}for user in db.query(User).all()]
    return RoleUsers(**{
        "users":role_users,
        "choose_users":[str(role_user.user_id) for role_user in role_bind_users]
    })


@role_router.post('/edit_users',name='修改角色下用户')
async  def edit_users(edit_user:RoleEditUsers,db:Session=Depends(get_mysql_db)):
    role_id = int(edit_user.role_id)
    role_info = db.query(Role).filter(Role.role_id == role_id).first()  # 通过角色id查询role表是否存在该角色
    if not role_info:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'角色id:{role_id}不存在')
    #清除角色下原有用户
    db.query(RoleUserRelation).filter(RoleUserRelation.role_id==role_id).delete()
    #重新绑定用户
    for user_id in edit_user.users:
        new_user_id =int(user_id)
        user_info =db.query(User).filter(User.user_id==new_user_id).first()
        if not user_info:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'用户id:{new_user_id}不存在')
        role_user_relations=RoleUserRelation(**{
            "role_id":role_id,
            "user_id":new_user_id
        })
        db.add(role_user_relations)
    db.commit()
    return JSONResponse(content={"code": 200, "message": "角色下用户修改成功"})

@role_router.get('/perm_lists',name='角色下所有权限')
async  def get_perm_lists(role_id:str,db:Session=Depends(get_mysql_db),current_user:User=Depends(has_permission('/role/perm_lists'))):
    role_info = db.query(Role).filter(Role.role_id==int(role_id)).first()
    if not role_info:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'角色id:{role_id}不存在')
    # role_id 下绑定的权限
    role_bind_perms=db.query(Permission.perm_id).join(RolePermissionRelation,RolePermissionRelation.permission_id ==Permission.perm_id).filter(RolePermissionRelation.role_id==int(role_id)).all()

    perms =[{"key":pem.perm_id,"label":pem.perm_name}for pem in db.query(Permission).all()]
    return  RolePermission(**{
        "perms":perms,
        "choose_perms":[str(role_pem.perm_id)for role_pem in role_bind_perms]
    })

@role_router.post('/edit_perms',name='修改角色下权限')
async  def role_perms_edit(perms_edit:RoleEditPermission,db:Session=Depends(get_mysql_db),current_user:User=Depends(has_permission('/role/edit_perms'))):
    """
    RoleEditPermission:角色权限关联信息
    """
    role_id =int(perms_edit.role_id)
    role_info =db.query(Role).filter(Role.role_id ==role_id).first()  #通过角色id查询role表是否存在该角色
    if not role_info:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'角色id:{role_id}不存在')
     #清除角色对应的权限
    db.query(RolePermissionRelation).filter(RolePermissionRelation.role_id == role_id).delete()
    for new_perms_id in perms_edit.perms:
        new_perms_id=int(new_perms_id)
        perms_info =db.query(Permission).filter(Permission.perm_id==new_perms_id).first()
        if not perms_info:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'权限id:{new_perms_id}不存在')
        new_role_perms_relation = RolePermissionRelation(**{
            "role_id":role_id,
            "permission_id":new_perms_id
        })
        db.add(new_role_perms_relation)
    db.commit()
    return JSONResponse(content={"code":200,"message":"角色下权限修改成功"})

@role_router.get('/menu_lists',name='角色下所有菜单')
async  def get_menu_lists(role_id:str,db:Session=Depends(get_mysql_db),current_user:User=Depends(has_permission('/role/menu_lists'))):
    # 判断角色id是否存在
    role_info = db.query(Role).filter(Role.role_id == int(role_id)).first()  # 通过角色id查询role表是否存在该角色
    if not role_info:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'角色id:{role_id}不存在')
    menus =[{"key":menu.menu_id,"label":menu.menu_name}for menu in db.query(Menu).all()]
    #角色下绑定的菜单
    role_bind_menus =db.query(Menu.menu_id).join(RoleMenuRelation,RoleMenuRelation.menu_id ==Menu.menu_id).filter(RoleMenuRelation.role_id==int(role_id)).all()
    return RoleMenus(**{
        "menus":menus,
        "choose_menus":[str(role_menu.menu_id) for role_menu in role_bind_menus]
    })

@role_router.post('/edit_menus',name='修改角色下菜单权限')
async def role_menus_edit(munu_edit:RoleEditMenus,db:Session=Depends(get_mysql_db),current_user:User=Depends(has_permission('/role/edit_menus'))):
    role_id =int(munu_edit.role_id)
    # 判断角色id是否存在
    role_info = db.query(Role).filter(Role.role_id == int(role_id)).first()  # 通过角色id查询role表是否存在该角色
    if not role_info:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'角色id:{role_id}不存在')
    # 删除角色下所有菜单
    db.query(RoleMenuRelation).filter(RoleMenuRelation.role_id == role_id).delete()
    # 绑定新的菜单
    for new_menu_id in munu_edit.menus:
        new_menu_id =int(new_menu_id)
        menu_info =db.query(Menu).filter(Menu.menu_id==new_menu_id).first()
        if not menu_info:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'菜单id:{menu_info}不存在')
        role_menu_relation=RoleMenuRelation(**{
            "role_id":role_id,
            "menu_id":new_menu_id
        })
        db.add(role_menu_relation)
    db.commit()
    return JSONResponse(content={"code":200,"message":"角色下菜单修改成功"})
