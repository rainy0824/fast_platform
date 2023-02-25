import request from '@/utils/request'

export function get_env_lists(pageNo,pageSize){

  return request({
    url: '/envs/environment_list',
    method: 'post',
    data:{
      pages:{
        pageNo:pageNo,
        pageSize:pageSize
      }
    }
  })
}

export function add_Env(env_data)
{
  return request({
    url: '/envs/add_environment',
    method: 'post',
    data: env_data
  })
}

export function edit_Env(env_id,env_data)
{
  return request({
    url: '/envs/update_environment',
    method: 'post',
    data: {
      update_env: env_data,
      env_id:env_id
    }
  })
}


export function del_Env(env_id)
{
  return request({
    url: '/envs/del_environment',
    method: 'delete',
    params:{
      env_id: env_id
    }
  })
}
