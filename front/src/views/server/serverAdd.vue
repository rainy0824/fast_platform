<template>
<!--添加服务器界面-->
<div class="app-container">
    <el-form ref="servers" :model="servers" :rules="form_rules" label-position="right" label-width="200px">
    <el-form-item label="服务器名称" prop="server_name" label-width="40%">
      <el-input v-model="servers.server_name" style="width: 400px" />
    </el-form-item>
    <el-form-item label="服务器描述" prop="server_desc" label-width="40%">
      <el-input v-model="servers.server_desc" type="textarea" style="width: 400px" />
    </el-form-item>
    <el-form-item label="服务器ip" prop="server_ip" label-width="40%">
      <el-input v-model="servers.server_ip" style="width: 400px" />
    </el-form-item>
    <el-form-item label="服务器登录名" prop="server_login" label-width="40%">
      <el-input v-model="servers.server_login_name" style="width: 400px" />
    </el-form-item>
    <el-form-item label="服务器登录密码" prop="server_login_pwd" label-width="40%">
      <el-input v-model="servers.server_login_pwd" style="width: 400px" show-password />
    </el-form-item>
      <el-form-item label-width="40%">
      <el-button type="primary" round @click="addServer"  >确 定</el-button>
      <el-button type="info" round @click="cancel">取 消</el-button>
    </el-form-item>
    </el-form>
</div>
</template>

<script>

import { validateIp } from '@/utils/validate'
import { add_server }  from '@/api/server'

export default {
  name: 'AddServer',
  components: {},
  props: {},
  data() {
    const validate_ip = (rule,value,callback) =>{

      if (!validateIp(value)){
        callback(new Error(""))
      }
      callback()
    }
    return {
      loading: false ,
      servers: {
        server_name: '',
        server_desc: '',
        server_ip: '',
        server_login_name: '',
        server_login_pwd: ''
      },
      form_rules: {
        server_name: [
          { required: true, message: '请输入服务器名称', trigger: 'blur' },
          { min: 3, max: 25, message: '长度在 3 到 25 个字符', trigger: 'blur'}
        ],
        server_desc: [
          { required: true, message: '请输入服务器描述', trigger: 'blur' },
          { min: 1, max: 200, message: '长度在200个字符内', trigger: 'blur' }
        ],
        server_ip: [
          { required: true, message: '请输入服务器ip', trigger: 'blur' },
          { min:16, max: 16, message: 'ip地址格式不正确"', trigger: 'blur', validator: validate_ip}
        ],
        server_port: [
          { required: false, message: '请输入服务器端口', trigger: 'blur' }
        ],
        server_login_name: [
          { required: false, message: '请输入服务器登录名', trigger: 'blur' }
        ],
        server_login_pwd: [
          { required: false, message: '请输入服务器登录密码', trigger: 'blur' },

        ]
      }
    }
  },
  watch: {},
  computed: {},
  methods: {
    cancel() {
      this.$router.go(-1)
    },
    // addServer() {
    //   this.$refs.servers.validate(vaild =>{
    //     console.log(vaild)
    //     if(vaild){
    //       this.loading =true
    //       this.$store.dispatch('myserver/add_Server',this.servers)
    //       .then(() =>
    //       {
    //       this.$router.push({name: 'servermannage'})
    //       this.loading =false
    //       })
    //       .catch(()=>{
    //         this.loading=false
    //       })
    //     }
    // })}

    addServer()
    {
      this.$refs.servers.validate(valid =>
      {
        console.log(valid)
        if (valid){
            this.loading =true
            add_server(this.servers)
            .then((response) =>{
              this.$router.push({name: 'ServerList'})
              this.loading =false
              this.$message.success(response.message)
            }).catch(()=>{
              this.loading =false
            })
          }
      })

    }

    }


}

</script>
