<template>
  <el-form  label-width="50px" size="mini" label-position="right">
    <div class="inline-title">
      <el-button size="small" type="text" title="添加参数" @click="addParams">
        <i class="el-icon-circle-plus"> Add</i>
      </el-button>
      <el-button type="text" @click="bulkEdit" title="文本编辑">
        {{ showBulk ? "KeyValueEdit" : "BulkEdit" }}
      </el-button>
    </div>
    <div v-show="showBulk">
      <el-input type="textarea" :rows="5" placeholder="请输入内容" v-model="textarea">
      </el-input>
    </div>
    <div v-show="!showBulk">
      <el-form ref="paramform" :model="paramform" :rules="paramform.params_rules">
        <el-table :data="paramform.params_array" border>
          <el-table-column header-align="center" label="KEY">
            <template slot-scope="scope">
              <!--prop 属性必须是带'params_array.'' + scope.$index + 'model绑定的值' -->
              <el-form-item :prop="'params_array.' + scope.$index + '.key'"
                :rules="paramform.params_rules.validate_key" >
                <!-- <el-input @change="changeKey(scope.row)" v-model.trim="scope.row.key" placeholder="请输入key"
                  clearable autocomplete="off"   /> -->
                <el-input  v-model.trim="scope.row.key" placeholder="请输入key"
                  clearable autocomplete="off"   />

              </el-form-item>
            </template>
          </el-table-column>

          <el-table-column header-align="center" label="VALUE">
            <template slot-scope="scope">
              <el-form-item :prop="'params_array.' + scope.$index + '.value'"
                :rules="paramform.params_rules.validate_value">
                <!-- <el-input @change="changeValue(scope.row, scope.$index)" v-model.trim="scope.row.value"
                  placeholder="请输入value" clearable autocomplete="off" /> -->
                <el-input  v-model.trim="scope.row.value"
                  placeholder="请输入value" clearable autocomplete="off" />

              </el-form-item>
            </template>
          </el-table-column>
          <el-table-column header-align="center" label="DESCRIPTION">
            <template slot-scope="scope">
              <el-form-item>                
                <el-input @change="111" v-model.trim="scope.row.description" placeholder="请输入description" autosize
                  clearable />
              </el-form-item>
            </template>
          </el-table-column>
          <el-table-column header-align="center" label="操作" width="100px">
            <template slot-scope="scope">
              <el-form-item>
                <el-button type="danger" icon="el-icon-delete" @click="delParams(scope.$index)" />
              </el-form-item>
            </template>
          </el-table-column>
        </el-table>
      </el-form>
    </div>

  </el-form>
</template>

<script>

export default {
  name: 'Params',
  components: {},
  props: {},
  data() {
    return {

      showBulk: false,
      input_keys: [], //key数组
      input_values: [], //value数组
      paramform: {
        params_array: [], //查询参数
        params_rules: {
          validate_key: [{ required: true, message: '参数不能为空', trigger: 'blur' }],
          validate_value: [{ required: true, message: '参数不能为空', trigger: 'blur' }]
        },
      },
      textarea: '',
      // array_kv: [], //转换结果对象[{'a','1','b':2}]
      obj_kv: {}

    }
  },
  watch: {

    'paramform.params_array': {
      handler: function (value) {
       
        this.obj_kv =this.hanle_key_value()
        this.$bus.$emit('send_param',this.obj_kv)
      },
      deep: true
    },


  },
  computed: {},
  methods: {
    hanle_key_value() {
            let param_kv={}
            if (this.paramform.params_array !== '') {
                this.paramform.params_array.map(item => {
                    
                    param_kv[item.key] = item.value
                })
            }
            return param_kv
        },
    addParams() {

      this.paramform.params_array.push({
        key: '', //key
        value: '', //value
        description: '' //description
      })
     
    },
    delParams(index) { 
      // console.log('index:', index)
      this.paramform.params_array.splice(index, 1)
      this.obj_kv=this.hanle_key_value()
      this.$bus.$emit('send_param', this.obj_kv)

    },
    bulkEdit() {
      if (this.showBulk) {
        this.bulkToKeyValue()
        this.showBulk = false
      } else {
        this.keyvalueToBulk()
        this.showBulk = true
      }
    },
    bulkToKeyValue() {
      //文本转key value
    },
    keyvalueToBulk() {
      // key value 转文本

    },
    changeKey(row_data) { //比较麻烦直接watch监听属性
      //@input 与@change 的不同： @input 是当值输入时就触发; 而@change 是当值变化且失去焦点时触发 同@blur, 只是回调的参数不一样
      this.obj_kv =this.hanle_key_value()
      this.$bus.$emit('send_param',this.obj_kv)

    },
    changeValue(row_data, row_index) {
        this.obj_kv =this.hanle_key_value()
        this.$bus.$emit('send_param', this.obj_kv)

    },
  },
  created() {

  },
  mounted() { }
}
</script>

<style lang="scss" scoped>
.inline-title {
  position: relative;
  margin-top: 0px;
  margin-bottom: 0px;
  padding-left: 11px;
  font-size: 14px;
  font-weight: 600;
  line-height: 30px;
  background: #f7f7fc;
  color: #333333;

}

.a1 {
  background-color: blue;
}
</style>
