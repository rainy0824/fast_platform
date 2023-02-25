<!--
 * @Author: error: git config user.name && git config user.email & please set dead value or install git
 * @Date: 2022-12-19 17:34:07
 * @LastEditors: error: git config user.name && git config user.email & please set dead value or install git
 * @LastEditTime: 2023-01-16 21:46:47
 * @FilePath: /front/src/views/auto/case/case_request_info.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <div>
    <el-card>
            <el-button style="float: right; padding: 5px 10px ; margin-right: 50px;" type="primary" @click="save_request_info">保存</el-button>
        <el-tabs v-model="default_select">
            <el-tab-pane label="数据维护" name="first">
                <DataManage  :env_lists="env_lists" />
            </el-tab-pane>
            <el-tab-pane label="前置用例" name="second">
              <PreTestCase />
            </el-tab-pane>
            <el-tab-pane label="SetupHooks" name="third">
              <SetUpHooks />
            </el-tab-pane>
            <el-tab-pane label="接口信息" name="four">
              <InterfaceInfo  :env_lists="env_lists"/>
            </el-tab-pane>
            <el-tab-pane label="参数提取" name="five">
              <ExtractData />
            </el-tab-pane>
            <el-tab-pane label="断言" name="six">
              <AssertData />
            </el-tab-pane>
            <el-tab-pane label="TearDownHooks" name="seven"></el-tab-pane>
        </el-tabs>
    </el-card>
  </div>
</template>

<script>
// 这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）
import DataManage from '@/views/auto/case/data_manage.vue'
import PreTestCase from '@/views/auto/case/pre_testcase.vue'
import InterfaceInfo from '@/views/auto/case/interface_info.vue'
import ExtractData from '@/views/auto/case/extract_data.vue'
import AssertData from '@/views/auto/case/assert_data.vue'
import SetUpHooks from '@/views/auto/case/setup_hooks.vue'
// import aa from '@/views/auto/case/aa.vue'
// import bb from '@/views/auto/case/bb.vue'
import {get_env_lists} from '@/api/env'
export default {
name: 'CaseRequestInfo', 
props: [
],
  components: {
    DataManage,PreTestCase,InterfaceInfo,ExtractData,AssertData,SetUpHooks
  },
  // 定义属性
  data() {
    return {
        default_select:'first',
        env_lists:[]
      
    }
  },
  // 计算属性，会监听依赖属性值随之变化
  computed: {
  },
  // 监控data中的数据变化
  watch: {
    default_select:{
        handler(new_value,o){
            
        },
        deep: true

    }

  },
  // 方法集合
  methods: {
    init_data(){
        //get_env_list 参数暂时写死
        
        get_env_lists(1,10).then(resp=>{
            let res = resp.envs
            res.forEach(item=>{
                this.env_lists.push({
                    env_id:item.environment_id,
                    env_name: item.environment_name,
                    env_url: item.environment_url
                })
            })
        })

    },
    save_request_info(){

    }

  },
  // 生命周期 - 创建完成（可以访问当前this实例）
  created() {
  
    this.init_data()
    
  },
  // 生命周期 - 挂载完成（可以访问DOM元素）
  mounted() {

  },
  beforeCreate() {}, // 生命周期 - 创建之前
  beforeMount() {}, // 生命周期 - 挂载之前
  beforeUpdate() {}, // 生命周期 - 更新之前
  updated() {}, // 生命周期 - 更新之后
  beforeDestroy() {}, // 生命周期 - 销毁之前
  destroyed() {}, // 生命周期 - 销毁完成
  activated() {}, // 如果页面有keep-alive缓存功能，这个函数会触发
}
</script>

<style lang='scss' scoped>
  
</style>