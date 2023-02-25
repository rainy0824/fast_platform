<!--
 * @Author: error: git config user.name && git config user.email & please set dead value or install git
 * @Date: 2022-09-23 14:40:55
 * @LastEditors: error: git config user.name && git config user.email & please set dead value or install git
 * @LastEditTime: 2023-01-09 20:12:41
 * @FilePath: /front/src/views/httptest/components/request_url.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <div>
    <el-form :inline="true" ref="urltref" :model="urlForm" :rules="addrules" label-width="50px"
      label-position="right" class="urlclass">
      <el-row :gutter="10">
        <el-col :lg="14" :xl="14" class="mb20">
          <el-form-item prop="url">
            <el-input v-model="urlForm.url" placeholder="请输入请求路径" class="input-with-select" style="min-width:900px;">
              <template #prepend>
                <el-select v-model="urlForm.method" placeholder="Select" style="width: 100px">
                  <el-option v-for="method in methodList" :key="method" :label="method" :value="method">
                    <span style="float: left; font-weight: 200">{{ method }}</span>
                  </el-option>
                </el-select>
              </template>
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :lg="10" :push="1">
          <el-button type="success" @click="debugrequest()" icon="el-icon-s-promotion" :disabled="urlForm.url.length===0 ">调试 </el-button>
        </el-col>
      </el-row>
    </el-form>
  </div>


</template>

<script>
import {
  param2Obj
} from '@/utils'
import { Message } from 'element-ui'
import { send_request } from '@/api/httptest'


export default {
  name: 'RequestUrl',
  components: {},
  props: {},
  data() {
    const checkUrl = (rule, value, callback) => {
        if (!this.urlForm.url.startsWith('http')) {
          return callback(new Error('请求地址为http或https开头'))
        }
      }
    return {
      urlForm: {
        url: '',
        method:'GET',
        params: ''//Params项后临时组装参数
      },
      body_type:0 ,//请求类型 默认为0 none ，1 json 2 form 3 x_form 
      body_data:'', //请求体参数
      body_headers:{},//请求头参数
      methodList: ['GET', 'POST', 'PUT', 'DELETE'],
      addrules: {
        url:[
          {requirte:true,validator: checkUrl,trigger:'blur'}
        ]
      }

    }
  },
  watch: {
    
  },
  computed: {},
  methods: {
    //       { 
    // "method": "POST",
    //  "url": "http://127.0.0.1:8400/api/login",
    //  "body": "{\"username\":\"admin\",\"password\":\"123456\"}",
    // "body_type": 3, 
    // "headers": {} }
    debugrequest() {
      try{
        send_request(
          {
            method: this.urlForm.method, //请求方法
            url: this.urlForm.url, //请求url
            body_type: this.body_type, //body类型 none  json form x_form
            body: this.body_data,
            headers:this.body_headers
          }
        ).then(response=>{
          this.$bus.$emit('show_response',response)
        })

      }catch{
        Message.error('请求失败')
      }

    }
  },
  created() {

  },
  mounted() {
    //处理params ，拼接到url
    this.$bus.$on('send_param', (result) => {
      console.log('接收result:', result)
      //result =>[{'a':'1','b':2}]=>?a=1&b=2
      // result.forEach((item, index) => {
      //   console.log("item:", item, index)
      //   let temp_url = this.urlForm.url.split('?')[0]
      //   let obj_to_param = ''
      //   obj_to_param = Object.keys(item).map(key => key + '=' + item[key]).join('&')
      //   if (obj_to_param.length !== 0) {
      //     this.urlForm.params = '?' + obj_to_param
      //     console.log('转换结果：', this.urlForm.params)
      //     this.urlForm.url = temp_url + this.urlForm.params
      //   }
      //   else {
      //     this.urlForm.url = temp_url
      //   }

      // })

        //result =>{'a':'1','b':2}=>?a=1&b=2
        let temp_url = this.urlForm.url.split('?')[0]
        let obj_to_param = ''
        obj_to_param = Object.keys(result).map(key => key + '=' + result[key]).join('&')
        if (obj_to_param.length !==0){
          this.urlForm.params ='?'+obj_to_param
          this.urlForm.url =temp_url+this.urlForm.params
        }
        else{
          this.urlForm.url=temp_url
        }


    }),
    //接收headers
    this.$bus.$on('send_header',(result)=>{
      console.log('receive_header',result)
      this.body_headers =result

    })
    //接收body
    this.$bus.$on('send_body_data',result=>{
      console.log('send_body_data',result)
      this.body_data =result.data
      this.body_type=result.type
    })
  }

}
</script>

<style lang="scss" scoped>
.urlclass {
  margin-bottom: 0px;
}
</style>
