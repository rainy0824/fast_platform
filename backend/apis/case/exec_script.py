# -*- coding: utf-8 -*-
# @Time    : 2023/1/13 22:46
# @Author  : sunxuan
# @Site    : //执行脚本
# @File    : exec_script.py
from fastapi import APIRouter,Body
from utils.response_code import resp_result
from backend.schemas.exec_script_schema import ScriptModel
exec_router=APIRouter()

@exec_router.post('/python_script',name='在线执行脚本')
async  def exec_python_script(script_data:ScriptModel):
    #             {
    #   "return_value": "gg",
    #   "hooks_code": "def test(x,y):\n    return x+y\ngg =test(10,2)"
    # }
    try:
     namespace={}
     exec(script_data.hooks_code,namespace)
     result =namespace.get(script_data.return_value)
     return resp_result(code=200,data=result,message='调试成功')
    except Exception as e:
        return f'调试出错:{e}'

