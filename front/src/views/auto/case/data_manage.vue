<!--
 * @Author: error: git config user.name && git config user.email & please set dead value or install git
 * @Date: 2022-12-21 17:37:20
 * @LastEditors: error: git config user.name && git config user.email & please set dead value or install git
 * @LastEditTime: 2023-01-09 20:16:38
 * @FilePath: /front/src/views/auto/case/data_manage.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
    <div>
        <el-tabs ref="left_tabs" :tab-position="tabPosition" v-model="default_select_pane_id">
            <el-tab-pane v-for="item in env_lists" :key="item.env_id" :name="item.env_id" :label="item.env_name">
                <el-form>
                    <div class="inline-title" label-width="50px" size="mini" label-position="right">
                        <el-button size="small" type="text" title="添加参数" @click="add_data">
                            <i class="el-icon-circle-plus"> Add</i>
                        </el-button>
                    </div>
                    <!--dataForm显示所有数据 通过prop属性对应-->
                    <el-table
                        :data="dataForm.length > 0 ? dataForm.slice((currentPage - 1) * pageSize, currentPage * pageSize) : []"
                        border style="width:100%">
                        <el-table-column header-align="left" type="index">
                        </el-table-column>
                        <el-table-column header-align="left" label="#id" prop="data_id">
                        </el-table-column>
                        <el-table-column header-align="left" label="变量名称" prop="data_name">
                        </el-table-column>
                        <el-table-column header-align="left" label="变量数据" prop="data_json">
                        </el-table-column>
                        <el-table-column header-align="left" label="操作">
                            <template slot-scope="scope">
                                <el-button type="text" @click="edit_data(scope.$index, scope.row)">编辑</el-button>
                                <el-button type="text" @click="del_data(scope.$index)">删除</el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                    <el-pagination v-show="dataForm.length > 0" align="right" background layout="total,prev,pager,next"
                        :current-page.sync="currentPage" :page-size="pageSize" :total="dataForm.length"
                        @current-change="handleCurrentChange" />
                </el-form>
            </el-tab-pane>

        </el-tabs>
        <el-dialog append-to-body :title="title" :visible.sync="dialogVisible" width="700px">
            <el-form ref="add_form" :model="add_form" :rules="add_rules" label-position="right" label-width="100px">
                <el-row>
                    <el-col :span="20">
                        <el-form-item label="测试场景:" prop="data_name">
                            <el-input v-model="add_form.data_name"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="20">
                        <el-form-item label="测试数据:" prop="data_json">
                            <el-input type="textarea" v-model="add_form.data_json" placeholder="json格式"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-form-item>
                    <el-button type="primary" @click="save_btn">保存</el-button>
                    <el-button type="primary" @click="cancle_btn">取消</el-button>
                </el-form-item>
            </el-form>
        </el-dialog>
    </div>
</template>

<script>
// 这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）
import { } from '@/api/testcase'
export default {
    name: 'DataManage',
    props: {
        env_lists: {
            type: Array,
            default: function () {
                return []
            }
        }

    }
    ,
    components: {
    },
    // 定义属性
    data() {
        return {
            tabPosition: 'left',//选项卡句左边
            default_select_pane_id: '',//默认选择
            dataForm: [
            ],
            kv_data: {},//组装数据{1:[{},{}],2:[],3:[]}
            add_form: { //item_data
                data_id: '',
                data_name: '',
                data_json: ''
            },
            add_rules: {//添加测试数据规则验证
                data_name: [
                    { required: true, message: '名称不能为空', trigger: 'blur' }
                ],
                data_json: [
                    { required: true, message: '值不能为空', trigger: 'blur' }
                ]

            },
            dialogVisible: false,
            title: '',
            switch_flag: false,
            current_index: '', //当前编辑的index
            currentPage: 1, //当前页
            pageSize: 5    //分页数


        }
    },
    // 计算属性，会监听依赖属性值随之变化
    computed: {
    },
    // 监控data props中的数据变化
    watch: {
        env_lists: {
            handler(newval) {
                this.receive_data = newval //获取env_list
               
                this.default_select_pane_id = this.receive_data[0].env_id //设置默认tab项
                const that = this
                this.receive_data.map(item => {
                    that.kv_data[item.env_id] = [] //初始化数据
                })
               
            },
            deep: true
        }
        ,
        default_select_pane_id: {
            handler(newid) {
                this.dataForm = this.kv_data[newid]
            },
            deep: true

        },
    },
    // 方法集合
    methods: {

        handleCurrentChange(val) {
            this.currentPage = val
        },
        add_data() { //添加界面
            this.dialogVisible = true
            this.add_form = {}
            this.title = '新增测试数据'
            this.switch_flag = true //新增
        },
        edit_data(idx, row_data) { //编辑界面
            
            this.dialogVisible = true
            this.title = '修改测试数据'
            this.switch_flag = false
            this.add_form = JSON.parse(JSON.stringify(row_data))
            this.current_index = idx  //保存行index

        },
        save_btn() { //保存按钮 判断保存的是哪个环境的数据 evn_id

            if (this.switch_flag) {
                console.log('新增时的保存')
                this.$refs.add_form.validate((vaild) => {
                    if (vaild) {
                       
                        //{1:[],2:[],3:[]} 根据key值判断是往哪个key里面添加数据
                        this.kv_data[this.default_select_pane_id].push({
                            data_name: this.add_form.data_name,
                            data_json: this.add_form.data_json
                        })
                     
                        this.dialogVisible = false
                    }
                })

            }
            else {
                //修改的时候需要将index进行修改
                this.$refs.add_form.validate((vaild) => {
                    if (vaild) {
                       
                        this.kv_data[this.default_select_pane_id][this.current_index].data_name = this.add_form.data_name,
                            this.kv_data[this.default_select_pane_id][this.current_index].data_json = this.add_form.data_json
                        this.dialogVisible = false
                    }

                })

            }
        },
        cancle_btn() {//取消按钮
            this.dialogVisible = false
        },
        del_data(idx) {//删除
            this.dataForm.splice(idx, 1)
        },

    },
    // 生命周期 - 创建完成（可以访问当前this实例）
    created() {
    },
    // 生命周期 - 挂载完成（可以访问DOM元素）
    mounted() {
    },
    beforeCreate() {

    }, // 生命周期 - 创建之前
    beforeMount() {


    }, // 生命周期 - 挂载之前
    beforeUpdate() {


    }, // 生命周期 - 更新之前
    updated() {


    }, // 生命周期 - 更新之后
    beforeDestroy() {


    }, // 生命周期 - 销毁之前
    destroyed() {
        console.log('我被销毁了')
    }, // 生命周期 - 销毁完成
    activated() {


    }, // 如果页面有keep-alive缓存功能，这个函数会触发
}
</script>

<style lang='scss' scoped>

</style>