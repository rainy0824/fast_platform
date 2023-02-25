#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2022/6/16 11:58 
# ide： PyCharm
from datetime import datetime

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.sql import func, or_
from starlette.responses import JSONResponse
from apis.permission.permission_controller import has_permission
from backend.config.db import get_mysql_db
from models.project.project_model import Project
from models.user.user_model import User
from schemas.page_schema import Pages
from schemas.project_schema import CreateProject, ProjectBase, Project_List, UpdateProject
from utils.response_code import resp_result

project_router = APIRouter()


@project_router.post('/get_project_lists_with_filterdata', response_model=Project_List, name='获取所有项目列表信息/分页')
async def get_project_lists_with_filterdata(pages: Pages,filter_data:dict,
                                            db: Session = Depends(get_mysql_db),
                                            current_user: User = Depends(has_permission('/project/project_lists'))):
    # if filterdata:
    #     if filterdata.project_name or filterdata.project_manager :
    #         totals = db.query(func.count(Project.project_id)).filter(
    #             or_(Project.project_name == filterdata.project_name),
    #             and_(Project.project_manager == filterdata.project_manager)
    #         ).scalar()
    #         projects = db.query(Project).filter(
    #             or_(Project.project_name == filterdata.project_name),
    #             and_(Project.project_manager == filterdata.project_manager)
    #         ).slice(pages.pagesize * (pages.pageno - 1), pages.pagesize * pages.pageno)
    #     else:
    #         totals = db.query(func.count(Project.project_id)).scalar()
    #         projects = db.query(Project).slice(pages.pagesize * (pages.pageno - 1), pages.pagesize * pages.pageno)
    # else:
    #     totals = db.query(func.count(Project.project_id)).scalar()
    #     projects = db.query(Project).slice(pages.pagesize * (pages.pageno - 1), pages.pagesize * pages.pageno)
    # not_null_filters = []
    # if filterdata:
    #     if filterdata.project_name:
    #         not_null_filters.append(Project.project_name.ilike(filterdata.project_name))
    #     if filterdata.project_manager:
    #         not_null_filters.append(Project.project_name.ilike(filterdata.project_manager))
    #     if filterdata.project_status:
    #         not_null_filters.append(Project.project_name.bool_op(filterdata.project_status))
    #     if len(not_null_filters) > 0:
    #         projects = db.query(Project).filter(*not_null_filters).slice(pages.pagesize * (pages.pageno - 1),
    #                                                                          pages.pagesize * pages.pageno)
    #         totals =projects.with_entities(func.count(*not_null_filters)).scalar()
    if len(filter_data)>0:
        query =db.query(Project)
        for attr,value in filter_data.items():
            query =query.filter(getattr(Project,attr)==value)
        if pages is not None:
            projects =query.slice(pages.pagesize * (pages.pageno - 1), pages.pagesize * pages.pageno)
            totals =projects.with_entities(func.count(Project.project_id)).scalar()
        else:
            projects =query.all()
            totals =len(projects)
    else:
        totals = db.query(func.count(Project.project_id)).scalar()
        projects = db.query(Project).slice(pages.pagesize * (pages.pageno - 1), pages.pagesize * pages.pageno)
    projects_list = Project_List(**{
        "totals": totals,
        "projects": [ProjectBase(**{
            'project_id': project.project_id,
            'project_name': project.project_name,
            'project_desc': project.project_desc,
            'project_manager': project.project_manager,
            'tester': project.tester,
            'developer': project.developer,
            'project_status': project.project_status,
            'create_time': project.create_time
        }) for project in projects]
    })
    return projects_list

@project_router.get('/get_all_project_list',name='获取所有项目')
async def get_all_project_list(db:Session=Depends(get_mysql_db),current_user: User = Depends(has_permission('/project/project_lists'))):
    totals = db.query(func.count(Project.project_id)).scalar()
    projects = db.query(Project).all()
    projects_list = Project_List(**{
        "totals": totals,
        "projects": [ProjectBase(**{
            'project_id': project.project_id,
            'project_name': project.project_name,
            'project_desc': project.project_desc,
            'project_manager': project.project_manager,
            'tester': project.tester,
            'developer': project.developer,
            'project_status': project.project_status,
            'create_time': project.create_time
        }) for project in projects]
    })
    return projects_list






