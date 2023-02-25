<!--
 * @Author: error: git config user.name && git config user.email & please set dead value or install git
 * @Date: 2022-09-23 14:40:55
 * @LastEditors: error: git config user.name && git config user.email & please set dead value or install git
 * @LastEditTime: 2023-01-09 20:19:24
 * @FilePath: /front/src/views/httptest/components/body.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
    <div>
        <el-form inline :model="BodyForm" label-width="50px" size="mini" label-position="right">
            <div class="flex-box">
            <el-radio-group size="small" v-model="radio_type" @change="radio_type_change">
                <el-radio label="none">none</el-radio>
                <el-radio label="form_data">form-data</el-radio>
                <el-radio label="x-www-form-urlencoded">x-www-form-urlencoded</el-radio>
                <el-radio label="raw">raw</el-radio>
                <!--弹窗组件 通过trigger触发弹窗 click/focus/hover/manual -->
                <!--v-show:频繁切换 v-if:不频繁切换-->
                <el-popover v-show="is_show_display" ref="popoverRef" trigger="click" placement="bottom"
                    :popper-options="{ boundariesElement: 'body' }">
                    <div class="dropdown-menu-item" v-for="language in languageList" :key="language"
                        @click="select_lan(language)">
                        <span>{{ language }}</span>
                    </div>
                    <!--通过插槽属性reference 显示html v-slot:reference <=>#reference -->
                    <!-- <template #reference>
                                        <el-button size="small" type="text" @click="pop_dashboard">
                                            {{selected_language}}
                                            <i v-if="!popoverOpen" class="el-icon-arrow-down" />     
                                            <i v-else class="el-icon-arrow-up"/>
                                        </el-button>
                                    </template> -->
                    <el-button style="margin-right:50px; flex:auto;" size="small" slot="reference" type="text" @click="arrow_up_down">
                        {{ selected_language }}
                        <i v-if="!arrowup_down" class="el-icon-arrow-down" />
                        <i v-else class="el-icon-arrow-up" />
                    </el-button>
                </el-popover>
            </el-radio-group>
            <el-button
                v-show="(radio_type === 'raw' || radio_type === 'x-www-form-urlencoded') && selected_language === 'JSON'"
                size="small" type="text" @click="json_format" style="margin-right:auto">Beautify </el-button>
            </div>
            <div class="form_bottom">
                <My_Json_Editor v-show="radio_type === 'raw' || radio_type === 'x-www-form-urlencoded'" />
                <el-empty description="this request does not have a body" v-show="radio_type ==='none'"></el-empty>
            </div>
        </el-form>
    </div>



</template>

<script>
// 这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）
import My_Json_Editor from '@/components/jsoneditor/json_editor.vue'

export default {
    name: 'Bodys',
    components: {
        My_Json_Editor
    },
    // 定义属性
    data() {
        return {

            radio_type: 'none',//默认值为none
            is_show_display: false,//如果是radio_type=row则显示Button JSON\Text 
            BodyForm: {},
            selected_language: 'JSON',
            languageList: ['JSON', 'Text'],
            arrowup_down: false, //箭头方向
            body_data: {
                type: '', //类型
                data: '' //结果
            },
            enm_radio:{
                    none: 0,
                    json: 1,
                    form_data: 2,
                    x_form: 3
                }
        }
    },
    // 计算属性，会监听依赖属性值随之变化 get() set()
    computed: {


    },
    // 监控data中的数据变化 callback
    watch: {
        radio_type:{
            handler(){
            this.is_show_display = (this.radio_type === 'raw' || this.radio_type === 'x-www-form-urlencoded') ? true : false
            if (this.radio_type === 'raw') { //json
                this.body_data.type = this.enm_radio.json //todo  暂时先写为x_form
               
            }   
            else if (this.radio_type === 'form_data') { //form_data
                //todo 处理form_data
                this.body_data.type = this.enm_radio.form_data
            }
            else if (this.radio_type === 'x-www-form-urlencoded') { //x_form
              
                this.body_data.type = this.enm_radio.x_form
                // this.$bus.$emit('send_body_data', this.body_data)
            }
            else { //none
                this.body_data.type = this.enm_radio.none
                this.body_data.data =''
            }  
          
            this.$bus.$emit('send_body_data', this.body_data)
            },
            deep: true
        },
    },
    // 方法集合
    methods: {
        //切换radio
        radio_type_change(value) {
            this.radio_type = value
           
        },
        //切换上下箭头
        arrow_up_down() {
            this.arrowup_down = !this.arrowup_down
      
        },

        //选择language
        select_lan(value) {
            this.selected_language = value
            this.$refs.popoverRef.doClose() //关闭弹窗 doShow()打开弹窗

        },
        json_format() {
            if(this.body_data.data !==''){
                try {
                    this.body_data.data = JSON.stringify(JSON.parse(this.body_data.data), null, 4);
                    this.$bus.$emit('format_code',this.body_data.data)
                } catch {
                this.$message('JSON格式错误!')
                 } 

            }
        },

    },
    // 生命周期 - 创建完成（可以访问当前this实例）
    created() {

    },
    // 生命周期 - 挂载完成（可以访问DOM元素）
    mounted() {
        this.$bus.$on('send_code',result =>{
           
            if(this.body_data.type === this.enm_radio.json || this.body_data.type === this.enm_radio.x_form){
 
                this.body_data.data =result
                this.$bus.$emit('send_body_data', this.body_data)
            }
        })

    },
    beforeCreate() { }, // 生命周期 - 创建之前
    beforeMount() { }, // 生命周期 - 挂载之前
    beforeUpdate() { }, // 生命周期 - 更新之前
    updated() { }, // 生命周期 - 更新之后
    beforeDestroy() { }, // 生命周期 - 销毁之前
    destroyed() { }, // 生命周期 - 销毁完成
    activated() { }, // 如果页面有keep-alive缓存功能，这个函数会触发
}
</script>

<style lang='scss' scoped>
.flex-box{
     display: flex;
}
.dropdown-menu-item {
    position: relative;
    box-sizing: border-box;
    height: 32px;
    color: #212121;
    font-size: 12px;
    font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, Fira Sans, Droid Sans, Helvetica, Arial, sans-serif;
    ;
    display: flex;
    align-items: center;
    cursor: default;
    -webkit-user-select: none;
    user-select: none;
    padding: 0 40px;

    span {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    &:hover {
        background-color: #EDEDED;
    }

    .container {
        width: 960px;
        margin: 0 auto;
    }

    .row {
        display: flex;
    }

    .col-4 {
        flex: 0 0 33.3333%;
    }



}
</style>