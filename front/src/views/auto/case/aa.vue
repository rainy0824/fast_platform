<!--
 * @Author: error: git config user.name && git config user.email & please set dead value or install git
 * @Date: 2022-12-22 22:51:44
 * @LastEditors: error: git config user.name && git config user.email & please set dead value or install git
 * @LastEditTime: 2023-01-03 17:46:46
 * @FilePath: /front/src/views/auto/case/aa.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
    <div >
        <el-form ref="urltref" :model="urlForm"  label-position="right" >
                <el-row :gutter="10" type="flex">
                    <el-col :span="5">
                        <el-form-item label="请求方式:" label-width="100px" >
                            <slot>
                                <el-select v-model="urlForm.method" placeholder="Select">

                                </el-select>
                            </slot>
                        </el-form-item>
                    </el-col>
                    <el-col :span="16" >
                            <el-col :span="8" :offset=4>
                                <el-form-item label="请求路径:" >
                                    <el-select v-model="urlForm.method" > 
                                    </el-select>
                                </el-form-item>
                            </el-col>
                            <el-col :span="8">
                                <el-input v-model="urlForm.relative_url" placeholder="请输入请求路径" >
                                </el-input>
                            </el-col>
                    </el-col>
                    <el-col :span="4">
                        <el-button type="success" @click="11" icon="el-icon-s-promotion"
                            :disabled="urlForm.absolute_url.length === 0">调试 </el-button>
                    </el-col>
                </el-row>
            </el-form>


    </div>
</template>
  
<script>

export default {
    name: 'aa',
    props: {
        env_lists:{
            type: Array,
            default: ()=>{
                return []
            }
        }
    },
    components: {
    },
    // 定义属性
    data() {
        const generateData = _ => {
            const data = [];
            for (let i = 1; i <= 15; i++) {
                data.push({
                    key: i,
                    label: `备选项 ${i}`,
                    disabled: i % 4 === 0
                });
            }
            return data;
        };
        return {
            select_base_url:'',
            relative_url:'', //相对路径
            urlForm: {
                absolute_url: '', //绝对路径
                method: 'GET',
                params: ''//Params项后临时组装参数
            },
            body_type: 0,//请求类型 默认为0 none ，1 json 2 form 3 x_form 
            body_data: '', //请求体参数
            body_headers: {},//请求头参数
            methodList: ['GET', 'POST', 'PUT', 'DELETE'],
            test_list:[
                {1:'http://127.0.0.1:8000'},
                {2:'http://192.168.1.1:7000'}
            ],
            addrules: {
                // url: [
                //     { requirte: true, validator: checkUrl, trigger: 'blur' }
                // ]
            }

        }
    },
    // 计算属性，会监听依赖属性值随之变化
    computed: {
    },
    // 监控data中的数据变化
    watch: {
        env_lists:{
            handler(value){
                console.log('vvvv',value)
                this.receive_data= value
                this.select_base_url =this.select_base_url
            },
            deep:true
        }

    },
    // 方法集合
    methods: {

    },
    // 生命周期 - 创建完成（可以访问当前this实例）
    created() {

    },
    // 生命周期 - 挂载完成（可以访问DOM元素）
    mounted() {
        
        console.log('huo',this.env_lists)
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