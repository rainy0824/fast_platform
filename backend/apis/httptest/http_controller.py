#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2022/9/22 16:13 
# ide： PyCharm //api test
from fastapi import Depends, APIRouter, HTTPException, status
from backend.apis.httptest.AsyncHttpRequest import AsyncHttpRequest
from  backend.schemas.httptest_schema import CreateHttpRequest,UpdateHttpRequest,HttpRequestBase
from utils.response_code import resp_result
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from starlette.responses import JSONResponse
from backend.config.db import get_mysql_db
from sqlalchemy.orm import Session
from sqlalchemy.sql import or_, func
from models.user.user_model import User
from apis.permission.permission_controller import has_permission
from models.httptest.http_model import HttpRequestModel

http_router=APIRouter()
@http_router.post('/send_http',name='http调试')
async  def send_http_request(data:CreateHttpRequest):
	'''debug http'''
	try:
		http_request_instance = await  AsyncHttpRequest.handle_client(data.url,data.body_type,body=data.body,headers=data.headers)
		result =await http_request_instance.aio_request(data.method)
		print(f'result:,{result}')
		if result.get('status'):#请求发送成功
			return resp_result(code=200,data=jsonable_encoder(result),message='异步请求发送成功')
		return{ 'code':500,'message':'异步请求发送失败','data':result}
	except Exception as e:
		return  f'请求错误:{e}'

@http_router.post('/add_http',name='添加http请求')
async  def add_http(http_request:CreateHttpRequest,db:Session=Depends(get_mysql_db)):
			add_request=HttpRequestModel(**{
				"request_method":http_request.method,
				"request_body":http_request.body,
				"request_url":http_request.url,
				"request_body_type":int(http_request.body_type),
				"request_headers":http_request.headers
			})
			db.add(add_request)
			db.commit()
			return resp_result(code=200, data=jsonable_encoder(http_request), message='http请求添加成功')
@http_router.post('/update_http',name='修改http请求')
async  def update_http(update_request:UpdateHttpRequest,db:Session=Depends(get_mysql_db)):
		request_info=db.query(HttpRequestModel).filter(HttpRequestModel.request_id==update_request.id).first()
		if not request_info:
			raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f':id:{update_request.id}不存在')
		request_info.request_method=update_request.method
		if not update_request.url.startswith('http'):
		       #TODO 不是绝对路径，就把environment中的url加进来
		       pass
		request_info.request_url=update_request.url
		request_info.request_body=update_request.body
		request_info.request_body_type=int(update_request.body_type)
		request_info.request_headers =update_request.headers
		request_info.update_time =datetime.now()
		db.add(request_info)
		db.commit()
		request_data =HttpRequestBase(**{
			'request_id':request_info.request_id,
			"request_method": request_info.request_method,
			"request_url": request_info.request_url,
			"request_body": request_info.request_body,
			"request_body_type":request_info.request_body_type,
			"request_headers": request_info.request_headers,
			"update_time":request_info.update_time

		})
		return  resp_result(code=200,data=jsonable_encoder(request_data),message="修改成功")

