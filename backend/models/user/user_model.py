#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2021/12/2 15:31 
# ide： PyCharm
# 用户模型

from models.model_base import Base
from sqlalchemy import Column, String, Boolean, DateTime, BigInteger
from datetime import  datetime
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
class User(Base):
    '''用户表'''
    __tablename__ ='user'
    __table_args__ = {'extend_existing':True}
    user_id = Column(BigInteger(),primary_key=True,unique=True,index=True,autoincrement=True)
    username =Column(String(30),nullable=False,unique=True,index=True,comment='用户名')
    nickname =Column(String(30),nullable=True,comment='昵称')
    avatar =Column(String(200),nullable=True,comment='头像')
    email =Column(String(30),nullable=False,comment='邮箱')
    hashed_password =Column(String(200),nullable=False,comment='加密密码')
    is_active =Column(Boolean(),default=True,comment='是否激活')
    create_time =Column(DateTime(),default=datetime.now,comment='创建时间')
    update_time =Column(DateTime(),default=datetime.now,onupdate=datetime.now,comment='最后一次更新时间')

    # hash加密
    def general_hash_password(self,password: str):
        print(f'{pwd_context.hash(password)}')
        self.hashed_password= pwd_context.hash(password)
        return  self.hashed_password
    # 验证hash密码
    def verify_password(self,origin_password) -> bool:
        '''
        :param origin_password: 明文密码
        :return:
        '''
        result =pwd_context.verify(origin_password, self.hashed_password)
        return result
    def __repr__(self):
        return f'username:{self.username}'


