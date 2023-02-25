<template>
  <div>
    <div>
      <el-button type="primary" style="float:left" @click="addCase">新增</el-button>
    </div>
    <el-table v-loading="listLoading" element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading"
      :data="case_list" border highlight-current-row>
      <el-table-column type="index" :index="indexMethod" width="50" />
      <el-table-column label="用例名称" prop="case_name" />
      <el-table-column label="所属项目" prop="case_project_name" />
      <el-table-column label="所属模块" prop="case_module_name" />
      <el-table-column label="用例状态" prop="case_status" />
      <el-table-column label="优先级" prop="case_priority" />
      <el-table-column label="创建时间" prop="create_time">
        <template slot-scope="scope">
          <span>{{ handle_time(scope.row.create_time) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" >
        <template slot-scope="scope">
          <el-button type="primary" icon="el-icon-edit" circle @click="editHandle(scope.row)" />
          <el-button type="primary" icon="el-icon-video-play" circle @click="runhandle(scope.row)" />
        </template>
      </el-table-column>
    </el-table>
    <div class="block">
      <el-pagination class="mt-20 text-right" align="right" :hide-on-single-page="hidePage" background
        layout="total,sizes,prev,pager,next,jumper" :current-page.sync="pagination.currentPage"
        :page-size="pagination.pageSize" :total="pagination.total" @current-change="handlePageChange"
        @size-change="handleSizeChange" />
    </div>
    <el-dialog v-if="dialogVisible" :title="title" :visible.sync="dialogVisible" width="1400px"  >
                <!--父传project_list属性 子：props接收-->
                <CaseBaseInfo  :project_lists="project_lists" /> 
                <CaseRequestInfo />
    </el-dialog>
  </div>

</template>

<script>
// 这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）
import { format_time } from '@/utils/index'
import { get_case_lists_by_filter_data }  from '@/api/testcase'
import { get_all_project_list } from '@/api/project'
// import { get_module_info } from '@/api/module' //前端自行组装调用需要此方法

import CaseBaseInfo from '@/views/auto/case/case_base_info.vue'
import CaseRequestInfo from '@/views/auto/case/case_request_info.vue'

export default {
name: 'TestCaseList', 
props: [
],
  components: {
    CaseBaseInfo,CaseRequestInfo
  },
  // 定义属性
  data() {
    return {
        case_list:[],
        // receive_list:[], //前端调用需要此参数，后端已做处理
        pagination: {
        currentPage: 1,
        total: 0,
        pageSize: 10
      },
      listLoading:false,
      hidePage: false,
      search_condition:{
      },//查询条件
      title: '',
      dialogVisible:false,
      isDisabled: false,
      project_lists:[]

      
    }
  },
  // 计算属性，会监听依赖属性值随之变化
  computed: {
  },
  // 监控data中的数据变化
  watch: {},
  // 方法集合
  methods: {
    init_data(){
        this.listLoading = true
    //   get_case_list(this.pagination.currentPage, this.pagination.pageSize,this.search_condition).then(response => {
    //     this.pagination.total = response.data.totals //总数多少
    //     this.receive_list = response.data.case_list //具体列表显示
    //     //todo 差一个接口，通过parent_id 拿到parent_name 
    //     this.receive_list.forEach((item)=>{
    //         //获取module_name
    //        get_module_info(item.case_module_id).then((response)=>{
    //            item.case_module_name=response.module_name
    //            this.case_list.push(item)
    //          })
    //        })    
    //     this.listLoading = false
    //   })
    get_case_lists_by_filter_data(this.pagination.currentPage, this.pagination.pageSize,this.search_condition).then(response => {
        this.pagination.total = response.data.totals //总数多少
        this.case_list = response.data.case_list //具体列表显示   
        this.listLoading = false
      })

    },
    addCase(){
        this.dialogVisible=true
        this.title='新增用例'

    },
    runhandle(){

    },
    handle_time(date) {
      return format_time(date)
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
    get_project_list(){
        get_all_project_list().then(response=>{
            let projects =response.projects
            projects.forEach(res => {
          this.project_lists.push({
            project_name: res.project_name,
            project_id: res.project_id
          })
        })
            
        })
    }
    
  },
  // 生命周期 - 创建完成（可以访问当前this实例）
  created() {
    
    this.init_data()
  },
  // 生命周期 - 挂载完成（可以访问DOM元素）
  mounted() {
    this.get_project_list()

  },
  beforeCreate() {}, // 生命周期 - 创建之前
  beforeMount() {}, // 生命周期 - 挂载之前
  beforeUpdate() {}, // 生命周期 - 更新之前
  updated() {}, // 生命周期 - 更新之后
  beforeDestroy() {}, // 生命周期 - 销毁之前
  destroyed() {}, // 生命周期 - 销毁完成
  activated() {}, // 如果页面有keep-alive缓存功能，这个函数会触发
}
</script>

<style lang='scss' scoped>

  
</style>