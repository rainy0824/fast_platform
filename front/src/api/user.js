import request from '@/utils/request'
import qs from 'qs'

export function login(data) {
  return request({
    url: '/login',
    method: 'post',
    headers: {
      'Content-type': 'application/x-www-form-urlencoded'
    },
    data: qs.stringify(data)
  })
}

export function getInfo() {
  return request({
    url: '/users/me',
    method: 'get'
  })
}

export function logout() {
  return request({
    url: '/logout',
    method: 'post'
  })
}

export function edit(data) {
  return request({
    url: '/users/update_user',
    method: 'post',
    data: {
      username: data.username,
      password: data.password,
      email: data.email,
      is_active: data.is_active,
      nickname: data.nickname
    }
  })
}

export function getUsers(pageNo, pageSize) {
  return request({
    url: '/users/all_users',
    method: 'get',
    params: {
      pageno: pageNo,
      pagesize: pageSize
    }
  })
}

// 带查询条件
export function getUsers_by_filter_data(pageNo, pageSize, filterdata) {
  return request({
    url: '/users/all_users_with_filterdata',
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
