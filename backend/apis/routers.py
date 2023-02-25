#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2021/12/2 14:24 
# ide： PyCharm
#URL路由配置
from  fastapi import  APIRouter
from  backend.apis.user.user_controller import user_router
from  backend.apis.role.role_controller import role_router
from  backend.apis.menu.menu_controller import menu_router
from  backend.apis.permission.permission_controller import perm_router
from  backend.apis.login.login_controller import login_router
from  backend.apis.server.server_controller import server_router
from  backend.apis.project.project_controller import project_router
from  backend.apis.environment.environment_controller import environment_router
from  backend.apis.module.module_controller import module_router
from  backend.apis.httptest.http_controller import http_router
from  backend.apis.case.case_controller import case_router
from  backend.apis.case.case_data_manage_controller import  case_data_manage_router
from  backend.apis.case.exec_script import  exec_router
api_router =APIRouter()
api_router.include_router(login_router,tags=['login'])
api_router.include_router(user_router,prefix='/users',tags=['users'])
api_router.include_router(perm_router,prefix='/perm',tags=['perm'])
api_router.include_router(role_router,prefix='/role',tags=['role'])
api_router.include_router(menu_router,prefix='/menu',tags=['menu'])
api_router.include_router(server_router,prefix='/servers',tags=['servers'])
api_router.include_router(project_router,prefix='/projects',tags=['projects'])
api_router.include_router(environment_router,prefix='/envs',tags=['envs'])
api_router.include_router(module_router,prefix='/modules',tags=['modules'])
api_router.include_router(http_router,prefix='/request',tags=['request'])
api_router.include_router(case_router,prefix='/case',tags=['case'])
api_router.include_router(case_data_manage_router,prefix='/case_data_manage',tags=['case_data_manage'])
api_router.include_router(exec_router,prefix='/online',tags=['online'])





