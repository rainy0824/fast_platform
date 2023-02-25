import request from '@/utils/request'

// 获取服务器列表
export function getServers_by_filter_data(pageNo, pageSize, filterdata) {
  return request({
    url: '/servers/server_lists',
    method: 'post',
    data: {
      pages: {
        pageno: pageNo,
        pagesize: pageSize
      },
      filterdata: filterdata
    }

  })
}

// 添加服务器信息
export function add_server(server_data){
  return request({
    url: '/servers/add_server',
    method: 'post',
    data: {
      server_name: server_data.server_name,
      server_ip: server_data.server_ip,
      server_desc: server_data.server_desc,
      server_login_name: server_data.server_login_name,
      server_iogin_pwd: server_data.server_login_pwd
    }
   })

}

//修改服务器信息
export function edit_server(server_data){
  return request({
    url: `/servers/edit_server/${server_data.server_id}`,
    method: 'post',
    data: server_data
  })
}

//删除服务器信息
export function delete_server(server_id){
  return request({
    url:'/servers/delete_server',
    method: 'delete',
    params: {
      server_id: server_id
    }
  })
}

//获取服务器详细信息
export function get_server_info(server_id){
  return request({
    url: `/servers/server_info/${server_id}`,
    method: 'get'
  })
}
