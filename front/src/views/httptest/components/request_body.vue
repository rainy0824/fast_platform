<!--
 * @Author: error: git config user.name && git config user.email & please set dead value or install git
 * @Date: 2022-09-23 14:40:55
 * @LastEditors: error: git config user.name && git config user.email & please set dead value or install git
 * @LastEditTime: 2023-01-04 15:54:37
 * @FilePath: /front/src/views/httptest/components/request_body.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <el-card>
    <el-tabs v-model="request_body">
    <el-tab-pane label="Params" name="first">
      <!-- <template #label><strong>Params</strong></template> -->
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
</template>

<script>
import Params from '@/views/httptest/components/params.vue'
import Headers from  '@/views/httptest/components/headers.vue'
import Bodys from  '@/views/httptest/components/body.vue'

export default {
  name:'RequestBody',
  components: {Params,Headers,Bodys},
  props: {},
  data() {
    return {
      request_body:'first',
      
    }
  },
  watch: {
    request_body:{
      handler(){
      },
      deep: true
    }
  },
  computed: {},
  methods: {},
  created() {},
  mounted() {}
}
</script>
<style lang="scss" scoped>

</style>
