/*
 * @Author: error: git config user.name && git config user.email & please set dead value or install git
 * @Date: 2022-12-22 16:56:48
 * @LastEditors: error: git config user.name && git config user.email & please set dead value or install git
 * @LastEditTime: 2022-12-22 17:06:40
 * @FilePath: /front/src/api/test_case_data_manage.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
import request from '@/utils/request'
export function get_data_manage_by_env_id(env_id){
    return request({
        url:'/case_data_manage/get_data_manage_by_env_id',
        method:'get',
        params:{
            data_env_id: env_id
        }
    })
}

export function data_manage_insert(dataform){
    return request({
        url:'/case_data_manage/data_manage_insert',
        method:'post',
        data:dataform 
    })
}

export function data_manage_update(dataform){
    return request({
        url:'/case_data_manage/data_manage_update',
        method:'post',
        data: dataform
    })
}

