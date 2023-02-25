<template>
  <div class="app-container">
    <div>
    <el-button type="primary" style="float:left" @click="addBoard">新增环境</el-button>
  </div>
  <el-table v-loading="listLoading" element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading" :data="envs" border highlight-current-row>
    <el-table-column type="index" :index="indexMethod" width="50" />
    <el-table-column label="环境名称" prop="environment_name" />
    <el-table-column label="环境url" prop="environment_url" />
    <el-table-column label="环境描述" prop="environment_desc" />
    <el-table-column label="创建时间" prop="create_time" >
      <template slot-scope="scope">
        <span>{{handle_time(scope.row.create_time)}}</span>
      </template>
    </el-table-column>
    <el-table-column label="操作" align="center">
      <template slot-scope="scope">
        <el-button type="primary" icon="el-icon-edit" circle @click="editBoard(scope.row)" />
        <el-button type="danger" icon="el-icon-delete" circle @click="delEnv(scope.row)" />
      </template>
    </el-table-column>
  </el-table>
    <div class="block">
    <el-pagination class="mt-20 text-right" align="right" :hide-on-single-page="hidePage" background layout="total,sizes,prev,pager,next,jumper" :current-page.sync="pagination.currentPage" :page-size="pagination.pageSize" :total="pagination.total" @current-change="handlePageChange" @size-change="handleSizeChange" />
    </div>

  <el-dialog :title="title"  :visible.sync="dialogFormVisible">
      <el-form ref="envForm"  :model="envForm"  :rules="ruleForm"   :disabled="isDisabled" >
                <el-form-item label="环境名称" prop="environment_name">
          <el-input v-model="envForm.environment_name" autocomplete="off" />
        </el-form-item>
                <el-form-item label="环境URL" prop="environment_url">
          <el-input v-model="envForm.environment_url" autocomplete="off" />
        </el-form-item>
                <el-form-item label="环境描述" prop="environment_desc">
          <el-input v-model="envForm.environment_desc" autocomplete="off" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取 消</el-button>
            <el-button type="primary" @click="handleEnv" v-show="is_show" >确 定</el-button>
      </div>
  </el-dialog>



  </div>
</template>

<script>
import { get_env_lists,add_Env,edit_Env,del_Env} from '@/api/env'
import { format_time} from '@/utils/index'
export default {
  name: 'EnvironmentList',
  components: {},
  props: {},
  data() {
    return {
      envs:[],
      envForm: {
        environment_name: '',
        environment_url: '',
        environment_desc: ''
      },
      pagination: {
        currentPage: 1,
        total: 0,
        pageSize: 10
      },
      ruleForm:{
        environment_name:[
           { required: true, message: '请输入环境名称', trigger: 'blur' }
        ],
        environment_url:[
           { required: true, message: '请输入环境名称', trigger: 'blur' }
        ],
        environment_desc:[
           { required: false, message: '请输入环境名称', trigger: 'blur' }
        ]
      },

      title: '',
      dialogFormVisible: false,//是否显示
      isDisabled: false ,//是否可编辑
      listLoading: false,
      hidePage: false,
      switchFlag: false ,//判断新增还是编辑
      is_show: true //是否显示确认

    }
  },
  watch: {},
  computed: {},
  methods: {

    handle_time(date){
      return format_time(date)
    },
    init_data(){
      this.listLoading=true
      get_env_lists(this.pagination.currentPage,this.pagination.pageSize).then(response =>{
        this.pagination.total=response.totals
        this.envs =response.envs
        this.listLoading=false
      })
    },
    handlePageChange() {
      // table改变, 重新加载数据
      this.init_data()
    },
    handleSizeChange(newPageSize) {
      // 页数大小改变
      const {
        pagination
      } = this
      pagination.pageSize = newPageSize
      this.handlePageChange((pagination.currentPage = 1))
    },
    indexMethod(index) {
      // 索引改变
      return (
        index + (this.pagination.currentPage - 1) * this.pagination.pageSize + 1
      )
    },
    addBoard(){
      this.dialogFormVisible =true
      this.isDisabled =false
      this.is_show =true
      this.envForm={}
      this.title='添加环境'
      this.switchFlag= true //切换为添加
    },
    editBoard(row_data){
      this.dialogFormVisible =true
      this.isDisabled=false
      this.title='修改'
      this.envForm=JSON.parse(JSON.stringify(row_data))
      this.switchFlag=false
    },
    //删除
    delEnv(row_data){
      this.$confirm("确定要删除,是否继续","提示",{
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
      }).then(()=>{
        del_Env(row_data.environment_id).then(response =>{
        this.init_data()
        this.$message.success(response.message)
      })
      })

    }
    ,
    //确认
    handleEnv(){
      if(this.switchFlag){
        this.$refs.envForm.validate(valid =>{
            if(valid){
              add_Env(this.envForm).then(response =>{
                this.init_data() //刷新数据
                this.$message.success(response.message)
               })
               this.dialogFormVisible =false
            }
          })
      }
      else{//修改
        this.$refs.envForm.validate(valid =>{
          if(valid){
            edit_Env(this.envForm.environment_id,this.envForm).then(response =>{
              this.init_data()
              this.$message.success(response.message)
            })
            this.dialogFormVisible=false

          }
        })

      }
    }


  },
  created() {
    this.init_data()
  },
  mounted() {}
}
</script>
