#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2021/12/2 16:15 
# ide： PyCharm
from pydantic import  BaseModel,Field

from typing import  Optional,List
class RoleBase(BaseModel):
    '''角色基本信息'''
    role_id:Optional[str]
    role_name:str=Field(title='角色名')
    role_desc:str
    user_counts:Optional[int]=Field(title='用户数')

class RoleList(BaseModel):
    totals: int
    roles:List[RoleBase]=Field(default=[],description='所有角色')

class RoleEditUsers(BaseModel):
    '''修改角色下关联用户'''
    role_id:str
    users:List[str]
class RoleEditBase(BaseModel):
    '''查询用户基础模型'''
    key:str=Field(title='用户/菜单/权限id')
    label:str=Field(title='用户/菜单/权限描述')

class RoleUsers(BaseModel):
    '''角色下所有用户'''
    users:List[RoleEditBase]=Field(default=[],description='所有用户')
    choose_users:List[str]=Field(default=[],description='角色对应的用户')
class PermissionBase(BaseModel):
    '''权限基础模型'''
    perm_id:Optional[str]=None
    perm_name:str
    perm_interface:str

class PermissionList(BaseModel):
    '''权限列表'''
    totals:int
    perms:List[PermissionBase]

class RolePermission(BaseModel):
    "角色下所有权限"
    perms:List[RoleEditBase]=Field(default=[],description='所有权限')
    choose_perms:List[str]=Field(default=[],description='角色对应的权限')

class RoleEditPermission(BaseModel):
    '''修改权限模型'''
    role_id:str=Field(title='角色id')
    perms:List[str]=Field(title='角色所对应的权限')

class RoleMenus(BaseModel):
    menus:List[RoleEditBase]=Field(default=[],description='所有菜单')
    choose_menus:List[str]=Field(default=[],description='角色下对应菜单')

class RoleEditMenus(BaseModel):
    role_id:str
    menus:List[str]=Field(title='角色所对应的菜单')




