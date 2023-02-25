<!--
 * @Author: error: git config user.name && git config user.email & please set dead value or install git
 * @Date: 2022-09-23 14:40:55
 * @LastEditors: error: git config user.name && git config user.email & please set dead value or install git
 * @LastEditTime: 2023-01-10 21:18:54
 * @FilePath: /front/src/views/httptest/components/headers.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->

<template>
    <el-form label-width="50px" size="mini" label-position="right">
        <div class="inline-title" >
            <el-button size="small" type="text" title="添加参数" @click="addHeaders">
                <i class="el-icon-circle-plus"> Add</i>
            </el-button>
        </div>

        <div>
            <!--el-from 嵌套el-table-->
            <el-form ref="headerform" :model="headerform" :rules="headerform.header_rules">
                <el-table :data="headerform.header_data" border>
                    <el-table-column header-align="center" label="KEY">
                        <template slot-scope="scope">
                            <!--不只是el-form才配置，每一个el-form-item都要配置rules属性 并且保证动态prop属性唯一性 -->
                            <el-form-item :prop="'header_data.' + scope.$index + '.input_key'"
                                :rules="headerform.header_rules.validate_key">
                                <!-- scope.row当前行数据  scope.row.input_key 给输入框绑定input_key -->
                                <el-input @change="changeKey(scope.row)" v-model.trim="scope.row.input_key"
                                    placeholder="请输入key" clearable autocomplete="off" />
                            </el-form-item>
                        </template>
                    </el-table-column>
                    <!-- prop 属性用来校验双向绑定校验规则-->
                    <el-table-column header-align="center" label="VALUE">
                        <template slot-scope="scope">
                            <el-form-item :prop="'header_data.' + scope.$index + '.input_value'"
                                :rules="headerform.header_rules.validate_value">
                                <el-input @change="changeValue(scope.row, scope.$index)"
                                    v-model.trim="scope.row.input_value" placeholder="请输入value" clearable
                                    autocomplete="off" />
                            </el-form-item>
                        </template>
                    </el-table-column>
                    <el-table-column header-align="center" label="DESCRIPTION">
                        <template slot-scope="scope">
                            <el-form-item>
                                <el-input @change="111" v-model.trim="scope.row.input_description"
                                    placeholder="请输入description" autosize clearable />
                            </el-form-item>
                        </template>
                    </el-table-column>
                    <el-table-column header-align="center" label="操作" width="100px">
                        <template slot-scope="scope">
                            <!-- scope.$index数组索引-->
                            <el-form-item>
                                <el-button type="danger" icon="el-icon-delete" @click="delrow(scope.$index)" />
                            </el-form-item>
                        </template>
                    </el-table-column>
                </el-table>
            </el-form>
        </div>
        
    </el-form>

</template>

<script>
// 这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）

export default {
    name: 'Headers',

    components: {
    },
    // 定义属性
    data() {
        return {

            headerform: {
                header_data: [],//存放数据
                header_rules: { //校验规则
                    validate_key: [
                        { required: true, message: '参数不能为空', trigger: 'blur' }
                    ],
                    validate_value: [
                        { required: true, message: '值不能为空', trigger: 'blur' }
                    ]
                }

            },
            send_header: {} //组装后的请求头
        }
    },
    // 计算属性，会监听依赖属性值随之变化
    computed: {
        
    },
    // 监控data中的数据变化
    watch: {
        // 'headerform.header_data': {
        //     handler: function () {
        //         console.log('--',this.headerform.header_data)
        //         if(this.headerform.header_data !== ''){
        //             this.headerform.header_data.map(item => {
        //             this.header_kv[item.input_key] = item.input_value
        //         })
        //         }
               
        //     },
        //     deep: true

        // }

    },
    // 方法集合
    methods: {
        //组装  [{input_key:'a','input_value':1},{input_key:'b','input_value':2}]  =>{a:1,b:2}
        hanle_key_value() {
            let header_kv={}
            if (this.headerform.header_data.length !=0) {
                this.headerform.header_data.map(item => {
                    header_kv[item.input_key] = item.input_value
                })
            }
            return header_kv
        },
        addHeaders() {
            this.headerform.header_data.push({
                input_key:'',
                input_value:''
            })
        },
        changeKey(row_data) {
          
            this.send_header=this.hanle_key_value()
          
            this.$bus.$emit('send_header', this.send_header) 
        },
        changeValue(row_data) {
           
            this.send_header=this.hanle_key_value()
           
            this.$bus.$emit('send_header', this.send_header)
        },
        delrow(row_index) {
            this.headerform.header_data.splice(row_index, 1)
           
            this.send_header=this.hanle_key_value() 
            
            this.$bus.$emit('send_header', this.send_header)
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


    }, // 生命周期 - 销毁之前
    destroyed() { }, // 生命周期 - 销毁完成
    activated() { }, // 如果页面有keep-alive缓存功能，这个函数会触发
}
</script>

<style lang='scss' scoped>
.inline-title {
    position: relative;
    margin-top: 0px;
    margin-bottom: 0px;
    padding-left: 11px;
    font-size: 14px;
    font-weight: 600;
    line-height: 30px;
    background: #f7f7fc;
    color: #333333;

}
</style>