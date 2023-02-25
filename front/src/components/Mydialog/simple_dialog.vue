<template>
  <div class="RegDialog" v-if="visible">
    <el-dialog :visible="dialogVisible" v-bind="$attrs" v-on="$listeners" :title="$attrs.title || '办理登记'" width="600px"
      @close="close">
      <template slot="title">
        <slot name="title"></slot>
      </template>
      <slot>
        <el-form :model="formData" ref="formRef" :rules="rules" class="form-style-overlay">
          <el-form-item label="服务进程" prop="server" v-if="list.length !== 0">
            <el-select v-model="formData.server" placeholder="请选择服务进程">
              <el-option v-for="item in list" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="服务进程" prop="server" v-if="treeList.length !== 0">
            <el-select ref="selectRef" v-model="formData.server" placeholder="请选择服务进程" popper-class="regdialog">
              <template slot="empty">
                <el-tree :data="treeList" :props="defaultProps" @node-click="handleNodeClick"></el-tree>
              </template>
            </el-select>
          </el-form-item>
          <el-form-item label="完成日期" prop="data">
            <el-date-picker v-model="formData.data" type="date" placeholder="请选择完成日期">
            </el-date-picker>
          </el-form-item>

          <el-form-item label="经办人" prop="name">
            <el-input v-model.trim="formData.name" maxlength="50" placeholder="请输入经办人"></el-input>
          </el-form-item>
          <el-form-item class="whole-line" label="备注" prop="remark">
            <el-input type="textarea" placeholder="请输入备注" v-model="formData.remark" maxlength="1000" show-word-limit
              :autosize="{ minRows: 6, maxRows: 6 }"></el-input>
          </el-form-item>
        </el-form>
      </slot>
      <template slot="footer">
        <slot name="footer">
          <el-button @click.native="save" checked>保存</el-button>
          <el-button @click.native="cancel">取消</el-button>
        </slot>
      </template>
    </el-dialog>
  </div>
</template>

<script>

export default {
  inheritAttrs: false,
  name: "RegDialog",
  components: {
  },
  props: {
    visible: {
      type: Boolean,
      required: true,
    },
    list: {
      type: Array,
      default: () => {
        return []
      },
    },
    treeList: {
      type: Array,
      default: () => {
        return []
      },
    },
    operator: {
      type: String,
      default: ''
    }
  },
  data() {
    return {

      defaultProps: {
        children: "children",
        label: "label",
      },
      dialogVisible: false,
      formData: {
        server: "",
        data: "",
        name: this.operator,
        remark: "",
      },
      currentId: '',
      rules: {
        server: [
          {
            required: true,
            message: "请选择服务进程",
            trigger: "blur",
          },
        ],
        data: [
          {
            required: true,
            message: "请选择完成日期",
            trigger: "blur",
          },
        ],
        name: [
          {
            required: true,
            message: "请输入经办人",
            trigger: "blur",
          },
        ],
      },
    };
  },
  watch: {
    visible(val) {

      this.dialogVisible = val;
    },
  },
  methods: {
    handleNodeClick(data, node) {
     
      if (!data.children) {
        this.currentId = data.id
        this.$refs.selectRef.blur();
        this.formData.server = data.label;
        let serveName = [];
        function joinName(node) {
          if (!node.parent) return;
          serveName.unshift(node.data.label);
          joinName(node.parent);
        }
        joinName(node);
        this.formData.server = serveName.join(" - ")
      }
    },
    save() {
      typeof this.$refs.formRef.validate === "function" &&
        this.$refs.formRef.validate((valid) => {
         
          if (valid) {
            
            if (this.list.length === 0) {
              this.formData.server = this.currentId
            }
            let formData = { ...this.formData };
            this.$emit("getFormData", formData);
            this.dialogVisible = false;
          }
        });
    },
    cancel() {
      this.dialogVisible = false;
    },
    close() {
      this.$emit("update:visible", false);
      typeof this.$refs.formRef.resetFields === "function" &&
        this.$refs.formRef.resetFields();
    },
  },
};
</script>

<style lang="scss" scoped>
.RegDialog {
  .el-select-dropdown {
    max-height: 230px !important;
    overflow: auto !important;
  }

  .form-style-overlay .el-form-item {
    width: 100%;
    padding-right: 0;

   .el-form-item__content {
      margin-right: 0 !important;
      margin-left: 0 !important;
    }
  }

.el-button {
    width: 80px;
  }

.el-select-approval {
    .el-select-dropdown {
      min-width: initial;
      width: 50% !important;
      left: 0 !important;
      border-top: 1px solid #d6d6d6;
      border-bottom: 1px solid #d6d6d6;
    }

    .el-select-dropdown__item {
      padding: 0;
      border-radius: 6px;

      .el-tree {
        padding: 6px 0;
      }

      .el-tree--highlight-current .el-tree-node.is-current>.el-tree-node__content {
        color: #4260db !important;
      }

      .el-tree-node__label {
        font-size: 14px;
        text-overflow: ellipsis;
        overflow: hidden;
        white-space: nowrap;
        padding-right: 10px;
      }
    }

    .el-select-dropdown__item.hover,
    .el-select-dropdown__item:hover {
      background: #eaeaea;
    }
  }
}
</style>
