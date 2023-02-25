<!--
 * @Author: error: git config user.name && git config user.email & please set dead value or install git
 * @Date: 2022-09-23 14:40:55
 * @LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
 * @LastEditTime: 2023-02-08 02:00:35
 * @FilePath: /front/src/views/user/editSelf.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <div class="app-container">
    <el-form ref="editSelf" :model="editSelf" :rules="editRules" title="修改个人信息">
      <el-form-item label="邮箱" prop="email" label-width="40%">
        <el-input v-model="editSelf.email" autocomplete="off" style="width: 400px" />
      </el-form-item>
      <el-form-item label="昵称" prop="nickname" label-width="40%">
        <el-input v-model="editSelf.nickname" style="width: 400px" />
      </el-form-item>
      <el-form-item label="密码" prop="password" label-width="40%">
        <el-input v-model="editSelf.password" show-password placeholder="不修改密码无需填写" style="width: 400px" />
      </el-form-item>
    </el-form>
    <div slot="footer" style="margin-left: 70%">
      <el-button type="primary" round @click="postEditSelf">确 定</el-button>
      <el-button type="info" round @click="cancel">取 消</el-button>
    </div>
  </div>
</template>
<script>
export default {
  name:'EditUser',
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
      editSelf: {
        email: '',
        nickname: '',
        password: '',
        avatar: ''
      },
      editRules: {
        email: [
          { required: true, message: '请输入email', trigger: 'blur' },
          { validator: checkEmail, trigger: 'blur' }
        ],
        password: [
          { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
        ],
        nickname: [
          { required: true, message: '请输入昵称', trigger: 'blur' },
          { min: 1, max: 10, message: '长度在 1 到 10 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    this.$store.dispatch('user/getInfo').then((data) => {
      this.editSelf = data
    })
  },
  methods: {
    cancel() {
      this.$router.go(-1)
    },
    postEditSelf() {
      this.$store.dispatch('user/editSelf', this.editSelf).then((response) => {
        // this.$message({
        //   message: '更新成功',
        //   type: 'success'
        // })
        this.$message.success(response.message)
        this.$router.push('/')
      }).catch(() => {
        this.listLoading = false
      })
    }
  }
}
</script>
