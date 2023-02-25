<template>
  <div class="app-container">
    <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
      <el-form :inline=true >
          <el-form-item label="用户名:">
          <el-input v-model="searchdata.username" placeholder="请输入用户名" prefix-icon="el-icon-search" @change="fetchData"/>
          </el-form-item>
          <el-form-item label="昵称:">
          <el-input v-model="searchdata.username" placeholder="请输昵称" prefix-icon="el-icon-search" @change="fetchData"/>
          </el-form-item>
          <el-form-item>
          <el-button type="primary" @click="addUser">新增用户</el-button>
          </el-form-item>
      </el-form>
    </el-col>
    <el-table
      v-loading="listLoading"
      element-loading-text="拼命加载中"
      element-loading-spinner="el-icon-loading"
      :data="users"
      border
      highlight-current-row
    >
      <el-table-column type="index" :index="indexMethod" width="50"/>
      <el-table-column label="用户名" property="username"/>
      <el-table-column label="Email" property="email"/>
      <el-table-column label="昵称" property="nickname"/>
      <el-table-column label="创建时间" property="create_time">
        <template slot-scope="scope">
            <span>{{handletime(scope.row.create_time)}}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="状态"
        :filters="[{ text: '已激活', value: '已激活' }, { text: '未激活', value: '未激活' }]"
        :filter-method="filterTag"
        filter-placement="bottom-end"
      >
        <template slot-scope="scope">
          <el-tag
            :type="scope.row.is_active === true ? 'primary' : 'danger'"
            disable-transitions
          >{{ scope.row.is_active === true ? '已激活' : '未激活' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center">
        <template slot-scope="scope">
          <el-button type="primary" icon="el-icon-edit" circle @click="editUser(scope.row)"/>
        </template>
      </el-table-column>
    </el-table>
    <div class="block">
      <el-pagination
        class="mt-20 text-right"
        align="right"
        :hide-on-single-page="hidePage"
        background
        layout="total,sizes,prev,pager,next,jumper"
        :current-page.sync="pagination.currentPage"
        :page-size="pagination.pageSize"
        :total="pagination.total"
        @current-change="handlePageChange"
        @size-change="handleSizeChange"
      />
    </div>
    <!---修改用户-->
    <el-dialog title="修改用户" :visible.sync="dialogFormVisible">
      <el-form ref="userForm" :model="user" :rules="editRules">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="user.username" :disabled="true" autocomplete="off"/>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="user.email" autocomplete="off"/>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="user.password" show-password placeholder="不修改密码无需填写"/>
        </el-form-item>
        <el-form-item label="昵称" prop="nickname">
          <el-input v-model="user.nickname"/>
        </el-form-item>
        <el-form-item label="状态" prop="is_active">
          <el-switch
            v-model="user.is_active"
            active-color="#13ce66"
            inactive-color="#ff4949"
          />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="postEditUser">确 定</el-button>
      </div>
    </el-dialog>
  </div>

</template>

<script>
// import { getUsers } from '@/api/user'
import { getUsers_by_filter_data } from '@/api/user'
import {format_time } from '@/utils/index'
export default {
  name:'UserList',
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
      users: null,
      listLoading: true,
      dialogFormVisible: false,
      hidePage: false,
      searchdata: {
        username: null
      },
      user: {
        username: '',
        password: '',
        email: '',
        nickname: '',
        is_active: true
      },
      pagination: {
        currentPage: 1,
        total: 0,
        pageSize: 10
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
    this.fetchData()
  },
  methods: {
    //处理时间
    handletime(date){
      return format_time(date)
    },
    fetchData() {
      this.listLoading = false
      // const { pagination } = this
      // getUsers(pagination.currentPage, pagination.pageSize).then(response => {
      //   this.users = response.users
      //   this.listLoading = false
      //   pagination.total = response.total
      // })
      this.searchdata.username === '' ? this.searchdata.username = null : this.searchdata
      getUsers_by_filter_data(this.pagination.currentPage, this.pagination.pageSize, this.searchdata).then(response => {
        this.users = response.users
        this.listLoading = false
        this.pagination.total = response.totals
      })
    },
    filterTag(value, row) {
      if (value === '已激活') {
        return row.is_active === true
      } else {
        return row.is_active === false
      }
    },
    editUser(row) {
      this.user = JSON.parse(JSON.stringify(row))
      this.dialogFormVisible = true
    },
    postEditUser() {
      this.$store.dispatch('user/editUser', this.user).then(() => {
        this.dialogFormVisible = false
        this.fetchData()
        this.$message({
          message: '用户信息修改成功',
          type: 'success'
        })
      }).catch(() => {
        this.listLoading = false
      })
    },
    handlePageChange() {
      // table改变, 重新加载数据
      this.fetchData()
    },
    handleSizeChange(newPageSize) {
      // 页数大小改变
      const { pagination } = this
      pagination.pageSize = newPageSize
      this.handlePageChange(pagination.currentPage = 1)
    },
    indexMethod(index) {
      // 索引改变
      return index + (this.pagination.currentPage - 1) * this.pagination.pageSize + 1
    },
    addUser() {
      this.$router.push({ path: '/user/add' })
    }
  }
}
</script>
