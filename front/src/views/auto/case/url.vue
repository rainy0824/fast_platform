<template>
  <div class="shouliTab">
    <!-- <h3 style="color: #333; width: 100%; text-align: center; margin: 10px auto">
      填写表单
    </h3> -->
    <el-form ref="form" :label-position="labelPosition" label-width="120px" :model="form" :rules="rules" size="small">
      <el-tabs style="" tabPosition="top" type="border-card">
        <el-tab-pane>
          <span slot="label"><i class="el-icon-date"></i> 业务类型</span>
          <!-- 表格表单1 -->
          <el-card>
            <el-row>
              <el-col :span="12">
                <el-form-item label="业务来源" prop="busiSoureId">
                  <el-select style="width: 100%" v-model="form.busiSoureId" placeholder="请选择业务来源">
                    <el-option v-for="item in yewulaiyuanObj" :key="item.value" :label="item.value" :value="item.key">
                    </el-option>
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="业务类型" prop="busiTypeId">
                  <el-select style="width: 100%" v-model="form.busiTypeId" placeholder="请选择业务类型">
                    <el-option v-for="item in yewuleixingObj" :key="item.value" :label="item.value" :value="item.key">
                    </el-option>
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="12">
                <el-form-item label="客户名称" prop="customName">
                  <el-input v-model="form.customName"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="联系方式" prop="phoneNumb">
                  <el-input v-model="form.phoneNumb" disabled></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="12">
                <el-form-item v-if="this.form.busiSoureId == '9'" label="客户类别">
                  <el-select style="width: 100%" v-model="form.customLevel" prop="customLevel" placeholder="请选择客户类别">
                    <el-option v-for="item in kehuleibieObj" :key="item.value" :label="item.value" :value="item.key">
                    </el-option>
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item v-if="this.form.busiSoureId == '9'" label="是否购买">
                  <el-select style="width: 100%" v-model="form.isBuy" prop="isBuy" placeholder="是否购买">
                    <el-option v-for="item in shifoumaiObj" :key="item.value" :label="item.value" :value="item.key">
                    </el-option>
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="12">
                <el-form-item label="受理来源">
                  <el-select style="width: 100%" v-model="form.sourceType" disabled placeholder="受理来源">
                    <el-option v-for="item in sourceTypeList" :key="item.value" :label="item.value" :value="item.key"
                      disabled></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="回访时间:" prop="returnTime">
                  <el-date-picker style="width: 100%" v-model="form.returnTime" type="datetime"
                    value-format="yyyy-MM-dd HH:mm:ss" placeholder="选择日期">
                  </el-date-picker>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="12">
                <el-form-item v-if="this.form.busiTypeId == '1'" label="销售人员" prop="salesMan">
                  <el-input v-model="form.salesMan"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="12"> </el-col>
            </el-row>
          </el-card>
          <el-card style="margin-top: 10px">
            <!-- 表格表单2 -->
            <el-row>
              <el-col :span="12">
                <el-form-item label="子公司/片区:" prop="areaInfo">
                  <el-cascader style="width: 100%" v-model="form.areaInfo" :options="areaInfoObj" @change="subChangeOpt"
                    filterable clearable></el-cascader>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="总代理地址:" prop="areaAddress">
                  <el-input v-model="form.areaAddress" prop="areaAddress" placeholder="总代理地址">
                  </el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="12">
                <el-form-item label="总代理姓名:" prop="areaManagerName">
                  <el-input v-model="form.areaManagerName" prop="areaManagerName" placeholder="总代理姓名">
                  </el-input>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="总代理手机号:" prop="areaManPhone">
                  <el-input v-model="form.areaManPhone" prop="areaManPhone" placeholder="总代理手机号">
                  </el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="12">
                <template v-if="this.form.busiTypeId == '2'">
                  <el-form-item label="投诉类型" prop="complainType">
                    <el-cascader v-model="form.complainType" :options="options" clearable @change="fnChangeOpt">
                    </el-cascader>
                  </el-form-item>
                </template>
              </el-col>
              <el-col :span="12"> </el-col>
            </el-row>
          </el-card>
          <el-card style="margin-top: 10px">
            <!-- 表格表单3 -->
            <el-form-item label="咨询内容" prop="consultContent">
              <el-input type="textarea" :autosize="{ minRows: 5, maxRows: 8 }" v-model="form.consultContent"></el-input>
            </el-form-item>
            <el-form-item label="处理意见" prop="dealOpinions">
              <el-input type="textarea" :autosize="{ minRows: 5, maxRows: 8 }" v-model="form.dealOpinions"></el-input>
            </el-form-item>
            <el-form-item v-if="isSendSmsBtn">
              <el-button @click="isSendSms" v-prevent-click size="mini" type="primary">是否需要发送短信</el-button>
            </el-form-item>
            <div v-if="sendSmsBtn">
              <!-- 表格表单3-2 -->
              <el-row>
                <el-col :span="12">
                  <el-form-item label="手机号:" prop="phoneNumbK">
                    <el-input v-model="messageObj.phoneNumb" placeholder="接收短信的手机号">
                    </el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="片区名称:" prop="areaName">
                    <el-input v-model="messageObj.areaName" placeholder="片区名称">
                    </el-input>
                  </el-form-item>
                </el-col>
              </el-row>
              <el-row>
                <el-col :span="12">
                  <el-form-item label="经理姓名:" prop="managerName">
                    <el-input v-model="messageObj.managerName" placeholder="经理姓名">
                    </el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="经理手机:" prop="mobile">
                    <el-input v-model="messageObj.mobile" placeholder="经理手机号">
                    </el-input>
                  </el-form-item>
                </el-col>
              </el-row>

              <el-form-item>
                <el-button size="mini" @click="fnsendmessage" v-prevent-click type="primary">发送短信</el-button>
              </el-form-item>
            </div>
          </el-card>
          <!-- 提交 -->
          <el-row>
            <el-col style="margin-top: 20px; text-align: center; margin-left: -80px">
              <el-form-item>
                <el-button type="primary" v-if="this.form.busiTypeId == 2" @click="confirmSubmit('form')">保存并发起工单
                </el-button>
                <el-button type="primary" @click="saveAccwept('form')">保存</el-button>
              </el-form-item>
            </el-col>
          </el-row>
        </el-tab-pane>
        <el-tab-pane label="历史受理单">
          <el-table height="100%" :data="tableData" v-loading="loading" highlight-current-row ref="multipleTable">
            <el-table-column type="index" width="55px"> </el-table-column>
            <!-- <el-table-column type="selection" width="55px"> </el-table-column> -->
            <el-table-column prop="id" label="受理编号" show-overflow-tooltip></el-table-column>
            <el-table-column prop="busiSoureId" label="业务来源" show-overflow-tooltip>
              <template slot-scope="scope">
                <span>{{ getAcceptSource(scope.row.busiSoureId) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="busiTypeId" label="业务类型" show-overflow-tooltip>
              <template slot-scope="scope">
                <span>{{ getAcceptType(scope.row.busiTypeId) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="customName" label="客户姓名" show-overflow-tooltip></el-table-column>
            <el-table-column prop="phoneNumb" label="来源号码" show-overflow-tooltip></el-table-column>
            <!-- <el-table-column
          prop="subsidiaryName"
          label="子公司"
          show-overflow-tooltip
        >
          <template slot-scope="scope">
            <span>{{ getZigongsiInfo(scope.row.subsidiaryName) }}</span>
          </template>
        </el-table-column> -->
            <el-table-column prop="apccetUserId" label="受理坐席" show-overflow-tooltip></el-table-column>
            <el-table-column label="操作" width="200">
              <!-- <el-button  @click="turnWorkOrder(scope.row)">转工单</el-button> -->
              <el-button type="primary" @click="handleDialogInfo(scope.row)">查看</el-button>
              <!-- <i class="el-icon-my-check" @click="handleDialogInfo(scope.row)"></i> -->
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-form>
    <el-dialog title="受理单详情" :visible.sync="dialogFormVisible" width="30%" size="tiny" show-close>
      <chatSummaryForm :dialogId="dialogId"></chatSummaryForm>
    </el-dialog>
  </div>
</template>

<script>
import chatSummaryForm from "@/view/common/tabs/chat-summary-form"; // 话后小结表单
export default {
  name: "outcall",
  components: {
    chatSummaryForm,
  },
  props: {
    /**
     * 弹窗是否回显
     */
    value: {
      type: Boolean,
    },
    info: {
      type: Object,
    },
  },
  directives: {
    // 自定义指令-防止按钮频发点击
    preventClick: {
      inserted(el, binding) {
        el.addEventListener("click", () => {
          if (!el.disabled) {
            el.disabled = true;
            setTimeout(() => {
              el.disabled = false;
            }, 6000);
          }
        });
      },
    },
  },
  data() {
    return {
      areaInfoObj: [], // 片区子公司obj option
      dialogFormVisible: false,
      labelPosition: "right",
      options: [],
      sendSmsBtn: false,
      tableData: [],
      isSendSmsBtn: true,
      dialogId: true,
      messageObj: {
        mobile: "",
        managerName: "",
        areaName: "",
        phoneNumb: this.info.contactNumber,
        // dunaxin: "",
      },
      form: {
        busiSoureId: "", // 业务来源
        busiTypeId: "", // 业务类型
        customName: "", // 客户姓名
        phoneNumb: this.info.contactNumber, // 联系方式-电话号码
        customLevel: "", // 客户类别
        isBuy: "", // 是否购买
        // serviceLargeType: "", // 省
        // serviceMediumType: "", // 市
        // serviceSmallType: "", // 镇
        // subsidiaryName: "", // 子公司
        areaInfo: "", // 片区-所属片区
        consultContent: "", // 咨询内容
        dealOpinions: "", // 处理意见
        areaManagerName: "", // 片区经理姓名
        areaManPhone: "", // 总代理手机号码
        areaAddress: "", // 总代理地址
        isSendManager: false, // 是否发送短信 0 否 1 是
        complainType: "", // 投诉类型
        returnTime: "", // 回访时间
        salesMan: "", // 销售人员
        id: "",
      },
      rules: {
        busiSoureId: [{ required: true, message: "请选择业务来源" }],
        busiTypeId: [{ required: true, message: "请选择业务类型" }],
        customName: [
          {
            required: true,
            message: "请输入客户信息",
            trigger: "change",
          },
        ],
        phoneNumb: [
          {
            required: true,
            message: "请输入联系方式",
            trigger: "change",
          },
        ],
        customLevel: [
          {
            required: true,
            message: "请选择客户类别",
            trigger: "change",
          },
        ],
        isBuy: [
          {
            required: true,
            message: "请选择是否购买",
            trigger: "change",
          },
        ],
        salesMan: [
          {
            required: true,
            message: "请输入销售人员",
            trigger: "change",
          },
        ],
        // subsidiaryName: [
        //   {
        //     required: true,
        //     message: "请输入子公司",
        //     trigger: "change",
        //   },
        // ],
        areaInfo: [
          {
            required: true,
            message: "请输入片区",
            trigger: "change",
          },
        ],
        areaAddress: [
          {
            required: true,
            message: "请输入总代理地址",
            trigger: "change",
          },
        ],
        areaManagerName: [
          {
            required: true,
            message: "请输入总代理地址",
            trigger: "change",
          },
        ],
        areaManPhone: [
          {
            required: true,
            message: "请输入总代理手机号",
            trigger: "change",
          },
        ],
        complainType: [
          {
            required: true,
            message: "请选择投诉类型",
            trigger: "change",
          },
        ],
        consultContent: [
          {
            required: true,
            message: "请输入咨询内容",
            trigger: "change",
          },
        ],
        dealOpinions: [
          {
            required: true,
            message: "请输入处理意见",
            trigger: "change",
          },
        ],
        returnTime: [
          {
            required: true,
            message: "请输入回访时间",
            trigger: "change",
          },
        ],
        // phoneNumbK: [
        //   {
        //     required: true,
        //     message: "短信接收号码不能为空",
        //     trigger: "change",
        //   },
        // ],
        // areaName: [
        //   {
        //     required: true,
        //     message: "请输入回访时间",
        //     trigger: "change",
        //   },
        // ],
        // managerName: [
        //   {
        //     required: true,
        //     message: "请输入回访时间",
        //     trigger: "change",
        //   },
        // ],
        // mobile: [
        //   {
        //     required: true,
        //     message: "请输入回访时间",
        //     trigger: "change",
        //   },
        // ],
      },
      yewulaiyuanObj: [],
      yewuleixingObj: [],
      kehuleibieObj: [],
      shifoumaiObj: [],
      sourceTypeList: [], // 受理来源
      serviceLargeList: [], // 问题类型第1级
      serviceMediumList: [], // 问题类型第2级
      serviceSmallList: [], // 问题类型第3级
      zigongsiObj: [],
      pianquObj: [],
    };
  },
  created() {
    this.yewulaiyuanObj = JSON.parse(
      sessionStorage.getItem("dics-getAllDatas")
    ).HS_BUSI_SOURCE;
    this.yewuleixingObj = JSON.parse(
      sessionStorage.getItem("dics-getAllDatas")
    ).HS_BUSI_TYPE;
    this.kehuleibieObj = JSON.parse(
      sessionStorage.getItem("dics-getAllDatas")
    ).HS_CUSTOM_LEVEL;
    this.shifoumaiObj = JSON.parse(
      sessionStorage.getItem("dics-getAllDatas")
    ).IS_BUY;
    this.zigongsiObj = JSON.parse(
      sessionStorage.getItem("dics-getAllDatas")
    ).SUBDEPT;
    this.pianquObj = JSON.parse(
      sessionStorage.getItem("dics-getAllDatas")
    ).AREA_DICT;
    this.sourceTypeList = JSON.parse(
      sessionStorage.getItem("dics-getAllDatas")
    ).SOURCE_TYPE;
    this.form.sourceType = this.info.callType;
    console.log("*******客户信息*********", this.info);
    if (this.info.customName != "") {
      this.form.customName = this.info.customName;
    }
    if (this.info.customid != "") {
      this.selectCustomInfoById();
    }
    console.log("*****呼叫类型********", this.info.callType);
    console.log(this.value, this.info);
    this.ajaxgetComplain1();
    this.ajaxgetPhoneInfo();
    this.selectAccpetInfoByPhone();
    this.getAreaOptionObj();
  },
  computed: {},
  methods: {
    // 调用子公司-片区信息
    getAreaOptionObj() {
      this.$axios
        .post(this.$apis.ccweb.workOrder.getSubdaryInfoTreeData)
        .then((res) => {
          if (res.data) {
            console.log(res.data);
            this.areaInfoObj = res.data;
          }
        });
    },
    // 片区和子公司选择
    handleAreaInfoChange(v) {
      // console.log(v);
    },
    // 根据客户ID获取客户级别
    selectAccpetInfoByPhone() {
      const params = {
        phoneNumb: this.form.phoneNumb,
      };
      this.$axios
        .post(this.$apis.ccweb.newDataSL.selectAcceptInfoByPhone, params)
        .then((res) => {
          if (res.data) {
            this.tableData = res.data;
          }
        });
    },
    /**
     * 来源类型转换
     */
    getAcceptSource(annoType) {
      const selectType = this.yewulaiyuanObj;
      for (var i in selectType) {
        if (annoType == selectType[i].key) {
          return selectType[i].value;
        }
      }
    },
    /**
     * 获取业务类型
     */
    getAcceptType(annoType) {
      const selectType = this.yewuleixingObj;
      for (var i in selectType) {
        if (annoType == selectType[i].key) {
          return selectType[i].value;
        }
      }
    },
    /**
     * 字典通用方法
     */
    getPianquObjInfo(annoType) {
      const selectType = this.pianquObj;
      for (var i in selectType) {
        if (annoType == selectType[i].key) {
          return selectType[i].value;
        }
      }
    },
    /**
     * 字典通用方法
     */
    getZigongsiInfo(annoType) {
      const selectType = this.zigongsiObj;
      for (var i in selectType) {
        if (annoType == selectType[i].key) {
          return selectType[i].value;
        }
      }
    },
    /**
     * 会话记录详情查看方法函数
     * @param {object} row 当前行
     */
    handleDialogInfo(row) {
      this.dialogId = row.dialogId;
      this.dialogFormVisible = true;
    },
    // 关闭工单
    closeTabwork() {
      this.$emit("closeTabAccept");
    },
    // 改变级联结果的数组为字符串
    fnChangeOpt(e) {
      // console.log(e);
      if (e && e.length > 0) {
        this.form.complainType = e.join(",");
      } else {
        this.form.complainType = "";
      }
      // console.log(this.form.complainType);
    },
    // 改变级联结果的数组为字符串
    subChangeOpt(e) {
      // console.log(e);
      if (e && e.length > 0) {
        this.form.areaInfo = e.join(",");
      } else {
        this.form.areaInfo = "";
      }
      // console.log(this.form.complainType);
    },
    // 获取投诉类型接口
    ajaxgetComplain1() {
      this.$axios
        .post(this.$apis.ccweb.newDataSL.getComplainTree)
        .then((res) => {
          console.log("投诉类型：", res.data);
          if (res.data) {
            this.options = res.data;
          }
        });
    },
    // 根据客户ID获取客户级别
    selectCustomInfoById() {
      const params = {
        id: this.info.customid,
      };
      this.$axios
        .post(this.$apis.ccweb.newDataSL.selectCustomInfoById, params)
        .then((res) => {
          if (res.data) {
            this.form.customLevel = res.data.customLevel;
          }
        });
    },
    // 获取代理信息
    ajaxgetPhoneInfo() {
      const params = {
        phoneNumber: this.info.contactNumber,
      };
      this.$axios
        .post(this.$apis.ccweb.newDataSL.getPhoneInfo, params)
        .then((res) => {
         
          this.form.areaAddress = res.data.generalAgentAddress;
          this.form.areaManPhone = res.data.generalAgentMobile;
          this.form.areaManagerName = res.data.generalAgentName;
        });
    },
    isSendSms() {
      this.sendSmsBtn = true;
      this.isSendSmsBtn = false;
    },
    // 发送短信
    fnsendmessage() {
      if (this.messageObj.areaName == "") {
        this.$message.error("片区名称不能为空");
        return;
      }
      if (this.messageObj.managerName == "") {
        this.$message.error("经理姓名不能为空");
        return;
      }
      if (this.messageObj.mobile == "") {
        this.$message.error("经理手机号码不能为空");
        return;
      }
      if (this.messageObj.phoneNumbK == "") {
        this.$message.error("客户号码不能为空");
        return;
      }
      // console.log("发送短信", this.messageObj);
      const params = this.messageObj;
      this.$axios
        .post(this.$apis.ccweb.newDataSL.sendSms, params)
        .then((res) => {
          if (res) {
            this.$message({
              message: "发送成功!",
              type: "success",
            });
            this.form.isSendManager = true;
          } else {
            this.$message.error("短信发送失败");
          }
        });
    },
    confirmSubmit(formName) {
      this.$confirm("是否发起工单?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.onSubmit(formName);
        })
        .catch(() => {
          // this.$message({
          //   type: "info",
          //   message: "失败",
          // });
        });
    },
    onSubmit(formName) {
      // if (this.areaInfo.length) {
      //   this.areaInfo = this.areaInfo.toString();
      // }
      // this.areaInfo = this.areaInfo.toString();
      // console.log(this.form, "this.form");
      this.$refs[formName].validate((valid) => {
        if (valid) {
          var obj = {
            sourceType: this.info.callType, // 电话来源ID0 入呼，1 外呼
            dialogId: this.info.dialogId, // 会话ID
            customId: this.info.customid, // 客户ID - 第一次没有  往后返回 id 后端是小写 这里注意
            contactId: this.info.contactId, // 会话客户信息ID
          };
          // let params = {};
          Object.assign(obj, this.form);
          this.$axios
            .post(this.$apis.ccweb.newDataSL.insertAcceptInfo, obj)
            .then((res) => {
              if (res.code == 200) {
                this.form.id = res.data.id;
                this.$message.success("保存受理信息成功");
                this.$emit("showWorkOrderPage", res.data);
              } else {
                this.$message.error(res.msg || "保存受理信息失败");
              }
            });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    /**
     * 保存受理信息 不发起工单
     */
    saveAccwept(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          var obj = {
            sourceType: this.info.callType, // 电话来源ID0 入呼，1 外呼
            dialogId: this.info.dialogId, // 会话ID
            customId: this.info.customid, // 客户ID - 第一次没有  往后返回 id 后端是小写 这里注意
            contactId: this.info.contactId, // 会话客户信息ID
          };
          // let params = {};
          Object.assign(obj, this.form);
          this.$axios
            .post(this.$apis.ccweb.newDataSL.insertAcceptInfo, obj)
            .then((res) => {
              if (res.code == 200) {
                this.form.id = res.data.id;
                this.$message.success("保存受理信息成功");
                this.closeTabwork();
              } else {
                this.$message.error(res.msg || "保存受理信息失败");
              }
            });
        } else {
          return false;
        }
      });
    },
    getServiceType(code, type) {
      console.log(code, type); // code 是选中的值 type是自定义
    },
    handleClose() {
      this.$emit("input", false);
      this.form.call = "";
    },
  },
};
</script>
<style lang="stylus" scoped>
/deep/.el-dialog {
  width: 70% !important;
  height: 60% !important;
  overflow: scroll;
}

/deep/.el-tabs__content {
  background: #f5fafe;
  height: 420px;
  overflow-y: scroll;

  .el-tab-pane {
  }
}

.el-textarea {
  textarea {
    padding: 8px; // 设置文本框的 padding
    height: $inputHeight; // 设置文本框的 height
    font-size: $inputFontSize;
    line-height: 21px;
  }
}

.shouliTab { // 表单框
  padding: 10px;
  overflow-y: scroll;
  height: 100%;
}

.hr {
  width: 100%;
  height: 1px;
  background: #ccc;
  margin: 10px 0;
}
.el-card{
  padding:12px;
}
.detail {
  p {
    padding-left: 10px;
    line-height: 30px;
    font-size: 16px;
    color: #606266;
  }
}
</style>