#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2022/2/23 16:25 
# ide： PyCharm
from datetime import datetime
from threading import Thread
import  asyncio
import  paramiko #sshclient
from fastapi import APIRouter, Depends, HTTPException, status,Body,WebSocket
from sqlalchemy.orm import Session
from sqlalchemy.sql import or_, func
from schemas.page_schema import Pages
from schemas.server_schema import ServerFilterdata,ServerList,ServerBase,UpdateServer
from models.user.user_model import User
from models.server.server_model import Server
from starlette.responses import JSONResponse
from apis.permission.permission_controller import has_permission
from config.db import get_mysql_db

server_router = APIRouter()


@server_router.post('/add_server',name='添加服务器')
async  def add_server(add_server:ServerBase,db:Session=Depends(get_mysql_db),current_user:User=Depends(has_permission('/server/add_server'))):
     server_info =db.query(Server).filter(Server.server_name ==add_server.server_name).first()
     if server_info:
         raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail='服务器名称已经存在')
     new_server=Server(**{
         'server_name':add_server.server_name,
         'server_desc':add_server.server_desc,
         'server_ip':add_server.server_ip,
         'server_port':add_server.server_port
     })
     if add_server.server_login_name:
          new_server.server_login_name=add_server.server_login_name
     if add_server.server_login_pwd:
         new_server.server_login_pwd=add_server.server_login_pwd
     db.add(new_server)
     db.commit()
     return JSONResponse(content={'message': '数据添加成功', 'code': 200})


@server_router.post('/server_lists',response_model=ServerList,name='获取所有服务器列表数据')
async def get_server_lists_with_filterdata(pages: Pages, filterdata: ServerFilterdata=Body(default=None),
                                           db: Session = Depends(get_mysql_db),
                                           current_user: User = Depends(has_permission('/server/server_lists'))):
    if filterdata:
        totals = db.query(func.count(Server.server_id)).filter(
            or_(Server.server_name == filterdata.server_name, filterdata.server_name == None),
            or_(Server.server_ip == filterdata.server_ip, filterdata.server_ip == None)
        ).scalar()
        servers = db.query(Server).filter(
            or_(Server.server_name == filterdata.server_name, filterdata.server_name == None),
            # or_(Server.server_name == filterdata.server_name, filterdata.server_name == None),
            ).slice(pages.pagesize * (pages.pageno - 1), pages.pagesize * pages.pageno)
    else:
        totals = db.query(func.count(Server.server_id)).scalar()
        servers = db.query(Server).slice(pages.pagesize *(pages.pageno-1),pages.pagesize*pages.pageno)

    server_list =ServerList(**{
        "totals":totals,
        "servers":[ServerBase(**{
            "server_id":server.server_id,
            "server_name":server.server_name,
            "server_ip":server.server_ip,
            "server_port":server.server_port,
            "server_desc":server.server_desc,
            "create_time":server.create_time,
            "server_login_name":server.server_login_name,
            "server_login_pwd":server.server_login_pwd
        }) for server in servers]
    })
    return  server_list

@server_router.get('/server_info/{server_id}',name='获取服务器详细信息')
async  def get_server_info(server_id:str,db:Session=Depends(get_mysql_db),current_user:User=Depends(has_permission('/server/server_info'))):
    server= db.query(Server).filter(Server.server_id==int(server_id)).first()
    if not server:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'服务器server_id:{server_id}不存在')
    server_info = ServerBase(**{
            "server_id":server.server_id,
            "server_name":server.server_name,
            "server_ip":server.server_ip,
            "server_port":server.server_port,
            "server_desc":server.server_desc,
            "create_time":server.create_time,
            "server_login_name":server.server_login_name,
            "server_login_pwd":server.server_login_pwd
    })
    return server_info

@server_router.post('/edit_server/{server_id}',name='修改服务器信息')
async  def edit_server(server_id:str,edit_server:UpdateServer,db:Session=Depends(get_mysql_db),current_user:User=Depends(has_permission('/server/edit_server'))):
    server_info =db.query(Server).filter(Server.server_id==int(server_id)).first()
    if not server_info:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'服务器server_id:{server_id}不存在')
    if edit_server.server_name:
         server_info.server_name =edit_server.server_name
    if edit_server.server_desc:
        server_info.server_desc =edit_server.server_desc
    if edit_server.server_ip:
        server_info.server_ip =edit_server.server_ip
    if edit_server.server_port:
        server_info.server_port =edit_server.server_port
    if edit_server.server_login_name:
        server_info.server_login_name =edit_server.server_login_name
    if edit_server.server_login_pwd:
        server_info.server_login_pwd =edit_server.server_login_pwd
    server_info.update_time =datetime.now()
    db.add(server_info)
    db.commit()
    return JSONResponse(content={"message":'数据修改成功','code':200})

@server_router.delete('/delete_server',name='删除服务器信息')
async  def delete_server(server_id:str,db:Session=Depends(get_mysql_db),current_user:User=Depends(has_permission('/server/delete_server'))):
    server_info =db.query(Server).filter(Server.server_id==int(server_id)).first()
    if not server_info:
        raise  HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail=f'server_id:{server_id}不存在')
    db.delete(server_info)
    db.commit()
    return  JSONResponse(content={'message':"数据删除成功",'code':200})

@server_router.websocket('/web_terminal',name='网页版终端')
async  def web_ssh(websocket:WebSocket,server_ip:str,server_port:str,server_login_name:str,server_login_pwd:str):
    await  websocket.accept()
    #实例化
    web_ssh_client =paramiko.SSHClient()
    web_ssh_client.load_system_host_keys()
    web_ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    web_ssh_client.connect(server_ip,int(server_port),server_login_name,server_login_pwd)
    transport = web_ssh_client.get_transport()
    chan = transport.open_session()
    chan.get_pty(term='ansi', width=80, height=40)
    chan = web_ssh_client.invoke_shell()
    async def send_ssh():
        try:
            while True:
                result = chan.recv(2048).decode('utf-8')
                await websocket.send_text(result)
        except Exception:
            pass
    # 初次连接，有两条信息返回，一个是上次登录信息，一个是默认信息
    for i in range(2):
        login_data = chan.recv(2048).decode('utf-8')
        await websocket.send_text(login_data)
    # 启动多线程接收ssh返回的信息
    Thread(target=asyncio.run, args=(send_ssh(),)).start()
    Thread(target=asyncio.run, args=(send_ssh(),)).start()
    try:
        while True:
            # 监听前端传递的信息，传送给ssh
            data = await websocket.receive_text()
            chan.send(data)
    except Exception as ex:
        print(f"websocket closed:{str(ex)}")
        await websocket.close()
        web_ssh_client.close()



