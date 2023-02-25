<!--
 * @Author: error: git config user.name && git config user.email & please set dead value or install git
 * @Date: 2022-12-26 10:48:00
 * @LastEditors: error: git config user.name && git config user.email & please set dead value or install git
 * @LastEditTime: 2023-01-17 21:44:58
 * @FilePath: /front/src/views/auto/case/setup_hooks.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
    <div>
        <el-form>
            <div class="inline-title" label-width="50px" size="mini" label-position="right">
                <el-button size="small" type="text" title="添加hooks" @click="add_data">
                    <i class="el-icon-circle-plus"> 添加hooks</i>
                </el-button>
            </div>
            <!--dataForm显示所有数据 通过prop属性对应-->
            <el-table
                :data="dataForm.length > 0 ? dataForm.slice((currentPage - 1) * pageSize, currentPage * pageSize) : []"
                border style="width:100%">
                <el-table-column header-align="left" type="index">
                </el-table-column>
                <el-table-column header-align="left" label="hooks名称" prop="data_name">
                </el-table-column>
                <el-table-column header-align="left" label="类型" prop="data_type">
                    <template slot-scope="scope">
                        <el-tag type="warning">
                            {{ scope.row.data_type }}
                        </el-tag>
                    </template>
                </el-table-column>
                <el-table-column header-align="left" label="返回值" prop="data_return_value">
                </el-table-column>
                <el-table-column header-align="left" label="状态" prop="data_status">
                    <template slot-scope="scope">
                        <!-- <el-tag :type="scope.row.data_status === true ? 'primary' : 'danger'" disable-transitions>
                            {{ scope.row.data_status === true ? '启用' : '禁用' }}
                        </el-tag> -->
                        <el-switch v-model="scope.row.data_status" active-color="#13ce66" inactive-color="#ff4949">
                        </el-switch>
                    </template>
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
        <el-drawer append-to-body :title="title" :visible.sync="drawer" direction="rtl" :before-close="handleClose"
            size="50%">
            <div>

                <el-form ref="add_form" :model="add_form" :rules="add_rules" label-position="right" label-width="100px">
                    <el-row>
                        <el-col :span="10">
                            <el-form-item label="Hooks类型:" prop="data_type">
                                <el-select v-model="add_form.data_type" style="width:100%">
                                    <el-option v-for="(item, i ) in hooks_type " :key="i" :value="item"
                                        :label="item"></el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="10">
                            <el-form-item label="Hooks名称:" prop="data_name">
                                <el-input v-model="add_form.data_name"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="10">
                            <el-tooltip placement="bottom-start">
                            </el-tooltip>
                            <el-form-item prop="data_return_value">
                                <template slot="label">
                                    <span>返回值:
                                        <el-tooltip class="return_item" effect="dark" placement="bottom-start">
                                            <div slot="content">
                                                <p>返回值可以为空</p>
                                                <p>返回值不为空则,hooks_code函数 接收值必须与返回值一致</p>
                                                <p>举例：<br />
                                                    def test(): <br />
                                                    &nbsp; return 'test'<br />
                                                    aa = test()<br />
                                                    <br />test()函数必须要有返回值来接收,否则返回None, aa即为返回值<br />
                                                </p>
                                            </div>
                                            <i class="el-icon-question" />
                                        </el-tooltip>
                                    </span>
                                </template>
                                <el-input v-model="add_form.data_return_value"></el-input>
                            </el-form-item>

                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="24">
                            <el-form-item prop="data_hooks_code">
                                <template slot="label">
                                    <span>脚本数据:
                                        <el-tooltip class="code_item" effect="dark" placement="bottom-start">
                                            <div slot="content">
                                                <p>点击可调试脚本</p>
                                            </div>
                                            <el-button type="danger" size="mini" icon="el-icon-video-play"
                                                @click="debug_script"></el-button>
                                        </el-tooltip>
                                    </span>
                                </template>
                                <PythonEditor />
                            </el-form-item>
                        </el-col>
                    </el-row>

                    <el-row>
                        <el-col :span="20">
                            <el-form-item label="状态:" prop="data_status">
                                <el-switch v-model="add_form.data_status" active-color="#13ce66"
                                    inactive-color="#ff4949" />
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-form-item>
                        <el-button type="primary" @click="save_btn">保存</el-button>
                        <el-button type="primary" @click="cancle_btn">取消</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </el-drawer>

    </div>
</template>

