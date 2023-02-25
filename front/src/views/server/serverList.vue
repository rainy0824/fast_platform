<template>
  <div class="app-container">
    <div>
      <el-button type="primary" @click="addServer"> 添加服务器</el-button>
      <el-input v-model="searchdata.server_name" prefix-icon="el-icon-search" style="width: 20%; float: right; margin-right: 5%" @change="init_data"/>
    </div>
    <el-table
      v-loading="listLoading"
      element-loading-text="拼命加载中"
      element-loading-spinner="el-icon-loading"
      :data="servers"
      border
      highlight-current-row
    >
      <el-table-column type="index" :index="indexMethod" width="50" />
      <el-table-column label="服务器名称" prop="server_name" />
      <el-table-column label="服务器描述" prop="server_desc" />
      <el-table-column label="服务器ip地址" prop="server_ip" />
       <el-table-column label="服务器端口port" prop="server_port" />
      <el-table-column label="创建时间" prop="create_time" >
        <template slot-scope="scope">
          <span>
            {{handletime(scope.row.create_time)}}
          </span>
        </template>
      </el-table-column>
      <el-table-column label="操作" >
        <template slot-scope="scope">
          <el-button type="primary" icon="el-icon-edit" circle  @click="editServer(scope.row)"/>
          <el-button type="danger" icon="el-icon-delete" circle @click="deleteServer(scope.row)" />
          <el-button type="success" @click="open_Web_ssh(scope.row)" >
            ssh <i class="el-icon-s-platform" />
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <div class="block">
      <el-pagination
        class="mt-20 text-right"
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
      <el-dialog title="服务器信息修改" :visible.sync="dialogFormVisible" >
      <el-form  ref='server_edit' :model="server" :rules="server_rules" style="width: 400px">
      <el-form-item label="服务器名称:" prop="server_name">
        <el-input v-model="server.server_name" autocomplete="off" />
      </el-form-item>
      <el-form-item label="服务器描述:" prop="server_desc">
        <el-input v-model="server.server_desc" autocomplete="off" />
      </el-form-item>
      <el-form-item label="服务器ip:" prop="server_ip">
        <el-input v-model="server.server_ip" autocomplete="off" />
      </el-form-item >
      <el-form-item label="服务器port:" prop="server_port">
        <el-input v-model="server.server_port" autocomplete="off" />
      </el-form-item >
      <el-form-item label="服务器登录名:" prop="server_login_name">
        <el-input v-model="server.server_login_name" />
      </el-form-item>
      <el-form-item label="服务器登录密码:" prop="server_login_pwd">
        <el-input v-model="server.server_login_pwd" show-password />
      </el-form-item>
    </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" round @click="post_edit_server" >确定</el-button>
      <el-button type="info" round @click="dialogFormVisible=false">取 消</el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>
import { getServers_by_filter_data , edit_server,delete_server } from '@/api/server'
import { validateIp } from '@/utils/validate'
import { format_time} from '@/utils/index'
export default {
  name: 'ServerList',
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
      servers: [],
      dialogFormVisible:false,
      listLoading: true,
      hidePage: false,
      searchdata: {
        server_name: null
      },
      pagination: {
        currentPage: 1,
        total: 0,
        pageSize: 10
      },
      server: {}, //
      server_rules: {
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
  methods: {
    //处理时间
    handletime(date){
      return format_time(date)
    },
    init_data() {
      this.listLoading = true
      this.searchdata.server_name === ''
        ? (this.searchdata.server_name = null)
        : this.searchdata
      getServers_by_filter_data(
        this.pagination.currentPage,
        this.pagination.pageSize,
        this.searchdata
      ).then((response) => {
        this.pagination.total = response.totals
        this.servers = response.servers
        this.listLoading = false
      })
    },
    handlePageChange() {
      // table改变, 重新加载数据
      this.init_data()
    },
    handleSizeChange(newPageSize) {
      // 页数大小改变
      const { pagination } = this
      pagination.pageSize = newPageSize
      this.handlePageChange((pagination.currentPage = 1))
    },
    indexMethod(index) {
      // 索引改变
      return (
        index + (this.pagination.currentPage - 1) * this.pagination.pageSize + 1
      )
    },
    //添加服务器信息
    addServer() {
      this.$router.push({
        name: 'AddServer'
      })
    },
    //编辑服务器界面
    editServer(row_data) {
      this.server = JSON.parse(JSON.stringify(row_data))
     
      this.dialogFormVisible = true
    },
    //提交修改数据
    post_edit_server(){
      this.$refs.server_edit.validate(valid=>{
        if(valid){
          this.listLoading=true
          edit_server(this.server).then(response=>{
            this.init_data()
            this.$message.success(response.message)
          })
          this.dialogFormVisible =false
        }
      })
    },
    deleteServer(row_data){
     
      this.$confirm("此操作将永久删除数据,是否继续","提示",{
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
      }).then(()=>{
        delete_server(JSON.parse(JSON.stringify(row_data)).server_id).then(response=>{
        this.init_data();
        this.$message.success(response.message)
      })

      })
    },
    open_Web_ssh(row_data){
      // this.$router.push({name:"web_ssh",params:row_data.server_id})
      
      window.open(`/#/server/web_ssh/${row_data.server_id}`)
    }

  },
  created() {
    this.init_data()
  },
  mounted() {}
}
</script>

