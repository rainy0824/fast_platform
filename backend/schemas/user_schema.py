#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2021/12/2 15:30 
# ide： PyCharm
from  datetime import datetime

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List


class UserBase(BaseModel):
    '''用户基础信息'''
    username: str
    email: EmailStr
    is_active: Optional[bool] = True
    nickname: str = None
    avatar: str = 'https://upfile.asqql.com/2009pasdfasdfic2009s305985-ts/2020-6/2020678493837817.gif'
    menus: Optional[List[str]]=[]
    create_time: datetime=None

    class Config:
        schema_exa = {
            'username': 'evan',
            'email': 'evan@qq.com',
            'is_active': True,
            'nickname': 'evan',
            'avatar': '1111',
            'menus':[]
        }


class CreateUserIn(UserBase):
    '''#添加用户'''
    password: str
class CreateUserOut(UserBase):
    '''#不暴露用户密码'''



class UpdateUser(UserBase):
    '''修改用户信息'''
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    nickname: Optional[str]
    is_active: Optional[bool] = True


class Token(BaseModel):
    '''token 信息'''
    access_token: str
    token_type: str


class AllUsers(BaseModel):
    '''所有用户'''
    totals: int = Field(default=0, title='用户总数')
    users: List[UserBase] = Field(default=[], title='所有用户信息')

    class Config:
        schema_exa = {'total': 20, 'users': [{
            'username': 'evan',
            'email': 'evan@qq.com',
            'is_active': True,
            'nick_name': 'evan',
            'avatar': '1111'
        }]}

class UserFilterDatas(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    nickname: Optional[str] = None
    is_active: Optional[bool] = None


