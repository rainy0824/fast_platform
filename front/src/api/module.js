/*
 * @Author: error: git config user.name && git config user.email & please set dead value or install git
 * @Date: 2022-09-23 14:40:55
 * @LastEditors: error: git config user.name && git config user.email & please set dead value or install git
 * @LastEditTime: 2022-12-19 23:40:29
 * @FilePath: /front/src/api/module.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
import request from '@/utils/request'

export  function get_module_lists(pageNo,pageSize,filter_data={}){
  return request({
    url: '/modules/module_lists',
    method: 'post',
    data:{
      pages:{
        pageno:pageNo, //注意key值与后端参数一致
        pagesize:pageSize
      },
      filter_data: filter_data
    }
  })
}

export function get_module_info(module_id){
  return request({
    url: '/modules/get_module_info',
    method:'post',
    params: {
      module_id: module_id
    }
  })
}

export function get_module_info_by_project_id(project_id){
  return request({
    url:'/modules/get_module_info_by_project_id',
    method:'post',
    params:{
      project_id:project_id
    }
  })
}



export  function add_module(module_data){
  return request({
    url: '/modules/add_module',
    method: 'post',
    data:module_data
  })
}

export  function edit_module(module_data){
  return request({
    url: '/modules/update_module',
    method: 'post',
    data: module_data
  })
}


export  function del_module(module_id){
  return request({
    url: '/modules/del_module',
    method: 'delete',
    params:{
      module_id:module_id
    }
  })
}

export function  module_list_to_tree(){

  return request({
    url:'/modules/module_list_to_tree_list',
    method:'get'
  })
}