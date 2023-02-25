#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2021/12/2 14:16 
# ide： PyCharm
#处理数据库连接

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker
#mysql数据库地址
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@192.168.0.53:3306/fast_platform"
# 创建mysql engine
db_engine = create_engine(SQLALCHEMY_DATABASE_URL,encoding='utf8', echo=True)

# 创建session会话
db_session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)


#db mananger
class DBContextManager:
    def __init__(self):
        print('__init__被调用了...')
        self.db = db_session()
    def __enter__(self):
        print('__enter__被调用了...')
        return  self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('__exit__被调用了...')
        self.db.close()


async  def get_mysql_db():
    with DBContextManager() as  db:
        yield  db
