<!--
 * @Author: error: git config user.name && git config user.email & please set dead value or install git
 * @Date: 2022-09-23 14:40:55
 * @LastEditors: error: git config user.name && git config user.email & please set dead value or install git
 * @LastEditTime: 2022-12-10 02:30:03
 * @FilePath: /front/src/views/user/userAdd.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <!--添加用户界面-->
  <div class="app-container">
    <el-form ref="addUser" :model="addUser" :rules="addRules">
      <el-form-item label="用户名" prop="username" label-width="40%">
        <el-input v-model="addUser.username" autocomplete="off" style="width: 400px" />
      </el-form-item>
      <el-form-item label="邮箱" prop="email" label-width="40%">
        <el-input v-model="addUser.email" autocomplete="off" style="width: 400px" />
      </el-form-item>
      <el-form-item label="昵称" prop="nickname" label-width="40%">
        <el-input v-model="addUser.nickname" style="width: 400px" />
      </el-form-item>
      <el-form-item label="密码" prop="password" label-width="40%">
        <el-input v-model="addUser.password" show-password style="width: 400px" />
      </el-form-item>
    </el-form>
    <div slot="footer" style="margin-left: 70%">
      <el-button type="primary" round @click="postAdd">确 定</el-button>
      <el-button type="info" round @click="cancel">取 消</el-button>
    </div>
  </div>
</template>

<script>
import request from '@/utils/request'
export default {
  name:'AddUser',
  data() {
    const checkEmail = (rule, value, callback) => {
      const mailReg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/
      if (!value) {
        return callback(new Error('邮箱不能为空'))
      }
      setTimeout(() => {
        if (mailReg.test(value)) {
          callback()
        } else {
          callback(new Error('请输入正确的邮箱格式'))
        }
      }, 100)
    }
    return {
      // 添加用户
      addUser: {
        username: '',
        email: '',
        nickname: '',
        password: '',
        avatar: ''
      },
      addRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 5, max: 15, message: '长度在 5 到 15 个字符', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入email', trigger: 'blur' },
          { validator: checkEmail, trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
        ],
        nickname: [
          { required: true, message: '请输入昵称', trigger: 'blur' },
          { min: 1, max: 10, message: '长度在 1 到 10 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    cancel() {
      this.$router.go(-1)
    },
    postAdd() {
      request({
        url: '/users/create_user',
        method: 'post',
        data: {
          username: this.addUser.username,
          email: this.addUser.email,
          is_active: true,
          nickname: this.addUser.nickname,
          password: this.addUser.password
        }
      }
      ).then(response => {
        this.$message({
          message: response.message,
          type: 'success'
        })
        this.$router.push({ path: '/manage/users' })
      })
    }
  }
}
</script>
