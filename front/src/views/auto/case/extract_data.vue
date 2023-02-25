<!--
 * @Author: error: git config user.name && git config user.email & please set dead value or install git
 * @Date: 2023-01-10 17:15:12
 * @LastEditors: error: git config user.name && git config user.email & please set dead value or install git
 * @LastEditTime: 2023-01-10 21:28:24
 * @FilePath: /front/src/views/auto/case/extract_data.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <div>
    <el-form label-width="50px" size="mini" label-position="right">
        <div class="inline-title" >
            <el-button size="small" type="text" title="提取参数" @click="add_extract_data">
                <i class="el-icon-circle-plus"> Add</i>
            </el-button>
        </div>

        <div>
            <el-form ref="extract_form" :model="extract_form" :rules="extract_form.extract_rules">
                <el-table :data="extract_form.extract_data" border>
                    <el-table-column header-align="center" label="变量名称">
                        <template slot-scope="scope">
                            <el-form-item :prop="'extract_data.' + scope.$index + '.extract_key'"
                                :rules="extract_form.extract_rules.validate_key">
                                <el-input @change="changeKey(scope.row)" v-model.trim="scope.row.extract_key"
                                    placeholder="请输入变量名" clearable autocomplete="off" />
                            </el-form-item>
                        </template>
                    </el-table-column>
                    <el-table-column header-align="center" label="提取值">
                        <template slot-scope="scope">
                            <el-form-item :prop="'extract_data.' + scope.$index + '.extract_value'"
                                :rules="extract_form.extract_rules.validate_value">
                                <el-input @change="changeValue(scope.row, scope.$index)"
                                    v-model.trim="scope.row.extract_value" placeholder="" clearable
                                    autocomplete="off" />
                            </el-form-item>
                        </template>
                    </el-table-column>
                    <el-table-column header-align="center" label="操作" width="100px">
                        <template slot-scope="scope">
                            <el-form-item>
                                <el-button type="danger" icon="el-icon-delete" @click="delrow(scope.$index)" />
                            </el-form-item>
                        </template>
                    </el-table-column>
                </el-table>
            </el-form>
        </div>
        
    </el-form>
  </div>
</template>

<script>
// 这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）

export default {
name: 'ExtractData', 
props: [

],
  components: {
  },
  // 定义属性
  data() {
    return {
        extract_form:{
            extract_data:[],
            extract_rules:{
                validate_key: [
                        { required: true, message: '变量名不能为空', trigger: 'blur' }
                    ],
                validate_value: [
                        { required: true, message: '值不能为空', trigger: 'blur' }
                    ]
            }
        },
        send_extract_data:[] //组装后的extractdata

      
    }
  },
  // 计算属性，会监听依赖属性值随之变化
  computed: {
  },
  // 监控data中的数据变化
  watch: {},
  // 方法集合
  methods: {
    //组装  [{input_key:'a','input_value':1},{input_key:'b','input_value':2}] =>[{a:1},{b:2}]
    hanle_key_value() {
        let arr_kv=[]
        if (this.extract_form.extract_data.length!=0) {
            this.extract_form.extract_data.map(item => {      
                    let extract_kv={} 
                    extract_kv[item.extract_key] = item.extract_value
                    arr_kv.push(extract_kv)
                })
            }
            return arr_kv
        },
    add_extract_data(){
        this.extract_form.extract_data.push({
            extract_key:'',
            extract_value:'body.'
        })

    },
    changeKey(){
        this.send_extract_data =this.hanle_key_value()
        // console.log('dt:',this.send_extract_data)
    },
    changeValue(){
        this.send_extract_data =this.hanle_key_value()
        // console.log('dt:',this.send_extract_data)
        
    },
    delrow(row_index){
        this.extract_form.extract_data.splice(row_index,1)
        this.send_extract_data =this.hanle_key_value()
    }
  },
  // 生命周期 - 创建完成（可以访问当前this实例）
  created() {
    
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