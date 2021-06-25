<template>
  <div>
    <!-- 这个是创造设备的弹窗 -->
    <a-modal v-model="showCreate" title="新建设备" :footer="null">
      <a-form
        :form="form"
        :label-col="{ span: 5 }"
        :wrapper-col="{ span: 12 }"
        @submit="handleSubmitCreate"
      >
        <a-form-item label="设备名称">
          <a-input v-model="createName" />
        </a-form-item>
        <a-tooltip>
          <template slot="title"> 现仅有device0001~device0004的数据 </template>
          <a-form-item label="数据来源">
            <a-input v-model="createCode" />
          </a-form-item>
        </a-tooltip>
        <a-form-item label="设备描述">
          <a-input v-model="createDescription" />
        </a-form-item>
        <a-form-item label="创造者">
          <a-input disabled="true" v-model="user" />
        </a-form-item>
        <a-form-item :wrapper-col="{ span: 12, offset: 5 }">
          <a-button type="primary" html-type="submit"> 确认 </a-button>
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 这个是更改设备信息的弹窗 -->
    <a-modal v-model="showAlter" title="更改设备信息" :footer="null">
      <a-form
        :form="form"
        :label-col="{ span: 5 }"
        :wrapper-col="{ span: 12 }"
        @submit="handleSubmitAlter"
      >
        <a-form-item label="设备名称">
          <a-input v-model="alterName" />
        </a-form-item>
        <a-tooltip>
          <template slot="title"> 现仅有device0001~device0004的数据 </template>
          <a-form-item label="数据来源">
            <a-input v-model="alterCode" />
          </a-form-item>
        </a-tooltip>
        <a-form-item label="设备描述">
          <a-input v-model="alterDescription" />
        </a-form-item>
        <a-form-item label="创建时间">
          <a-input disabled="true" v-model="alterTime" />
        </a-form-item>
        <a-form-item :wrapper-col="{ span: 12, offset: 5 }">
          <a-button type="primary" html-type="submit"> 确认 </a-button>
        </a-form-item>
      </a-form>
    </a-modal>

    <div v-if="!isEmpty" style="position: relative">
      <div style="margin-bottom: 16px">
        <a-button type="dashed" @click="showCreateMadal"> 新建设备 </a-button>
        <div style="float: right">
          <a-input-search
            placeholder="请输入要搜索的关键词"
            style="width: 200px"
            @search="onSearch"
          />
        </div>
      </div>
      <a-table
        :columns="columns"
        :data-source="deviceList"
        :pagination="ipagination1"
        @change="handleTableChange2"
      >
        <span slot="option" slot-scope="text, record">
          <a @click="deleteDevice(record.name)">删 除 </a>
          <a-divider type="vertical" />
          <a
            @click="
              showAlterMadal(
                record.id,
                record.name,
                record.code,
                record.description,
                record.create_time
              )
            "
            >更 改
          </a>
        </span>
      </a-table>
    </div>
  </div>
</template>
<script>
const columns = [
  {
    title: "序号",
    dataIndex: "id",
    width: "8%",
  },
  {
    title: "设备名",
    dataIndex: "name",
    width: "15%",
  },
  {
    title: "数据流",
    dataIndex: "code",
    width: "15%",
  },
  {
    title: "描述",
    dataIndex: "description",
    width: "30%",
  },
  {
    title: "创建日期",
    dataIndex: "create_time",
    width: "22%",
  },
  {
    title: "选项",
    dataIndex: "option",
    width: "10%",
    scopedSlots: { customRender: "option" },
  },
];

export default {
  data() {
    return {
      headers: {
        authorization: "authorization-text",
      },
      columns,
      deviceList: [],
      showCreate: false,
      showAlter: false,

      alterId: 0,
      alterName: "",
      alterCode: "",
      alterDescription: "",
      alterTime: "",
      oldName: "",

      createName: "",
      createCode: "",
      createDescription: "",
      user: this.$store.state.user.name,

      //这个是配置表格分页的参数，antd of vue本身对表格数据就有一定处理了
      ipagination1: {
        current: 1,
        pageSize: 5,
        showTotal: (total, range) => {
          return (
            "第 " + range[0] + " ~ " + range[1] + " 条，共 " + total + " 条"
          );
        },
        showQuickJumper: true,
        showSizeChanger: false,
        total: 0,
      },
    };
  },
  methods: {
    //这个是实现表格分页跳转的函数
    handleTableChange2(pagination, filters, sorter) {
      this.ipagination1.current = pagination.current;
      this.ipagination1.pageSize = pagination.pageSize;
      filters;
      sorter;
    },
    showCreateMadal() {
      this.showCreate = true;
    },
    handleSubmitAlter() {
      this.axios
        .post("/api/alterDevice", {
          id: this.alterId,
          token: this.$store.state.user.token,
          code: this.alterCode,
          newName: this.alterName,
          oldName: this.oldName,
          description: this.alterDescription,
        })
        .then((res) => {
          console.log(res.data);
          window.alert(res.data.msg);
          location.reload();
        });
    },
    handleSubmitCreate() {
      this.axios
        .post("/api/createDevice", {
          token: this.$store.state.user.token,
          code: this.createCode,
          name: this.createName,
          description: this.createDescription,
          user: this.user,
        })
        .then((res) => {
          this.createDescription = "";
          this.createName = "";
          this.createCode = "";
          console.log(res.data);
          window.alert(res.data.msg);
          location.reload();
        });
    },
    showAlterMadal(id, name, code, description, time) {
      this.showAlter = true;
      this.alterId = id;
      this.alterName = name;
      this.alterCode = code;
      this.alterDescription = description;
      this.alterTime = time;
      this.oldName = name;
    },
    onSearch(value) {
      console.log(value);
      this.axios
        .get("/api/selectDevice", {
          params: {
            token: this.$store.state.user.token,
            name: value,
          },
        })
        .then((res) => {
          if (res.data.code === 0) {
            this.deviceList = res.data.data;
          } else {
            console.log("获取文件失败");
          }
        })
        .catch(function (err) {
          console.log(err);
        });
    },

    getDevice() {
      this.axios
        .get("/api/getDevice", {
          params: {
            token: this.$store.state.user.token,
          },
        })
        .then((res) => {
          if (res.data.code === 0) {
            this.deviceList = res.data.data;
            console.log(this.deviceList);
          } else {
            console.log("获取文件失败");
          }
        })
        .catch(function (err) {
          console.log(err);
        });
    },
    deleteDevice(value) {
      console.log("运行了delete:" + value);
      // 这个that很重要哦，this的指向问题
      var that = this;
      this.$confirm({
        title: "您确定删除该设备吗",
        content: "删除了不可恢复哦~",
        okText: "确认",
        okType: "danger",
        cancelText: "取消",
        onOk() {
          console.log("OK");
          that.axios
            .get("/api/deleteDevice", {
              params: {
                token: that.$store.state.user.token,
                name: value,
              },
            })
            .then((res) => {
              window.alert(res.data.msg);
              location.reload();
            });
        },
        onCancel() {
          console.log("Cancel");
        },
      });
    },
  },

  mounted: function () {
    console.log(this.$store.state.user);
    console.log(this.$store.state.user.token);
    this.getDevice();
  },
};
</script>
