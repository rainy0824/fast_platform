<!--
 * @Author: error: git config user.name && git config user.email & please set dead value or install git
 * @Date: 2022-12-26 10:48:45
 * @LastEditors: error: git config user.name && git config user.email & please set dead value or install git
 * @LastEditTime: 2023-01-13 21:16:10
 * @FilePath: /front/src/views/auto/case/interface_info.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
    <div>
        <el-form ref="urltref" :model="urlForm" label-position="right" :rules="url_rules">
            <el-row :gutter="10" type="flex">
                <el-col :span="4">
                    <el-form-item label="请求方式:" label-width="100px" prop="method">
                        <slot>
                            <el-select v-model="urlForm.method" placeholder="Select">
                                <el-option v-for="method in methodList" :key="method" :label="method" :value="method">
                                    {{ method }}
                                </el-option>
                            </el-select>
                        </slot>
                    </el-form-item>
                </el-col>
                <el-col :span="16">
                    <el-col :span="8" :offset=4>
                        <el-form-item label="请求路径:">
                            <el-select v-model="select_base_url" clearable>
                                <el-option v-for="item in env_lists" :key="item.env_id" :name="item.env_id"
                                    :label="item.env_url" :value="item.env_url">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="8" >
                        <el-form-item prop="relative_url">
                            <el-input v-model="relative_url" placeholder="请输入请求路径">
                            </el-input>
                        </el-form-item>
                    </el-col>
                </el-col>
                <el-col :span="4">
                    <el-button type="success" @click="debug_interface" icon="el-icon-s-promotion"
                        :disabled="relative_url.length === 0">调试 </el-button>
                </el-col>
            </el-row>
        </el-form>
        <el-card>
            <el-tabs v-model="select_pane">
                <el-tab-pane label="Params" name="first">
                    <Params />
                </el-tab-pane>
                <el-tab-pane label="Headers" name="second">
                    <Headers />
                </el-tab-pane>
                <el-tab-pane label="Body" name="third">
                    <Bodys />
                </el-tab-pane>
            </el-tabs>
        </el-card>
        <div>
            <el-input v-model="response_result" type="textarea" clearable v-show="Object.keys(response_result).length !=0"
                        rows="10">
            </el-input>
                    
        </div>
    </div>
</template>

<script>
// 这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）
import Params from '@/views/httptest/components/params.vue'
import Headers from '@/views/httptest/components/headers.vue'
import Bodys from '@/views/httptest/components/body.vue'
import { send_request } from '@/api/httptest'
export default
    {
        name: 'InterfaceInfo',
        props: {
            env_lists: {
                type: Array,
                default: () => {
                    return []
                }
            }
        },
        components: {
            Params, Headers, Bodys
        },
        // 定义属性
        data() {
            const checkUrl = (rule, value, callback) => {
                if (this.select_base_url === '') {
                    if (!this.relative_url.startsWith('http')) {
                        return callback(new Error('请求地址为http或https开头'))
                    }
                }
            };
            return {
                select_pane: 'first',
                select_base_url: '',//base_url
                relative_url: '', //相对路径
                urlForm: {
                    // absolute_url: this.select_base_url + this.relative_url, //绝对路径  base_url+relative_url
                    method: 'GET',
                    params: ''//Params项后临时组装参数
                },
                body_type: 0,//请求类型 默认为0 none ，1 json 2 form 3 x_form 
                body_data: '', //请求体参数
                body_headers: {},//请求头参数
                methodList: ['GET', 'POST', 'PUT', 'DELETE'],
                url_rules: {
                    relative_url: [
                        { required: true, validator: checkUrl, trigger: 'blur' }
                    ],
                    method:[
                        {required: true ,message:'请选择请求方式',trigger:'change'}
                    ]
                },
                response_result:'',//响应结果
                
            }
        },
        // 计算属性，会监听依赖属性值随之变化
        computed: {
            absolute_url: {
                get() {
                    if (this.select_base_url === '') {
                        return this.relative_url
                    }
                    else {
                        return this.select_base_url + this.relative_url
                    }

                }

            }
        },
        // 监控data中的数据变化
        watch: {
            env_lists: {
                handler(value) {
                    this.receive_data = value
                    this.select_base_url = this.select_base_url
                },
                deep: true
            }

        },
        // 方法集合
        methods: {
            debug_interface() {
                try {
                    send_request(
                        {
                            method: this.urlForm.method, //请求方法
                            url: this.absolute_url, //请求url
                            body_type: this.body_type, //body类型 none  json form x_form
                            body: this.body_data,
                            headers: this.body_headers
                        }
                    ).then(response => {
                    this.response_result='' //重置数据
                    this.response_result = JSON.stringify(response, null, 4);
                    // this.$bus.$emit('format_code',this.response_result)
                    })
                }
                catch (error) {
                    this.$message(error)
                }
            }
        },
        // 生命周期 - 创建完成（可以访问当前this实例）
        created() {

        },
        // 生命周期 - 挂载完成（可以访问DOM元素）
        mounted() {
            //处理params ，拼接到url
            this.$bus.$on('send_param', (result) => {
                console.log('接收result:', result)
                //result =>{'a':'1','b':2}=>?a=1&b=2
                let temp_url = this.relative_url.split('?')[0]
                let obj_to_param = ''
                obj_to_param = Object.keys(result).map(key => key + '=' + result[key]).join('&')
                if (obj_to_param.length !== 0) {
                    this.urlForm.params = '?' + obj_to_param
                    this.relative_url = temp_url + this.urlForm.params
                }
                else {
                    this.relative_url = temp_url
                }


            }),
            //接收headers
            this.$bus.$on('send_header', (result) => {
                    console.log('receive_header', result)
                    this.body_headers = result

                })
            //接收body
            this.$bus.$on('send_body_data', result => {
                console.log('send_body_data', result)
                this.body_data = result.data
                this.body_type = result.type
            })
        },
        beforeCreate() { }, // 生命周期 - 创建之前
        beforeMount() { }, // 生命周期 - 挂载之前
        beforeUpdate() { }, // 生命周期 - 更新之前
        updated() { }, // 生命周期 - 更新之后
        beforeDestroy() { 
            this.$bus.$off('send_param')
            this.$bus.$off('send_header')
            this.$bus.$off('send_body_data')

        }, // 生命周期 - 销毁之前
        destroyed() { }, // 生命周期 - 销毁完成
        activated() { }, // 如果页面有keep-alive缓存功能，这个函数会触发
    }
</script>

<style lang='scss' scoped>

</style>