##查看项目详细信息
@project_router.get('/get_project_info/{project_id}', response_model=ProjectBase, name='查看项目详细信息')
async def get_project_info(project_id: int, db: Session = Depends(get_mysql_db),
                           current_user: User = Depends(has_permission('/project/project_info'))):
    pj_info = db.query(Project).filter(Project.project_id == int(project_id)).first()
    if not pj_info:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f':项目id:{project_id}不存在')
    return ProjectBase(**{
        'project_id': pj_info.project_id,
        'project_name': pj_info.project_name,
        'project_desc': pj_info.project_desc,
        'project_manager': pj_info.project_manager,
        'tester': pj_info.tester,
        'developer': pj_info.developer,
        'project_status': pj_info.project_status,
        'create_time': pj_info.create_time
    })


##添加项目
@project_router.post('/add_project', name='添加项目')
async def add_project(add_project: CreateProject, db: Session = Depends(get_mysql_db),
                      current_user: User = Depends(has_permission('/project/add_project'))):
    if len(add_project.project_name.strip())>0:
        project_info = db.query(Project).filter(or_(Project.project_name == add_project.project_name)).first()
        if project_info:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='项目名称已存在')
        new_project = Project(**{
            'project_name': add_project.project_name,
            'project_desc': add_project.project_desc,
            'project_manager': add_project.project_manager,
            'developer': add_project.developer,
            'tester': add_project.tester,
            'project_status': add_project.project_status,
        })
        db.add(new_project)
        db.flush() #刷新获取project_Id
        db.commit()

        data=ProjectBase(**{
            'project_id': new_project.project_id,
            'project_name': new_project.project_name,
            'project_desc': new_project.project_desc,
            'project_manager': new_project.project_manager,
            'developer': new_project.developer,
            'tester': new_project.tester,
            'project_status': new_project.project_status,
            'create_time':new_project.create_time
        })
        return resp_result(code=200, data=jsonable_encoder(data), message='项目添加成功')
    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='项目名称不能为空')



@project_router.post('/update_project', name='修改项目', response_model=ProjectBase)
async def update_project(update_project: UpdateProject, project_id: str = Body(...),
                         db: Session = Depends(get_mysql_db),
                         current_user: User = Depends(has_permission('/project/update_project'))):
    if len(update_project.project_name.strip())>0:
        query_project_name = db.query(Project).filter(or_(Project.project_name == update_project.project_name)).first()
        if query_project_name:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='项目名称已存在')
        query_project = db.query(Project).filter(or_(Project.project_id == int(project_id))).first()
        if not query_project:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f':项目id:{project_id}不存在')
        if update_project.project_name is not None:
            query_project.project_name = update_project.project_name
        if update_project.project_desc is not None:
            query_project.project_desc = update_project.project_desc
        if update_project.project_manager is not None:
            query_project.project_manager = update_project.project_manager
        if update_project.developer is not None:
            query_project.developer = update_project.developer
        if update_project.tester is not None:
            query_project.tester = update_project.tester
        if update_project.project_status is not None:
            query_project.project_status = update_project.project_status
        query_project.update_time = datetime.now()
        db.add(query_project)
        db.flush()
        db.commit()
        result_data = ProjectBase(**{
            'project_id': query_project.project_id,
            'project_name': query_project.project_name,
            'project_desc': query_project.project_desc,
            'project_manager': query_project.project_manager,
            'developer': query_project.developer,
            'tester': query_project.tester,
            'project_status': query_project.project_status,
            'create_time': query_project.create_time

        })
        return resp_result(code=200, data=jsonable_encoder(result_data), message='项目修改成功')
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='项目名称不能为空')

@project_router.delete('/del_project', name='删除模块')
async def del_project(project_id:str,db: Session = Depends(get_mysql_db),
                         current_user: User = Depends(has_permission('/project/update_project'))):
    project_info = db.query(Project).filter(Project.project_id == int(project_id)).first()
    if not project_info:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'id:{project_id}不存在')
    db.delete(project_info)
    db.commit()
    return JSONResponse(content={'message': "数据删除成功", 'code': 200})