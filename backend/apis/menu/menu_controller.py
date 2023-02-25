#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2022/2/16 16:57 
# ide： PyCharm
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.sql import or_, func
from backend.config.db import get_mysql_db
from sqlalchemy.orm import Session

from models.menu.menu_model import Menu
from models.user.user_model import User
from apis.permission.permission_controller import has_permission
from schemas.menu_schema import MenuBase
from common.funcs.common_func import  list_to_tree
menu_router = APIRouter()





# def get_menus(parent_id, all_menus, all_parent_ids):
#     child_menus = []
#     child_menus_dicts = []
#     for menu in all_menus:
#         if menu.parent_id == parent_id:
#             child_menus.append(menu)
#     for child_menu in child_menus:
#         # 判断有没有子菜单
#         child_menus_dict = {"menu_id": str(child_menu.menu_id), "menu_name": child_menu.menu_name}
#         if child_menu.menu_id in all_parent_ids:
#             child_menus_dict["children"] = get_menus(child_menu.menu_id, all_menus, all_parent_ids)
#         child_menus_dicts.append(child_menus_dict)
#     if len(child_menus) == 0:
#         return
#     return child_menus_dicts


@menu_router.get('/menu_lists', name='获取所有菜单列表')
async def get_menu_lists(db: Session = Depends(get_mysql_db),
                         current_user: User = Depends(has_permission('/menu/menu_lists'))):
    # menu_list = []
    # all_menus = db.query(Menu).all()
    # parent_menus =db.query(Menu).filter(Menu.parent_id ==0).all()
    # #获取所有父级菜单id
    # all_parent_ids = [menu.parent_id for menu in db.query(Menu.parent_id).distinct().all()]
    # for parent_menu in parent_menus:
    #     parent_menus_dict ={
    #         "menu_id":parent_menu.menu_id,
    #         "menu_name":parent_menu.menu_name
    #     }
    #     if parent_menu.menu_id in all_parent_ids: #有子菜单就添加子菜单信息
    #         parent_menus_dict["children"]=get_menus(parent_menu.menu_id, all_menus, all_parent_ids)
    #     menu_list.append(parent_menus_dict)
    # return JSONResponse({"menus": menu_list})
    all_menus = db.query(Menu).all()
    all_menus_list = [{"menu_id": menu.menu_id, "menu_name": menu.menu_name, "parent_id": menu.parent_id} for menu in
                      all_menus]
    menu_list = list_to_tree(all_menus_list)
    return JSONResponse({"code": 200, "menus": menu_list})


@menu_router.post('/add_menu', name='添加菜单')
async def add_menu(menu: MenuBase, db: Session = Depends(get_mysql_db),
                   current_user: User = Depends(has_permission(('/menu/add_menu')))):
    old_menu_info = db.query(Menu).filter(or_(Menu.menu_name == menu.menu_name, Menu.menu_flag == menu.menu_flag)).first()
    if old_menu_info:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='菜单名称或接口已经存在，请重新输入')
    if menu.parent_id !='0':#选了父id
        if db.query(Menu).filter(Menu.menu_id == menu.parent_id).first():
            new_menu = Menu(**{"menu_name": menu.menu_name, "menu_flag": menu.menu_flag, "parent_id": menu.parent_id})
        else:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'父id：{menu.parent_id}不存在')
    else:#父id不存在 默认父id就为0 menu.parnt_id=0
        new_menu = Menu(**{"menu_name": menu.menu_name, "menu_flag": menu.menu_flag,"parent_id":menu.parent_id})
    db.add(new_menu)
    db.commit()
    return JSONResponse(content={"code": 200, "message": "菜单添加成功"})


@menu_router.post('/edit_menu', name='修改菜单')
async def edit_menu(menu: MenuBase, db: Session = Depends(get_mysql_db),
                    cureent_user: User = Depends(has_permission('/menu/edit_menu'))):
    old_menu_info = db.query(Menu).filter(Menu.menu_id == int(menu.menu_id)).first()
    if not old_menu_info:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'菜单id:{menu.menu_id}不存在')
    if menu.parent_id:
        if db.query(Menu).filter(Menu.parent_id == old_menu_info.parent_id).first():
            old_menu_info.parent_id = menu.parent_id
        else:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'父信息id：{menu.parent_id}不存在')
    if menu.menu_id ==menu.parent_id:
         raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'父id：{menu.parent_id}不能与当前id:{menu.menu_id} 相同')
    if old_menu_info.menu_name != menu.menu_name:
        if db.query(Menu).filter(Menu.menu_name == menu.menu_name).first():
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'菜单名称:{menu.menu_name}已经存在，请重新输入')
        old_menu_info.menu_name = menu.menu_name
    if old_menu_info.menu_flag != menu.menu_flag:
        if db.query(Menu).filter(Menu.menu_flag == menu.menu_flag).first():
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'菜单标识:{menu.menu_flag}已经存在，请重新输入')
        old_menu_info.menu_flag = menu.menu_flag
    old_menu_info.update_time = datetime.now()
    db.add(old_menu_info)
    db.commit()
    return JSONResponse(content={"code": 200, "message": "菜单信息修改成功"})


@menu_router.get('/get_menu_info', name='查询菜单信息')
async def get_menu_info(menu_id: str, db: Session = Depends(get_mysql_db),
                        current_user: User = Depends(has_permission('/menu/get_menu_info'))):
    menu_info = db.query(Menu).filter(Menu.menu_id == int(menu_id)).first()
    if not menu_info:
        raise HTTPException(status_code=406, detail=f'查询菜单id:{menu_id}不存在')
    return MenuBase(**{
        "menu_name": menu_info.menu_name,
        "menu_flag": menu_info.menu_flag,
        "parent_id": menu_info.parent_id,
        "menu_id": menu_info.menu_id})

