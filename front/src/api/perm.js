import request from '@/utils/request'

export function getPerms_by_filterdata(pageNo, pageSize, filterdata) {
  return request({
    url: '/perm/perm_lists',
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
export function addPerm(data) {
  return request({
    url: '/perm/add_perm',
    method: 'post',
    data: data
  })
}
export function editPerm(data) {
  return request({
    url: `/perm/edit_perm/${data.perm_id}`,
    method: 'post',
    data: data
  })
}
