<!--
 * @Author: error: git config user.name && git config user.email & please set dead value or install git
 * @Date: 2022-12-26 10:47:02
 * @LastEditors: error: git config user.name && git config user.email & please set dead value or install git
 * @LastEditTime: 2023-01-09 23:15:17
 * @FilePath: /front/src/views/auto/case/pre_testcase.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
    <div style="text-align:center">
        <!--transfer 绑定props  :props={key:'id' , label:'name' , disabled:'status'} 未指定别名则默认key label disabled-->
        <el-transfer style="text-align: left; display: inline-block" filterable filter-placeholder="请输入case名称"
            :titles="['可选用例', '已选用例']" v-model="selected_value" :format="{
                noChecked: '${total}',
                hasChecked: '${checked}/${total}'
            }"
            :data="project_case_lists" @change="handleChange">
            <span slot-scope="{option}" style="font-size:14px">
                {{ option.label }}
                <el-button type="text" @click.prevent="query_case(option.key)"><i class="el-icon-view"></i></el-button>
            </span>
        </el-transfer>
        <el-drawer  title="用例详情" :visible.sync="show_drawer" :direction="direction"  append-to-body>
            <h4 class="inline-title">基本信息</h4>
                <span v-for="item in  case_info" :key="item.case_id">{{ item }}</span> 
             
        </el-drawer>
    </div>
</template>

<script>
// 这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）

import { get_case_lists_by_filter_data_with_no_pages } from '@/api/testcase';



export default {
    name: 'PreTestCase',
    props: [

    ],
    components: {
    },
    // 定义属性
    data() {
        return {
            project_case_lists: [],//根据项目来获取case
            selected_value: [], //已选的case
            show_drawer:false,
            direction:'rtl', //打开方向 rtl / ltr / ttb / btt
            case_info:[]


        }
    },
    // 计算属性，会监听依赖属性值随之变化
    computed: {
    },
    // 监控data中的数据变化
    watch: {
        selected_value(n, o) {
            console.log(n, o)
        }
    },
    // 方法集合
    methods: {
        handleChange(value, direction, movedKeys) {
            console.log(value, direction, movedKeys);
            console.log('select_value', this.selected_value)

        },
        query_case(item_key) {
            this.show_drawer=true
            get_case_lists_by_filter_data_with_no_pages({case_id:item_key}).then(resp=>{
                this.case_info =resp.data.case_list
            })

        }

    },
    // 生命周期 - 创建完成（可以访问当前this实例）
    created() {

    },
    // 生命周期 - 挂载完成（可以访问DOM元素）
    mounted() {
        this.$bus.$on('send_porject_case_lists', (result) => {
            this.project_case_lists = [] //每次改变都先清空list
            result.forEach(item => {
                //transfer中props没有指定属性则默认为key label disabled
                this.project_case_lists.push({
                    key: item.case_id,
                    label: item.case_name,
                    disabled: item.case_status === 0
                })  

            })
        })
    },
    beforeCreate() { }, // 生命周期 - 创建之前
    beforeMount() { }, // 生命周期 - 挂载之前
    beforeUpdate() { }, // 生命周期 - 更新之前
    updated() { }, // 生命周期 - 更新之后
    beforeDestroy() { 
        this.$bus.$off('send_porject_case_lists')
    }, // 生命周期 - 销毁之前
    destroyed() { }, // 生命周期 - 销毁完成
    activated() { }, // 如果页面有keep-alive缓存功能，这个函数会触发
}
</script>

<style lang='scss' scoped>
.transfer-footer {
    margin-left: 20px;
    padding: 6px 5px;
}

.inline-title {
  position: relative;
  margin-bottom: 12px;
  margin-top: 0px;
  padding-left: 11px;
  font-size: 14px;
  font-weight: 600;
  height: 28px;
  line-height: 28px;
  background: #f7f7fc;
  color: #333333;

}
</style>