<script>
// 这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）
import PythonEditor from '@/components/pythoneditor/python_editor.vue'
import { exec_python_script } from '@/api/test_case_setup_hooks'
export default {
    name: 'SetUpHooks',
    props: {
    },
    components: {
        PythonEditor
    },
    // 定义属性
    data() {
        return {
            dataForm: [
            ],
            hooks_type: ['Python方法'],
            kv_data: {},//组装数据{1:[{},{}],2:[],3:[]}
            add_form: { //item_data
                data_id: '',
                data_name: '',
                data_type: '',
                data_status: true,
                data_return_value: '',
                data_hooks_code: ''
            },
            add_rules: {//添加测试数据规则验证
                data_name: [
                    { required: true, message: '名称不能为空', trigger: 'blur' }
                ],
                data_type: [
                    { required: true, message: '名称不能为空', trigger: 'change' }
                ],
                data_status: [
                    { required: true, message: '请选择状态', trigger: 'blur' }
                ],
                data_hooks_code: [
                    { required: true, message: '值不能为空', trigger: 'blur' }
                ]

            },
            title: '',
            drawer: false,
            current_index: '', //当前编辑的index
            currentPage: 1, //当前页
            pageSize: 5    //分页数
        }
    },
    // 计算属性，会监听依赖属性值随之变化
    computed: {
    },
    // 监控data中的数据变化
    watch: {
        'add_form.data_hooks_code': {
            handler() {
                this.$bus.$on('send_python_code', code => {
                    this.add_form.data_hooks_code = code
                })
               
            },
            deep: true
        },
        'add_form.data_return_value': {
            handler(value) {
                this.add_form.data_return_value = value
            }
        },
        'add_form.data_status': {

            handler(value) {
                this.add_form.data_status = value
            }
        }

    },
    // 方法集合
    methods: {
        debug_script() {
            exec_python_script({
                hooks_code: this.add_form.data_hooks_code,
                return_value: this.add_form.data_return_value
            }).then(resp => {
                if (resp.code == 200) {
                    this.$notify({
                        title: '执行成功',
                        message: resp.data,
                        type: 'success',
                        offset: 50,
                        duration: 3000
                    })
                } else {
                    this.$notify({
                        title: '执行失败',
                        message: '请检查参数',
                        type: 'error',
                        offset: 50,
                        duration: 3000
                    })
                }
            })
        },
        handleClose(done) {
            // debugger;
            this.$confirm('确认关闭？')
                .then(_ => {
                    done();
                })
                .catch(_ => { });
        },

        handleCurrentChange(val) {
            this.currentPage = val
        },
        add_data() { //添加界面
            this.drawer = true
            this.add_form = {
                data_name: '',
                data_type: '',
                data_status: true,
                data_return_value: '',
                data_hooks_code: ''
            }
            this.$bus.$emit('resetting_code', '')
            this.title = '新增SetUpHooks'
            this.switch_flag = true //新增
        },
        edit_data(idx, row_data) { //编辑界面
            this.drawer = true
            this.title = '修改SetUpHooks'
            this.switch_flag = false
            this.add_form = JSON.parse(JSON.stringify(row_data))
            this.$bus.$emit('resetting_code',this.add_form.data_hooks_code)
            this.current_index = idx  //保存行index

        },
        save_btn() { //保存按钮 判断保存的是哪个环境的数据 evn_id

            if (this.switch_flag) {
                console.log('新增时的保存')
                this.$refs.add_form.validate((vaild) => {
                    if (vaild) {
                        this.dataForm.push({
                            data_name: this.add_form.data_name,
                            data_type: this.add_form.data_type,
                            data_status: this.add_form.data_status,
                            data_return_value: this.add_form.data_return_value,
                            data_hooks_code: this.add_form.data_hooks_code,

                        })
                        this.drawer = false
                    }
                })

            }
            else {
                //修改的时候需要将index进行修改
                this.$refs.add_form.validate((vaild) => {
                    if (vaild) {
                        this.dataForm[this.current_index].data_name = this.add_form.data_name
                        this.dataForm[this.current_index].data_type = this.add_form.data_type
                        this.dataForm[this.current_index].data_status = this.add_form.data_status
                        this.dataForm[this.current_index].data_return_value = this.add_form.data_return_value
                        this.dataForm[this.current_index].data_hooks_code = this.add_form.data_hooks_code
                    }
                   
                 
                    this.drawer = false
                })

            }
        },
        cancle_btn() {//取消按钮
            this.drawer = false
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
    beforeCreate() { }, // 生命周期 - 创建之前
    beforeMount() { }, // 生命周期 - 挂载之前
    beforeUpdate() { }, // 生命周期 - 更新之前
    updated() { }, // 生命周期 - 更新之后
    beforeDestroy() { 
        this.$bus.$off('send_python_code')
    }, // 生命周期 - 销毁之前
    destroyed() { }, // 生命周期 - 销毁完成
    activated() { }, // 如果页面有keep-alive缓存功能，这个函数会触发
}
</script>

<style lang='scss' scoped>

</style>