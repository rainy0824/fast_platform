<template>
    <div>
        <el-button @click="changedata"> 按钮</el-button>
        <el-tabs v-model="select_pane">
            <el-tab-pane label="Body" name="first">
                
            </el-tab-pane>
            <el-tab-pane label="Cookie" name="second">
                <el-table :data="response_cookies" stripe border>
                    <el-table-column label="key" prop="name" width="200"></el-table-column>
                    <el-table-column label="value" prop="value" width="400"></el-table-column>
                </el-table>
            </el-tab-pane>
            <el-tab-pane label="Headers" name="third">
                <el-table :data="response_headers" stripe border>
                    <el-table-column label="key" prop="name" width="200"></el-table-column>
                    <el-table-column label="value" prop="value" width="400"></el-table-column>
                </el-table>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>
  
<script>
import response_bodyVue from '@/views/httptest/components/response_body.vue'


export default {
    name: 'bb',
    components: {},
    props: {},
    data() {
        return {
            select_pane:'first',
            response_data:'',
            response_cookies:[
               {
                name:'a',
                value:1
               },
               {
                name:'b',
                value:2
               }
            ],
            response_headers:[
            {
                name:'a1',
                value:1
               },
               {
                name:'b1',
                value:2
               }
            ]

        }
    },
    watch: {



    },
    computed: {},
    methods: {
        changedata(){
            this.response_cookies.push({name:'c',value:3})
        }
    },
    created() {

    },
    mounted() { }
}
</script>
  
<style lang="scss" scoped>

</style>
  