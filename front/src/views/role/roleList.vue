<template>
  <div class="app-container">
    <div>
      <el-button type="primary" @click="addVisible=true,newRole={}">新增角色</el-button>
    </div>
    <el-table
      v-loading="listLoading"
      element-loading-text="拼命加载中"
      element-loading-spinner="el-icon-loading"
      :data="roles"
      border
      highlight-current-row
    >
      <el-table-column type="index" width="50" />
      <el-table-column label="角色名" property="role_name" />
      <el-table-column label="角色描述" property="role_desc" />
      <el-table-column label="成员个数" property="user_counts" />
      <el-table-column label="操作" width="100" align="center">
        <template slot-scope="scope">
          <el-button type="primary" icon="el-icon-edit" circle @click="editRole(scope.row)" />
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
    <el-dialog title="添加角色" :visible.sync="addVisible">
      <el-form ref="roleForm" :model="newRole" :rules="addRule">
        <el-form-item label="角色名" prop="role_name">
          <el-input v-model="newRole.role_name" autocomplete="off" />
        </el-form-item>
        <el-form-item label="描述" prop="role_desc">
          <el-input v-model="newRole.role_desc" autocomplete="off" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="addVisible = false">取 消</el-button>
        <el-button type="primary" @click="addRole">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getRoles, roleAdd } from '@/api/role'
export default {
  name:'RoleList',
  data() {
    return {
      roles: [],
      listLoading: true,
      addVisible: false,
      newRole: {},
      addRule: {
        role_name: [
          { required: true, message: '请输入角色名', trigger: 'blur' },
          { min: 1, max: 10, message: '长度在 1 到 10 个字符', trigger: 'blur' }
        ],
        role_desc: [
          { required: true, message: '请输入描述', trigger: 'blur' },
          { min: 1, max: 30, message: '长度在 1 到 30 个字符', trigger: 'blur' }
        ]
      },
      pagination: {
        currentPage: 1,
        total: 0,
        pageSize: 10
      },
      hidePage: false,
    }
  },
  created() {
    this.loadRole()
  },
  methods: {
    loadRole() {
      getRoles().then(response => {
        this.roles = response.roles
        this.pagination.total = response.totals
        this.listLoading = false
      })
    },
    handlePageChange() {
      // table改变, 重新加载数据
      this.loadRole()
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
    editRole(row) {
      const roleId = row.role_id
      this.$router.push({ path: `/role/edit/${roleId}` })
    },
    addRole() {
      roleAdd(this.newRole).then(response => {
        this.loadRole()
        this.$message({
          message: response.message,
          type: 'success'
        })
        this.addVisible = false
      })
    }
  }
}
</script>

