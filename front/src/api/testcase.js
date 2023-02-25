/*
 * @Author: error: git config user.name && git config user.email & please set dead value or install git
 * @Date: 2022-12-17 16:28:13
 * @LastEditors: error: git config user.name && git config user.email & please set dead value or install git
 * @LastEditTime: 2022-12-26 21:42:58
 * @FilePath: /front/src/api/testcase.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
import request from '@/utils/request'
export function get_case_lists_by_filter_data(pageNo,pageSize,filter_data={}){
    return request({
        url: '/case/get_case_lists_by_filter_data',
        method: 'post',
        data:{
          pages:{
            pageno:pageNo,
            pagesize:pageSize
          },
          filter_data:filter_data
        }
      })
}
export function get_case_lists_by_filter_data_with_no_pages(filter_data={}) {
    return request({
        url: '/case/get_case_lists_by_filter_data',
        method: 'post',
        data:{
          filter_data:filter_data
        }
      })
}
