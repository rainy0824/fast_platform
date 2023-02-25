#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2021/12/3 16:10 
# ide： PyCharm
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from models.user.user_model import User
from schemas.user_schema import Token
from config.db import get_mysql_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError

import jwt
from config.config import settings
from typing import Optional
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse

oauth2 = OAuth2PasswordBearer(tokenUrl='/api/login')
login_router = APIRouter()


def create_access_token(*, data: dict,expire_time: Optional[float] = None)->str:
    '''
    生成jwt token
    :param data: user info
    :param expire_time:  过期时间
    :return: jwt token str
    '''
    copy_data = data.copy()
    if expire_time:  # 有过期时间配置
        expire_time = datetime.utcnow() + timedelta(minutes=expire_time)
    else:
        expire_time = datetime.utcnow() + timedelta(minutes=15)
    #exp 是固定写法
    copy_data.update({'exp': expire_time})
    ##生成加密token
    # access_token = jwt.encode(payload=copy_data,key=settings.SECRET_KEY, algorithm=settings.ALGORITHM).decode('utf-8') //windows
    access_token = jwt.encode(payload=copy_data,key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    print(f'token is :{type(access_token),access_token}')
    return access_token

# create_access_token(data={'username':'admin'},expire_time=10)


def verify_user(username: str, password: str, db:Session):
    '''
    登录认证
    :param username: 用户名
    :param password: 明文密码
    :param db: session对象
    :return:
    '''
    print(f'verify_user:{type(db)}')
    user = get_user(username, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="账号或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # 验证密码
    if not user.verify_password(password):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="账号或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def get_user(username:str, db:Session):
    '''
    通过用户名查询用户
    :param db: session 对象
    :param usename: 用户名
    :return: userDB
    '''
    user = db.query(User).filter(User.username == username).first()
    return user


async def get_current_user(token: str = Depends(oauth2),db=Depends(get_mysql_db)):
    '''
    获取当前登录用户信息
    :param token: token str
    :return:
    '''
    auth_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='无效的认证',
                                   headers={'WWW-Authenticate': 'Bearer'})
    try:
        decode_token = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        username: str = decode_token.get('sub')
        if username is None:
            raise auth_exception
    except PyJWTError:
        raise auth_exception
    # new_db_session = await get_mysql_db()
    user = get_user(username,db)
    if not user:
        raise auth_exception
    return user


async def get_current_user_isactive(current_user: User = Depends(get_current_user)):
    '''
    获取用户当前状态是否可用
    :param current_user: User
    :return:
    '''
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='用户未激活')

    return current_user


@login_router.post('/login',response_model=Token,name='用户登录接口')
async def login_with_access_token(*, formdata: OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_mysql_db)):
    '''
    登录
    :param formdata: 表单提交数据 OAuth2PasswordRequestForm 类当做依赖参数
    :return: access_token
    '''
    user = verify_user(formdata.username, formdata.password,db)
    if not  user.is_active:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="账号未激活",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token=create_access_token(data={"sub":user.username},expire_time=settings.ACCESS_TOKEN_EXPIRE_TIME_MINUTES)

    return JSONResponse(content={'access_token':access_token,'token_type':'bearer','detail':"登录成功"},status_code=status.HTTP_200_OK)

@login_router.post('/logout',name='用户登出')
async  def logout():
    return  JSONResponse(content={'message':"退出登录"})

