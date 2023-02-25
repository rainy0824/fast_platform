/*
 * @Author: error: git config user.name && git config user.email & please set dead value or install git
 * @Date: 2022-09-23 14:40:55
 * @LastEditors: error: git config user.name && git config user.email & please set dead value or install git
 * @LastEditTime: 2022-12-19 20:00:38
 * @FilePath: /front/src/api/project.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
import request from '@/utils/request'

//获取项目列表/分页
export function getProjects_by_filter_data(pageNo, pageSize, filter_data={}){
  return request({
    url: '/projects/get_project_lists_with_filterdata',
    method: 'post',
    data: {
      pages: {
        pageno: pageNo,
        pagesize: pageSize
      },
      filter_data: filter_data
    }

  })

}
//不带参数获取所有项目
export function get_all_project_list(){
  return request({
    url:'/projects/get_all_project_list',
    method:'get'
  })
}



//添加项目
export function addProject(project_data){
  return request({
    url: '/projects/add_project',
    method: 'post',
    data: project_data
    // data: {
    //   project_name: project_data.project_name,
    //   project_desc: project_data.project_desc,
    //   project_manager: project_data.project_manager,
    //   developer: project_data.developer,
    //   tester: project_data.tester,
    //   project_status: project_data.project_status
    // }
  })
}

//修改项目
export function updateProject(project_id,project_data){
  return request({
    url: '/projects/update_project',
    method: 'post',
    data:{
      update_project:project_data,
      project_id: project_id
    }

    // data:{
    //   update_project:{
    //   project_name: project_data.project_name,
    //   project_desc: project_data.project_desc,
    //   project_manager: project_data.project_manager,
    //   developer: project_data.developer,
    //   tester: project_data.tester,
    //   project_status: project_data.project_status
    //   },
    //   project_id: project_id
    // }
  })
}

//获取项目详情
export function getProjectInfo(project_id){
  return request({
    url: `/projects/get_project_info/${project_id}`,
    method: 'get'
  })
}

