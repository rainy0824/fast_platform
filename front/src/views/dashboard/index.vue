<!--
 * @Author: error: git config user.name && git config user.email & please set dead value or install git
 * @Date: 2022-09-23 14:40:55
 * @LastEditors: error: git config user.name && git config user.email & please set dead value or install git
 * @LastEditTime: 2022-12-10 02:17:54
 * @FilePath: /front/src/views/dashboard/index.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <div class="dashboard-container">
    <div class="dashboard-text">Hi, {{ name }}</div>
    <br>
    <div><h2>{{ tipMessage }}</h2></div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name:'DashBoard',
  data() {
    return {
      tipMessage: '早上好,来杯☕吧～今天工作也要加油鸭！奥利给！！！🏆'
    }
  },
  computed: {
    ...mapGetters([
      'name'
    ])
  },
  created() {
    const currentHour = (new Date()).getHours()
    if ((currentHour >= 0 && currentHour <= 6) || (currentHour >= 22 && currentHour <= 24)) {
      this.tipMessage = '夜深了,早点下班~明天继续加油😘'
    } else if (currentHour >= 11 && currentHour < 13) {
      this.tipMessage = '中午好,午饭吃什么想好了吗?🤣'
    } else if (currentHour >= 13 && currentHour <= 15) {
      this.tipMessage = '下午好,早上效率如何?今天的计划能完成吗😃'
    } else if (currentHour >= 16 && currentHour <= 18) {
      this.tipMessage = '傍晚好,今天是按时下班还是加班呢🤪'
    } else if (currentHour >= 19 && currentHour <= 21) {
      this.tipMessage = '晚上好,加班辛苦啦~加油🤞'
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
