# -*- coding: utf-8 -*-
# @Time    : 2022/12/21 22:52
# @Author  : sunxuan
# @Site    : 存放测试数据 ddt
# @File    : case_data_manage_controller.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from utils.response_code import resp_result
from sqlalchemy.orm import Session
from backend.config.db import get_mysql_db
from models.user.user_model import User
from models.case.case_data_manage_model import DataManageModel
from schemas.case_data_manage_schema import DataManageBase,CreateDataManage,UpdateDataManage
from models.env.environment_model import  Environment
case_data_manage_router=APIRouter()

@case_data_manage_router.get('/get_data_manage_by_env_id',name='获取测试数据')
async  def get_data_manage_by_env_id(data_env_id:int ,db:Session=Depends(get_mysql_db)):
    env_info = db.query(Environment).filter(Environment.environment_id ==data_env_id).first()
    if not env_info:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'该环境id:{data_env_id}不存在')
    data_info = db.query(DataManageModel).filter(DataManageModel.data_env_id ==data_env_id).first()
    if not data_info:
        data_list=[]
    else:
        data_list =DataManageBase(**{
            'data_id':data_info.data_id,
            'data_env_id':data_info.data_env_id,
            'data_name':data_info.data_name,
            'data_json':data_info.data_json
        })
    return  resp_result(code=200, data=jsonable_encoder(data_list))


@case_data_manage_router.post('/data_manage_insert',name='添加测试数据')
async def insert_test_data(add_data:CreateDataManage,db:Session=Depends(get_mysql_db)):
      env_info = db.query(Environment).filter(Environment.environment_id== add_data.data_env_id).first()
      if not env_info:
          raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='环境不存在，请维护环境配置后再试')
      data_info =db.query(DataManageModel).filter(DataManageModel.data_name==add_data.data_name).first()
      if data_info:
          raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='场景名称已经存在')
      new_data =DataManageModel(**{
          'data_env_id':add_data.data_env_id,
          'data_name':add_data.data_name,
          'data_json':add_data.data_json
      })
      db.add(new_data)
      db.commit()
      return  resp_result(code=200, data=jsonable_encoder(add_data), message='data添加成功')

@case_data_manage_router.post('/data_manage_update',name='修改测试数据')
async  def update_test_data(update_data:UpdateDataManage,db:Session=Depends(get_mysql_db)):
      env_info = db.query(Environment).filter(Environment.environment_id== update_data.data_env_id).first()
      if not env_info:
          raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'环境id:{update_data.data_env_id}不存在，请检查环境配置后再试')
      data_info =db.query(DataManageModel).filter(DataManageModel.data_id ==update_data.data_id).first()
      if not data_info:
          raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'dataid:{update_data.data_id}不存在')
      data_info.data_name =update_data.data_name
      data_info.data_env_id =update_data.data_env_id
      data_info.data_json =update_data.data_json
      db.add(data_info)
      db.commit()
      return  resp_result(code=200, data=jsonable_encoder(update_data), message='data修改成功')

@case_data_manage_router.delete('/data_manage_del',name='删除测试数据')
async  def del_test_data(data_id: int, db: Session = Depends(get_mysql_db)):
        data_info=db.query(DataManageModel).filter(DataManageModel.data_id ==data_id).firset()
        if not data_info:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'数据id{data_id}不存在')
        db.delete(data_info)
        db.commit()
        return JSONResponse(content={'message': "数据删除成功", 'code': 200})



