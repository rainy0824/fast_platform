import request from '@/utils/request'
export function getRoles() {
  return request({
    url: '/role/role_list',
    method: 'get'
  })
}
export function roleAdd(data) {
  return request({
    url: '/role/add_role',
    method: 'post',
    data: data
  })
}
export function getUsers(role_id) {
  return request({
    url: '/role/user_lists',
    params: role_id
  })
}
export function getMenus(data) {
  return request({
    url: '/role/menu_lists',
    params: data
  })
}
export function getPerms(data) {
  return request({
    url: '/role/perm_lists',
    params: data
  })
}
export function submitUsers(data) {
  return request({
    url: '/role/edit_users',
    method: 'post',
    data: data
  })
}
export function submitPerms(data) {
  return request({
    url: '/role/edit_perms',
    method: 'post',
    data: data
  })
}
export function submitMenus(data) {
  return request({
    url: '/role/edit_menus',
    method: 'post',
    data: data
  })
}
