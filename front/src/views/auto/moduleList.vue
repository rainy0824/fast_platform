<template>
  <div class="app-container">
    <div>
      <el-button id="module_add" type="primary" style="float:left" @click="addBoard">新增</el-button>
    </div>
    <el-table v-loading="listLoading" element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading"
      :data="modules_list" border highlight-current-row>
      <el-table-column type="index" :index="indexMethod" width="50" />
      <el-table-column label="模块名称" prop="module_name" />
      <el-table-column label="所属项目" prop="module_project_name" />
      <el-table-column label="上级模块id" prop="parent_module_id" />
      <el-table-column label="测试负责人" prop="module_manager" />
      <el-table-column label="描述信息" prop="module_desc" />
      <el-table-column label="创建时间" prop="create_time">
        <template slot-scope="scope">
          <span>{{ handle_time(scope.row.create_time) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center">
        <template slot-scope="scope">
          <el-button type="primary" icon="el-icon-edit" circle @click="editBoard(scope.row)" />
          <el-button type="danger" icon="el-icon-delete" circle @click="delModule(scope.row)" />
        </template>
      </el-table-column>
    </el-table>
    <div class="block">
      <el-pagination class="mt-20 text-right" align="right" :hide-on-single-page="hidePage" background
        layout="total,sizes,prev,pager,next,jumper" :current-page.sync="pagination.currentPage"
        :page-size="pagination.pageSize" :total="pagination.total" @current-change="handlePageChange"
        @size-change="handleSizeChange" />
    </div>

     <el-dialog :title="title" :visible.sync="dialogFormVisible">
      <div class="dialog_content">
        <el-form ref="moduleForm" :model="moduleForm" :rules="ruleForm" :disabled="isDisabled" label-width="100px"
          label-position="left">
          <el-form-item label="父模块名称" prop="parent_module_id">
            <treeselect id="parent_module_id" style="width:100%" v-model="moduleForm.parent_module_id" :options="module_tree_list" :normalizer="normalizer" 
              placeholder="请选择上级模块,不选择即为根模块" />
            </el-form-item>
          <el-form-item label="模块名称" prop="module_name">
            <el-input id="module_name" v-model="moduleForm.module_name" autocomplete="off" />
          </el-form-item>
          <el-form-item label="所属项目" prop="module_project_id">
            <el-select id="module_project_id" style="width:100%" v-model="moduleForm.module_project_id" clearable placeholder="请选择项目">
              <el-option v-for="(item, i) in project_lists" :key="i" :label="item.name" :value="item.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="测试负责人" prop="module_manager">
            <el-input id="module_manager" v-model="moduleForm.module_manager" autocomplete="off" />
          </el-form-item>
          <el-form-item label="描述信息" prop="module_desc">
            <el-input id="module_desc" type="textarea" rows="3" v-model="moduleForm.module_desc" autocomplete="off" />
          </el-form-item>
        </el-form>
      </div>
      <div class="dialog_footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleModule" v-show="is_show">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { get_all_project_list} from '@/api/project'
import { get_module_lists, add_module, edit_module, del_module, module_list_to_tree } from '@/api/module'
import { format_time } from '@/utils/index'
import Treeselect from '@riophae/vue-treeselect'
// import the styles
import '@riophae/vue-treeselect/dist/vue-treeselect.css'
export default {
  name: 'ModuleList',
  components: { Treeselect },
  props: {},
  data() {
    return {
      modules_list: [],//显示数组结构的模块数据
      module_tree_list: [],//显示树形结构的模块数据
      project_lists: [], //显示项目list
      moduleForm: {
        parent_module_id: 0,
        module_name: '',
        module_manager: '',
        module_project_id: '',
        module_desc: '',

      },
      ruleForm: {
        module_name: [
          { required: true, message: '请输入模块名称', trigger: 'blur' }
        ],
        module_project_id: [
          { required: true, message: '请选择项目', trigger: 'blur' }
        ],
        module_manager: [
          { required: false, message: '请输入测试负责人', trigger: 'blur' }
        ],
        module_desc: [
          { required: false, message: '请输入描述信息', trigger: 'blur' }
        ]
      },
      pagination: {
        currentPage: 1,
        total: 0,
        pageSize: 10
      },
      title: '',
      dialogFormVisible: false,//是否显示
      isDisabled: false,//是否可编辑
      listLoading: false,
      hidePage: false,
      switchFlag: false,//判断新增还是编辑
      is_show: true,//是否显示确认
      search_condition: {

      },

    }
  },
  watch: {},
  computed: {},
  methods: {
    normalizer(node) {
      return {
        id: node.module_id,
        label: node.module_name
      }
    },
    handle_time(date) {
      return format_time(date)
    },
    init_data() {
      this.listLoading = true
      get_module_lists(this.pagination.currentPage, this.pagination.pageSize, this.search_condition).then((response) => {
        this.pagination.total = response.totals //总数多少
        this.modules_list = response.modules  //具体列表显示
        this.listLoading = false
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
    //切换添加模块
    addBoard() {
      this.dialogFormVisible = true
      this.isDisabled = false
      this.is_show = true
      this.moduleForm = {
      }
      this.title = '添加模块'
      this.switchFlag = true //切换为添加
    },
    //切换编辑模块
    editBoard(row_data) {
      this.dialogFormVisible = true
      this.isDisabled = false
      this.is_show = true
      this.moduleForm = JSON.parse(JSON.stringify(row_data))
      this.title = '修改模块'
      this.switchFlag = false
      if (this.moduleForm.parent_module_id === 0) {
        this.moduleForm.parent_module_id = undefined
      }//默认显示为空

    },
    //删除模块
    delModule(row_data) {
      this.$confirm("确定要删除,是否继续", "提示", {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        del_module(row_data.module_id).then(response => {
          this.init_data()
          this.$message.success(response.message)
        })
      })
    },
    handleModule() {
      if (this.switchFlag) { //发送添加请求
        this.$refs.moduleForm.validate(valid => {
          if (valid) {
          
            add_module(this.moduleForm).then(response => {
              this.init_data()
              this.$message.success(response.message)
              
            })
            this.dialogFormVisible = false
          }
        })
      }
      else {
        this.$refs.moduleForm.validate(valid => { //发送修改请求
          if (valid) {
           
            edit_module(this.moduleForm).then(response => {
              this.init_data()
              this.$message.success(response.message)
            })
            this.dialogFormVisible = false
          }
        })

      }
    },
    //获取树形结构的模块
    get_tree_module_list() {
      module_list_to_tree().then(resp => {
        this.module_tree_list = resp.module_tree_lists
        console.log('tag', this.module_tree_list)
       
      })
    }
    ,
    //获取项目列表
    getprojectList() {
      get_all_project_list().then(response => {
        let result = response.projects
        result.forEach(res => {
          this.project_lists.push({
            name: res.project_name,
            id: res.project_id
          })
        })
       

      }).catch(error => {
        this.$message(error)
      })
    }

  },
  created() {
    this.init_data();
  },
  mounted() {
    
    this.getprojectList();//加载项目列表
    this.get_tree_module_list() //加载树形模块列表
  }
}
</script>
<style scoped="scss">
.dialog_content {
  width: 500px;
  padding: auto;
  margin: auto;

}

.dialog_footer {
  text-align: center;
}

.el-select-dropdown__item {
  padding: 0;
  border-radius: 6px;
}

.el-select-dropdown__item.hover,
.el-select-dropdown__item:hover {
  background: #eaeaea;
}
</style>
