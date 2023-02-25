# -*- coding: utf-8 -*-
# @Time    : 2022/11/2 23:11
# @Author  : sunxuan
# @Site    : 
# @File    : request_emus.py
from enum import IntEnum

class BodyType(IntEnum):
	'''
	请求参数类型
	'''
	none = 0
	json = 1
	form = 2
	x_form = 3
	graphQL = 4


class RequestType(IntEnum):
	http = 1
	grpc = 2
	dubbo = 3
	websocket = 4
