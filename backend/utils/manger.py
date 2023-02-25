#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2021/12/3 15:02 
# ide： PyCharm
#创建管理员账号
from hashlib import  md5
import  requests

class ManagerHandler:
    def __init__(self,username,password,real_name):
        self.username=username
        self.password =password
        self.real_name =real_name

    def create_superadmin(self,account,password,real_name,session,rand_m5,email,dept_id:int=1):
        user_password =md5(password.encoded()).hexdigest()+rand_m5
