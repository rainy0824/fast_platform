<!--
 * @Author: error: git config user.name && git config user.email & please set dead value or install git
 * @Date: 2022-12-18 11:36:51
 * @LastEditors: error: git config user.name && git config user.email & please set dead value or install git
 * @LastEditTime: 2023-01-13 18:49:57
 * @FilePath: /front/src/views/auto/case/case_base_info.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
    <div>
        <el-card>
            <div slot="header" class="clearfix">
                <span style="font-size:18px">用例基本信息</span>
                <el-button style="float: right; padding: 5px 10px ; margin-right: 50px;" type="primary">取消</el-button>
                <el-button style="float: right; padding: 5px 10px ; margin-right: 10px;" type="primary">保存</el-button>
            </div>
            <el-form ref="case_base_form" :label-position="lable_position" :model="case_base_form"
                :rules="case_base_form_rules" size="mini" label-width="100px">
                <el-row :gutter="24">
                    <el-col :span="8">
                        <el-form-item label="用例名称" prop="case_name">
                            <el-input v-model="case_base_form.case_name"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="8">
                        <el-form-item label="所属项目" prop="case_project_id">
                            <!-- <el-select style="width:100%" @change="projectChange"  v-model="case_base_form.case_project_id" clearable filterable
                                placeholder="请选择项目"> -->
                            <el-select style="width:100%" v-model="case_base_form.case_project_id" clearable filterable
                                placeholder="请选择项目">
                                <el-option v-for="item in project_lists" :key="item.project_id"
                                    :label="item.project_name" :value="item.project_id"></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="8">
                        <el-form-item label="所属模块" prop="case_module_id">
                            <el-select style="width:100%" v-model="case_base_form.case_module_id" clearable
                                placeholder="请选择模块">
                                <el-option v-for="item in module_lists" :key="item.module_id" :label="item.module_name"
                                    :value="item.module_id"></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="24">
                    <el-col :span="8">
                        <el-form-item label="用例标签">
                            <el-input v-model="case_base_form.case_tag"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="8">
                        <el-form-item label="用例状态" prop="case_status">
                            <el-select style="width:100%" v-model="case_base_form.case_status" clearable
                                placeholder="请选择状态">
                                <el-option v-for="item in case_status_lists" :key="item.case_status_id"
                                    :label="item.case_status_name" :value="item.case_status_id"></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="8">
                        <el-form-item label="用例级别" prop="case_priority">
                            <el-select style="width:100%" v-model="case_base_form.case_priority" clearable
                                placeholder="请选择级别">
                                <el-option v-for="item in case_priority_lists" :key="item.case_priority_id"
                                    :label="item.case_priority_name" :value="item.case_priority_id">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>

            </el-form>
        </el-card>
        <!-- <aa /> -->
    </div>
</template>

<script>
// 这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）
import { get_module_info_by_project_id } from '@/api/module'
import { get_case_lists_by_filter_data_with_no_pages } from '@/api/testcase'
import aa from '@/views/auto/case/aa.vue'
export default {
    name: 'CaseBaseInfo',
    props: {
        project_lists: {
            type: Array,
            default: function () {
                return []
            }
        }
    },
    components: {
        aa,
    },
    // 定义属性
    data() {
        return {
            lable_position: 'right',
            case_base_form: {
                case_name: '',
                case_project_id: '',
                case_module_id: '',
                case_status: '',
                case_tag: '',
                case_priority: ''

            },
            case_base_form_rules: {
                case_name: [
                    { required: true, message: '用例名称不能为空', trigger: 'blur' }
                ],
                case_project_id: [
                    { required: true, message: '请选择项目', trigger: 'change' }
                ],
                case_module_id: [
                    { required: true, message: '请选择模块', trigger: 'change' }
                ],
                case_status: [
                    { required: true, message: '请选择状态', trigger: 'change' }
                ],
                case_priority: [
                    { required: true, message: '请选择级别', trigger: 'change' }
                ],


            },
            module_lists: [],//通过project_list获取对应的modules
            case_status_lists: [
                {
                    case_status_id: 0,
                    case_status_name: '禁用'
                },
                {
                    case_status_id: 1,
                    case_status_name: '启用'
                }
            ],//0 禁用 1正常
            case_priority_lists: [
                {
                    case_priority_id: 0,
                    case_priority_name: 'P0'
                },
                {
                    case_priority_id: 1,
                    case_priority_name: 'P1'
                },
                {
                    case_priority_id: 2,
                    case_priority_name: 'P2'
                },
                {
                    case_priority_id: 3,
                    case_priority_name: 'P3'
                },
            ]

        }
    },
    // 计算属性，会监听依赖属性值随之变化
    computed: {
    },
    // 监控data/ props 中的数据变化 
    watch: {
        'case_base_form.case_project_id': {
            handler(new_project_id, old_project_id) {
                this.module_lists = [] //每次project_id发生改变就清空module_lists
                this.case_base_form.case_module_id = ''
                const that = this //自定义函数中无法使用this
                if (new_project_id) {
                    //根据_project_id 获取对应的module_list
                    get_module_info_by_project_id(new_project_id).then(resp => {
                        //console.log('this:', this) //undefine
                        //console.log('that:', that)  //vue component
                        let tmp_arr = resp  //return [xxx]
                        tmp_arr.forEach(function (item) {
                            that.module_lists.push({
                                module_id: item.module_id,
                                module_name: item.module_name
                            })
                        })
                    });
                    //根据project_id获取project_case_lists信息
                    get_case_lists_by_filter_data_with_no_pages({ case_project_id: new_project_id }).then(resp => {
                        that.$bus.$emit('send_porject_case_lists', resp.data.case_list)

                    }

                    )
                }
            },
            deep: true
        }
    },
    // 方法集合
    methods: {
        init_data() {

        },
        // projectChange(project_id) { //监听数据变化联动，最好使用wath来监听
        //     console.log('change it ')
        //     if (project_id) {
        //         this.module_lists = [] //每次project_id发生改变就清空module_lists
        //         this.case_base_form.case_module_id = ''
        //         get_module_info_by_project_id(project_id).then(resp => {
        //             let tmp_arr = resp
        //             tmp_arr.forEach((item) => {
        //                 this.module_lists.push({
        //                     module_id: item.module_id,
        //                     module_name: item.module_name
        //                 })
        //             })
        //         })

        //     }
        // }

    },
    // 生命周期 - 创建完成（可以访问当前this实例）
    created() {
        this.init_data()
    },
    // 生命周期 - 挂载完成（可以访问DOM元素）
    mounted() {
    },
    beforeCreate() { }, // 生命周期 - 创建之前
    beforeMount() { }, // 生命周期 - 挂载之前
    beforeUpdate() { }, // 生命周期 - 更新之前
    updated() { }, // 生命周期 - 更新之后
    beforeDestroy() {


    }, // 生命周期 - 销毁之前
    destroyed() { }, // 生命周期 - 销毁完成
    activated() { }, // 如果页面有keep-alive缓存功能，这个函数会触发
}
</script>

<style lang='scss' scoped>

</style>