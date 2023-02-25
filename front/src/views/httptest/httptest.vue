<!--
 * @Author: error: git config user.name && git config user.email & please set dead value or install git
 * @Date: 2022-09-23 14:40:55
 * @LastEditors: error: git config user.name && git config user.email & please set dead value or install git
 * @LastEditTime: 2023-01-04 12:27:15
 * @FilePath: /front/src/views/httptest/httptest.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
<div class="wrapper">
  <el-card >
    <div>
      <h3>{{title}}</h3>
      <div class="request_url">
        <h4 class="inline-title">请求信息</h4>
        <RequestUrl />
      </div>
      <div class="request_body">
        <h4 class="inline-title">参数信息</h4>
        <RequestBody />
      </div>
      <div class="response_body">
          <h4 class="inline-title" >响应信息</h4>
        <ResponseBody  />
      </div>
    </div>
  </el-card>
</div>
</template>

<script>
import RequestUrl from '@/views/httptest/components/request_url.vue'
import RequestBody from '@/views/httptest/components/request_body.vue'
import ResponseBody from '@/views/httptest/components/response_body.vue'

export default {
  name: 'HttpTest',
  components: {
    RequestUrl,
    RequestBody,
    ResponseBody
  },
  props: {},
  data() {
    return {
      title: 'HTTP在线调试'

    }
  },
  watch: {},
  computed: {},
  methods: {},
  created() {},
  mounted() {}
}
</script>

<style lang="scss" scoped>
.el-container {
  margin: 24px;
  background-color: red;
}

.el-header {
  background-color: #cab3d1;
  color: #333;
  text-align: left;
  // line-height: 100px;
  // margin-left: 30px;

}

.el-footer {
  background-color: #b3c0d1;
  color: #333;
  text-align: center;
  line-height: 200px;
}

.el-main {
  background-color: #e9eef3;
  color: #333;
  text-align: center;
  line-height: 360px;
  // margin-left: 30px;
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

//加样式
h4::before {
  content: '';
  position: absolute;
  top: 7px;
  left: 0;
  width: 3px;
  height: 14px;
  background: #409eff;
}

</style>
