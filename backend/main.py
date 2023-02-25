# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author： rainy
# datetime： 2021/11/30 18:24
# ide： PyCharm
import os

from fastapi import FastAPI, applications
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from starlette.staticfiles import StaticFiles
from backend.config.config import settings
from backend.apis.routers import api_router
from fastapi.openapi.docs import get_swagger_ui_html

app = FastAPI()
# windows
# app.mount('/static', StaticFiles(directory=os.path.join('C:\\Users\\sunxuan\\Desktop\\test_platform\\backend',
# 'static\\swagger-ui')),name='static'
##linux
app.mount('/static',
		  StaticFiles(directory=os.path.join('/Users/sunxuan/Documents/fast_platform/backend', 'static/swagger-ui')),
		  name='static')


def get_local_swagger(*args, **kwargs):
	'''获取本地swagger资源'''
	return get_swagger_ui_html(*args, **kwargs,
							   swagger_favicon_url='static/swagger-ui-3.52.5/dist/favicon-16x16.png',
							   swagger_css_url='static/swagger-ui-3.52.5/dist/swagger-ui.css',
							   swagger_js_url='static/swagger-ui-3.52.5/dist/swagger-ui-bundle.js')


applications.get_swagger_ui_html = get_local_swagger

# 允许跨域访问
if settings.BACKEND_CORS_ORIGIN:
	app.add_middleware(CORSMiddleware,
					   allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGIN],
					   allow_methods=['*'],
					   allow_headers=['*'],
					   allow_credentials=False
					   )
app.include_router(router=api_router, prefix=settings.API_PREFIX)
if __name__ == '__main__':
	# HOST 本地ip
	uvicorn.run(app='main:app', host='127.0.0.1', port=8400, reload=settings.RELOAD, debug=True)
