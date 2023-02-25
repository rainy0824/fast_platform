<!--
 * @Author: error: git config user.name && git config user.email & please set dead value or install git
 * @Date: 2022-11-20 17:27:26
 * @LastEditors: error: git config user.name && git config user.email & please set dead value or install git
 * @LastEditTime: 2023-01-09 20:12:45
 * @FilePath: /front/src/views/httptest/components/response_body.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->

<template>
    <div>
        <el-card>
            <div :class="classobj">
                <span style="float: left; padding: 5px 10px ; margin-right: 50px; ">状态: {{ response_content.status_code }}</span>
                <span style="float: right; padding: 5px 10px ; margin-right: 50px;">时间:{{ response_content.cost_time }}</span>
            </div>
            <el-tabs v-model="select_pane">
                <el-tab-pane label="Body" name="first">
                    <el-input v-model="response_content.response_data" type="textarea" clearable v-show="response_content.response_data.length !== 0"
                        rows="10">
                    </el-input>
                    <el-empty description="暂无数据" v-show="is_empty"></el-empty>
                </el-tab-pane>
                <el-tab-pane label="Cookie" name="second">
                    <el-table :data="response_content.response_cookies" stripe border>
                        <el-table-column label="key" prop="name" width="200"></el-table-column>
                        <el-table-column label="value" prop="value" width="400"></el-table-column>
                    </el-table>
                </el-tab-pane>
                <el-tab-pane label="Headers" name="third">
                    <el-table :data="response_content.response_headers" stripe border>
                        <el-table-column label="key" prop="name" width="200"></el-table-column>
                        <el-table-column label="value" prop="value" width="400"></el-table-column>
                    </el-table>
                </el-tab-pane>
            </el-tabs>
        </el-card>

    </div>


</template>

<script>
export default {
    name: 'ResponseBody',
    data() {
        return {
            select_pane: 'first',
            response_content:{
                response_data: '', //响应结果
                response_cookies: [],
                response_headers: [],
                cost_time: '', //响应时间
                status_code: '',//响应状态
            },
            is_empty: true,   

        }
    }
    ,
    methods: {
        

    },
    computed: {
        classobj() {
            return {
                success_style: this.response_content.status_code === 200,
                faild_style: this.response_content.status_code !== 200
            }
        }

    },
    watch:{
        response_headers:{
            handler(){
               

            },
            deep: true
        },
        response_cookies:{
            handler(){

            }
        }

    },
    mounted() {
        this.$bus.$on('show_response', (receive_response_content) => {
            // console.log('显示响应结果:', receive_response_content)
            //将{'a':1,'b':2}=> [{'key':a,'value':1},{'key':b,'value':2}]
            this.response_content.response_data=''
            this.response_content.response_cookies=[]
            this.response_content.response_headers=[]
            let temp_a,temp_b
            this.is_empty = false
            this.response_content.response_data = receive_response_content.data.response
            this.response_content.cost_time = receive_response_content.data.cost
            this.response_content.status_code = receive_response_content.data.status_code 
            temp_a = JSON.parse(receive_response_content.data.cookies)//string =>dict
            Object.keys(temp_a).forEach(key => { this.response_content.response_cookies.push({ 'name': key, 'value': temp_a[key] }) })
            temp_b = JSON.parse(receive_response_content.data.response_headers)
            Object.keys(temp_b).forEach(key => { this.response_content.response_headers.push({ 'name': key, 'value': temp_b[key] }) })

            


        })
    }

}
</script>

<style>
.success_style {
    color: green;
}

.faild_style {
    color: red;
}
</style>