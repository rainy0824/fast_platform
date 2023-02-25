<!--
 * @Author: error: git config user.name && git config user.email & please set dead value or install git
 * @Date: 2023-01-13 21:52:35
 * @LastEditors: error: git config user.name && git config user.email & please set dead value or install git
 * @LastEditTime: 2023-01-17 21:28:01
 * @FilePath: /front/src/components/pythoneditor/python_editor.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->

<template>
    <div class="codeEditBox">
      
        <PythonEditor ref="python_editor" v-model="code" @init="editorInit" @input='codeChange' :lang="lang" :options="editorOptions"
            :theme="theme">
        </PythonEditor>
    </div>

</template>>
<script>

import PythonEditor from 'vue2-ace-editor';

export default {
    components: {
        PythonEditor,
    },
    data() { 
        return {
            code: '',
            editorOptions: {
                // 设置代码编辑器的样式
                enableBasicAutocompletion: true, //启用基本自动完成
                enableSnippets: true, // 启用代码段
                enableLiveAutocompletion: true, //启用实时自动完成
                tabSize: 2, //标签大小
                fontSize: 14, //设置字号
                showPrintMargin: false, //去除编辑器里的竖线
            },
            lang: 'python', //编辑器语法格式
            theme: 'ambiance'//主题
        };
    },
    methods: {
        codeChange(val) {
            this.$bus.$emit('send_python_code',this.code) 
        },

        editorInit() {
            /* 主题'ambiance','chaos','chrome','clouds_midnight','cobalt','crimson_editor','dawn','dracula','dreamweaver','eclipse','github',
            'gob','gruvbox','idle_fingers','iplastic','katzenmilch','kr_theme','kuroir','merbivore','merbivore_soft','monokai','mono_industrial',
            'pastel_on_dark','solarized_dark','solarized_light','sqlserver','terminal','textmate','tomorrow','tomorrow_night','tomorrow_night_blue',
            'tomorrow_night_bright','tomorrow_night_eighties','twilight','vibrant_ink','xcode',*/
            require('brace/theme/ambiance'); //与theme中保持一致
            require('brace/ext/language_tools'); //language extension prerequsite...
            require('brace/mode/yaml');
            require('brace/mode/json');
            require('brace/mode/less');
            require('brace/snippets/json');
            require('brace/mode/python');
            require('brace/snippets/python');
        },
    },
    mounted(){
        // console.log('编辑器中的值：' + this.$refs.PythonPythonEditor.editor.getValue())
        this.$bus.$on('resetting_code',result=>{
            this.code =result
        })
    },
    beforeDestroy(){
        this.$bus.$off('resetting_code')
    }
};
</script>


<style scoped>
.codeEditBox {
    width: 100%;
    height: 200px;
    border: 1px solid #dcdce2;
}
</style>
