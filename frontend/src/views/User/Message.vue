<template>
  <div>
    <div v-if="!isEmpty" style="position: relative">
      <div style="margin-bottom: 20px;text-align:center;display:block">
          请选择设备：
        <a-select
            v-decorator="[
              'dataSource',
              { rules: [{ required: true, message: '请选择想要查看的数据来源' }] },
            ]"
            placeholder="请选择设备"
            style="width:400px;margin-right:20px"
            @change="handleSelectChange"
          >
            <a-select-option v-for="item in deviceList" :key="item.id" :value="item.code">
              {{ item.name }}
            </a-select-option>
          </a-select>
          <a-button type="dashed" @click="showData"> 确定 </a-button>
      </div>
      <a-table
        :columns="columns"
        :data-source="messageList"
        :pagination="ipagination1"
        @change="handleTableChange2"
      >
        <span slot="alert" slot-scope="text, record">
          <a-tag color="red" v-if="record.alert">警告</a-tag>
          <a-tag color="blue" v-if="!record.alert">正常</a-tag>
        </span>
      </a-table>
    </div>
    <baidu-map class="bm-view" center="杭州" zoom="10" :scroll-wheel-zoom="true">
      <bm-polyline :path="polylinePath" stroke-color="blue" :stroke-opacity="0.5" :stroke-weight="2"  @lineupdate="updatePolylinePath"></bm-polyline>
    </baidu-map>
  </div>
</template>
<script>
const columns = [
  {
    title: "警告",
    dataIndex: "alert",
    width: "10%",
    scopedSlots: { customRender: "alert" },
  },
  {
    title: "信息",
    dataIndex: "info",
    width: "30%",
  },
  {
    title: "经度",
    dataIndex: "lat",
    width: "15%",
  },
  {
    title: "纬度",
    dataIndex: "lng",
    width: "15%",
  },
  {
    title: "时间",
    dataIndex: "timestamp",
    width: "20%",
  },
  {
    title: "数值",
    dataIndex: "value",
    width: "10%",
  },
];

export default {
  data() {
    return {
      columns,
      deviceList: [],
      messageList:[],
      selectCode:"",
      timer:undefined,

      user: this.$store.state.user.name,

      //地图坐标
      polylinePath: [],

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
    //这个是地图绘制折线
    updatePolylinePath (e) {
      this.polylinePath = e.target.getPath()
    },
    handleSelectChange(value){
        console.log(value)
        this.selectCode=value
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
            console.log("获取设备失败");
          }
        })
        .catch(function (err) {
          console.log(err);
        });
    },
    showData()
    {
        console.log("showData")
        this.getMessage()
    },
    getMessage() {

      this.axios
        .get("/api/getMessage", {
          params: {
            clientId: this.selectCode,
          },
        })
        .then((res) => {
          if (res.data.code === 0) {
            this.messageList = res.data.data;
            console.log(this.messageList);
            var data = []
            for(var i=0;i<this.messageList.length;i++){
              let result = {}
              result.lat = this.messageList[i].lat
              result.lng = this.messageList[i].lng
              data.push(result)
            }
            console.log("here is data")
            console.log(data)
            this.polylinePath=data
          } else {
            console.log("获取消息失败");
          }
        })
        .catch(function (err) {
          console.log(err);
        });
    },
  },

  mounted: function () {
    console.log(this.$store.state.user);
    console.log(this.$store.state.user.token);
    this.getDevice()
    this.timer=setInterval(this.getMessage, 3000)
  },
  beforeDestroy:function(){
      clearInterval(this.timer)
  }
};
</script>
<style>
.bm-view {
  width: 100%;
  height: 600px;
  margin-top:20px
}
</style>