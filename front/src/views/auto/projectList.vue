<template>
  <div class="app-container">
    <div>
      <el-button id="project_add" type="primary" style="float:left" @click="addBoard">新增项目</el-button>
    </div>
    <el-table v-loading="listLoading" element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading"
      :data="projects" border highlight-current-row>
      <el-table-column type="index" :index="indexMethod" width="50" />
      <el-table-column label="项目名称" prop="project_name" />
      <el-table-column label="项目描述" prop="project_desc" />
      <el-table-column label="负责人" prop="project_manager" />
      <el-table-column label="项目状态">
        <template slot-scope="scope">
          <el-tag :type="scope.row.project_status === true ? 'primary' : 'danger'" disable-transitions>
            {{ scope.row.project_status === true ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="创建时间" prop="create_time">
        <template slot-scope="scope">
          <span>{{ handle_time(scope.row.create_time) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center">
        <template slot-scope="scope">
          <el-button type="primary" icon="el-icon-view" circle @click="getBoard(scope.row)" />
          <el-button type="primary" icon="el-icon-edit" circle @click="editBoard(scope.row)" />
          <el-button type="danger" icon="el-icon-delete" circle @click="11" />
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
      <el-form ref="projectForm" :model="projectForm" :rules="ruleForm" :disabled="isDisabled">
        <el-form-item label="项目名称" prop="project_name">
          <el-input id="project_name" v-model="projectForm.project_name" autocomplete="off" />
        </el-form-item>
        <el-form-item   label="项目描述" prop="project_desc">
          <el-input id="project_desc" v-model="projectForm.project_desc" autocomplete="off" />
        </el-form-item>
        <el-form-item label="项目负责人" prop="project_manager">
          <el-input   id="project_manager" v-model="projectForm.project_manager" autocomplete="off" />
        </el-form-item>
        <el-form-item    label="开发人员" prop="developer">
          <el-input id="project_developer" v-model="projectForm.developer" autocomplete="off" />
        </el-form-item>
        <el-form-item   label="测试人员" prop="tester">
          <el-input  id="project_tester"  v-model="projectForm.tester" autocomplete="off" />
        </el-form-item>
        <el-form-item label="状态" prop="project_status">
          <el-switch v-model="projectForm.project_status" active-color="#13ce66" inactive-color="#ff4949" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleProject" v-show="is_show">确 定</el-button>

      </div>
    </el-dialog>


  </div>
</template>

<script>
import {
  getProjects_by_filter_data, getProjectInfo, addProject, updateProject
} from '@/api/project'

import { format_time } from '@/utils/index'
export default {
  name: 'ProjectList',
  components: {},
  props: {},
  data() {
    return {
      projects: [],
      title: '添加/修改项目',
      pagination: {
        currentPage: 1,
        total: 0,
        pageSize: 10
      },
      //新增项目对应表单字段
      projectForm: {
        project_name: '',
        project_desc: '',
        project_manager: '',
        tester: '',
        developer: '',
        project_status: true
      },
      ruleForm: {
        project_name: [
          { required: true, message: '请输入项目名称', trigger: 'blur' }
        ],
        project_desc: [
          { required: false, message: '请输入项目描述', trigger: 'blur' }
        ],
        project_manager: [
          { required: false, message: '请输入管理人员', trigger: 'blur' }
        ],
        tester: [
          { required: false, message: '测试人员', trigger: 'blur' }
        ],
        developer: [
          { required: false, message: '开发人员', trigger: 'blur' }
        ],
      },
      search_condition: {

      },
      dialogFormVisible: false,//是否显示
      isDisabled: false,//是否可编辑
      listLoading: false,
      hidePage: false,
      switchFlag: false,//判断新增还是编辑
      is_show: true //是否显示确认
    };
  },
  watch: {},
  computed: {},
  methods: {
    handle_time(date) {
      return format_time(date)
    },
    init_data() {
      this.listLoading = true
      getProjects_by_filter_data(
        this.pagination.currentPage,
        this.pagination.pageSize,
        this.search_condition
      ).then((response) => {
        this.pagination.total = response.totals
        this.projects = response.projects
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
    //查看项目
    getBoard(row_data) {
      this.dialogFormVisible = true,
        this.title = '查看项目'
      this.projectForm = JSON.parse(JSON.stringify(row_data))
      this.isDisabled = true
      this.is_show = false
    },
    //添加项目信息界面
    addBoard() {
      this.dialogFormVisible = true
      this.isDisabled = false
      this.is_show = true
      this.projectForm = {
        project_name: '',
        project_desc: '',
        project_manager: '',
        tester: '',
        developer: '',
        project_status: true
      }
      this.title = '添加项目'
      this.switchFlag = true //切换为添加
    },
    // //编辑项目列表弹出项目列表框
    editBoard(row_data) {
      this.dialogFormVisible = true
      this.isDisabled = false
      this.is_show = true
      this.title = '修改项目'
      this.projectForm = JSON.parse(JSON.stringify(row_data))
     
      this.switchFlag = false //切换为修改
    },
    //确认
    handleProject() {
      if (this.switchFlag) {
        //添加项目
        this.$refs.projectForm.validate(valid => {
          if (valid) {
            addProject(this.projectForm).then(response => {
              this.init_data() //刷新数据
              this.$message.success(response.message)
            })
            this.dialogFormVisible = false
          }
        })
      } else {
        //修改项目
        this.$refs.projectForm.validate(valid => {
          if (valid) {
            updateProject(this.projectForm.project_id, this.projectForm).then(response => {
              this.init_data() //刷新数据
              this.$message.success(response.message)
            }

            )
          }
          this.dialogFormVisible = false
        })

      }

    }

  },
  created() {
    this.init_data()
  },
  mounted() { },
};
</script>

<style lang="scss" scoped>

</style>
