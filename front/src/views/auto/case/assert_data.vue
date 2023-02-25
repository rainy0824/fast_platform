<!--
 * @Author: error: git config user.name && git config user.email & please set dead value or install git
 * @Date: 2023-01-10 17:15:53
 * @LastEditors: error: git config user.name && git config user.email & please set dead value or install git
 * @LastEditTime: 2023-01-13 18:23:41
 * @FilePath: /front/src/views/auto/case/assert_data.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
    <div>
        <el-form label-width="50px" size="mini" label-position="right">
            <div class="inline-title">
                <el-button size="small" type="text" title="校验参数" @click="add_assert_data">
                    <i class="el-icon-circle-plus"> Add</i>
                </el-button>
            </div>

            <div>
                <el-form ref="assert_form" :model="assert_form" :rules="assert_form.assert_rules">
                    <el-table :data="assert_form.assert_data" border>
                        <el-table-column header-align="center" label="校验参数名">
                            <template slot-scope="scope">
                                <el-form-item :prop="'assert_data.' + scope.$index + '.check_key'"
                                    :rules="assert_form.assert_rules.validate_key">
                                    <el-input @change="changeKey(scope.row)" v-model.trim="scope.row.check_key"
                                        placeholder="请输入参数名" clearable autocomplete="off" />
                                </el-form-item>
                            </template>
                        </el-table-column>

                        <el-table-column header-align="center" label="规则">
                            <template slot-scope="scope">
                                <el-form-item :prop="'assert_data.' + scope.$index + '.comparator_rule'"
                                    :rules="assert_form.assert_rules.validate_rule">
                                        <el-select @change="changeRule" v-model.trim="scope.row.comparator_rule"
                                            placeholder="请选择规则" clearable style="width:100%">
                                            <el-option v-for="(comparator_rule, i) in comparatorOptions" :key="i"
                                                :value="comparator_rule" :label="comparator_rule">
                                            </el-option>
                                        </el-select>
                                </el-form-item>
                            </template>
                        </el-table-column>

                        <el-table-column header-align="center" label="校验类型">
                            <template slot-scope="scope">
                                <el-form-item :prop="'assert_data.' + scope.$index + '.value_type'"
                                    :rules="assert_form.assert_rules.validate_type">                                  
                                    <el-select @change="changeType(scope.row)" v-model.trim="scope.row.value_type"
                                        placeholder="请选择类型" clearable style="width:100%">
                                        <el-option v-for="value_type in typeOptions" :key="value_type"
                                            :value="value_type" :label="value_type">
                                        </el-option>
                                    </el-select>
                                </el-form-item>
                            </template>
                        </el-table-column>

                        <el-table-column header-align="center" label="期望值">
                            <template slot-scope="scope">
                                <el-form-item :prop="'assert_data.' + scope.$index + '.expect_value'"
                                    :rules="assert_form.assert_rules.validate_value">
                                    <el-input @change="changeValue(scope.row, scope.$index)"
                                        v-model.trim="scope.row.expect_value" placeholder="输入期望值" clearable
                                        autocomplete="off" />
                                </el-form-item>
                            </template>
                        </el-table-column>

                        <el-table-column header-align="center" label="操作" width="100px">
                            <template slot-scope="scope">
                                <el-form-item>
                                    <el-button type="danger" icon="el-icon-delete" @click="delrow(scope.$index)" />
                                </el-form-item>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-form>
            </div>

        </el-form>
    </div>
</template>

<script>
// 这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）

export default {
    name: 'AssertData',
    props: {
    },
    components: {
    },
    // 定义属性
    data() {
        return {
            assert_form: {
                assert_data: [
                ],
                assert_rules: {
                    validate_key: [
                        { required: true, message: '校验对象名不能为空', trigger: 'blur' }
                    ],
                    validate_rule: [
                        { required: true, message: '规则不能为空', trigger: 'change' },
                      
                    ],
                    validate_type: [
                        { required: true, message: '值类型不能为空', trigger: 'change' ,}
                    ],
                    validate_value: [
                        { required: true, message: '期望值不能为空', trigger: 'blur' }
                    ]
                }
            },
            comparatorOptions: [
                'equals',
                'contains',
                'startswith',
                'endswith',
                'regex_match',
                'type_match',
                'contained_by',
                'less_than',
                'less_than_or_equals',
                'greater_than',
                'greater_than_or_equals',
                'not_equals',
                'string_equals',
                'length_equals',
                'length_greater_than',
                'length_greater_than_or_equals',
                'length_less_than',
                'length_less_than_or_equals',
                'json_equals',
            ],
            typeOptions: ['string', 'int', 'float', 'boolean', 'dict', 'list'],

        }
    },
    // 计算属性，会监听依赖属性值随之变化
    computed: {
    },
    // 监控data中的数据变化
    watch: {},
    // 方法集合
    methods: {
        add_assert_data() {
            this.assert_form.assert_data.push({
                check_key: 'body.',
                comparator_rule: '',
                value_type: '',
                expect_value: ''
            })
            // this.assert_form.assert_data.push(
            //     {
            //         comparator_rule:''
            //     }
            // )
        },
        changeKey() {
            console.log('----', this.assert_form.assert_data)
        },
        changeRule(val) {
            console.log('我被处罚了', val)
            console.log('----', this.assert_form.assert_data)

        },
        changeType(val) {

            console.log('----', this.assert_form.assert_data)
        },
        changeValue() {
            console.log('----', this.assert_form.assert_data)

        },
        delrow(row_index) {
            this.assert_form.assert_data.splice(row_index, 1)
        }
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
    beforeDestroy() { }, // 生命周期 - 销毁之前
    destroyed() { }, // 生命周期 - 销毁完成
    activated() { }, // 如果页面有keep-alive缓存功能，这个函数会触发
}
</script>

<style lang='scss' scoped>

</style>