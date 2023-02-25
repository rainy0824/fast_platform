#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2021/12/2 14:19 
# ide： PyCharm
from typing import List
from  pydantic import  AnyHttpUrl
class Settings:
    '''配置信息'''
    API_PREFIX ='/api'
    # openssl rand -hex 32 生成随机秘钥
    SECRET_KEY = '08ec78ff975652027463d86ee0379e6f953128ea6370abe69dd9be1aaaa408f8'
    # 加密算法HS256
    ALGORITHM = 'HS256'
    # 过期时间
    ACCESS_TOKEN_EXPIRE_TIME_MINUTES = 30
    #热加载
    RELOAD =True
    #跨域白名单
    BACKEND_CORS_ORIGIN:List[AnyHttpUrl]=['http://localhost:9528','http://127.0.0.1:8888']

settings =Settings()