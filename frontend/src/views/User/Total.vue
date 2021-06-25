<template>
  <div>
    <div style="padding: 5px">
      <a-row :gutter="16">
        <a-col :span="12">
          <a-card hoverable style="margin-top: 5px; margin-bottom: 5px">
            <div
              id="pieChart"
              style="width: 100%; height: 400px; margintop: 10px"
            ></div>
            <a-card-meta title="" style="text-align: center; padding-top: 5px">
              <template slot="description"> 设备在线情况 </template>
            </a-card-meta>
          </a-card>
        </a-col>
        <a-col :span="12">
          <a-card hoverable style="margin-top: 5px; margin-bottom: 5px">
            <div
              id="barChart"
              style="width: 100%; height: 400px; margintop: 10px"
            ></div>
            <a-card-meta title="" style="text-align: center; padding-top: 5px">
              <template slot="description"> 最近七天设备新增情况 </template>
            </a-card-meta>
          </a-card>
        </a-col>
      </a-row>
      <a-row :gutter="16">
          <a-col :span="24">
              <a-card hoverable style="margin-top: 5px; margin-bottom: 5px">
            <div
              id="lineChart"
              style="width: 100%; height: 400px; margintop: 10px"
            ></div>
            <a-card-meta title="" style="text-align: center; padding-top: 5px">
              <template slot="description"> 最近七天接受消息情况 </template>
            </a-card-meta>
          </a-card>
          </a-col>
      </a-row>
    </div>
  </div>
</template>
<script>
import * as echarts from "echarts";

export default {
  name: "Total",
  data() {
    return {
      pieChart: null,
      mypieChart: null,
      barChart: null,
      mybarChart: null,
      lineChart: null,
      mylineChart: null,

      onlineDevice: 0,
      offlineDevice: 0,

      recentDay: [],
      barData: [],

      total:[],
      normal:[],
      alert:[],
    };
  },
  methods: {
    drawPie() {
      var option_pie = {
        tooltip: {
          trigger: "item",
        },
        legend: {
          top: "5%",
          left: "center",
        },
        series: [
          {
            name: "设备在线情况",
            type: "pie",
            radius: ["40%", "70%"],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderColor: "#fff",
              borderWidth: 2,
            },
            label: {
              show: false,
              position: "center",
            },
            emphasis: {
              label: {
                show: true,
                fontSize: "40",
                fontWeight: "bold",
              },
            },
            labelLine: {
              show: false,
            },
            data: [
              { value: this.onlineDevice, name: "在线设备" },
              { value: this.offlineDevice, name: "离线设备" },
            ],
          },
        ],
      };
      option_pie && this.mypieChart.setOption(option_pie);
    },
    drawBar() {
      var option_bar = {
        xAxis: {
          type: "category",
          data: this.recentDay,
        },
        yAxis: {
          type: "value",
        },
        series: [
          {
            data: this.barData,
            type: "bar",
          },
        ],
      };
      option_bar && this.mybarChart.setOption(option_bar);
    },
    drawLine() {
      var option_line = {
        title: {
          text: "",
        },
        tooltip: {
          trigger: "axis",
        },
        legend: {
          data: ["总消息", "报警消息", "正常消息"],
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true,
        },
        toolbox: {
          feature: {
            saveAsImage: {},
          },
        },
        xAxis: {
          type: "category",
          boundaryGap: false,
          data: this.recentDay,
        },
        yAxis: {
          type: "value",
        },
        series: [
          {
            name: "总消息",
            type: "line",
            stack: "总量",
            data: this.total,
          },
          {
            name: "报警消息",
            type: "line",
            stack: "总量",
            data: this.alert,
          },
          {
            name: "正常消息",
            type: "line",
            stack: "总量",
            data: this.normal,
          },
        ],
      };
      option_line && this.mylineChart.setOption(option_line);
    },
    getRecentDevice() {
      this.axios
        .get("/api/getRecentDevice", {
          params: {
            token: this.$store.state.user.token,
          },
        })
        .then((res) => {
          if (res.data.code === 0) {
            console.log(res.data.day);
            this.recentDay = res.data.day;
            this.barData = res.data.count;
            this.drawBar();
          }
        });
    },
    getRecentMessage(){
      this.axios
        .get("/api/getRecentMessage", {
          params: {
            token: this.$store.state.user.token,
          },
        })
        .then((res) => {
          if (res.data.code === 0) {
            this.total = res.data.total;
            this.normal=res.data.normal
            this.alert=res.data.alert
            this.drawLine();
          }
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
            for (var i = 0; i < this.deviceList.length; i++) {
              if (
                this.deviceList[i].code > "device0000" &&
                this.deviceList[i].code < "device0006"
              )
                this.onlineDevice += 1;
              else this.offlineDevice += 1;
            }
            console.log(this.onlineDevice, this.offlineDevice);
            console.log(this.deviceList);
            this.drawPie();
          } else {
            console.log("获取文件失败");
          }
        })
        .catch(function (err) {
          console.log(err);
        });
    },
  },
  mounted: function () {
    this.getDevice()
    this.getRecentDevice()
    this.getRecentMessage()
    // 下面是三个图表的初始化
    if (
      !this.mypieChart &&
      typeof this.mypieChart != "undefined" &&
      this.mypieChart != 0
    ) {
      this.pieChart = document.getElementById("pieChart");
      this.mypieChart = echarts.init(this.pieChart);
    }
    if (
      !this.mybarChart &&
      typeof this.mybarChart != "undefined" &&
      this.mybarChart != 0
    ) {
      this.barChart = document.getElementById("barChart");
      this.mybarChart = echarts.init(this.barChart);
    }
    if (
      !this.mylineChart &&
      typeof this.mylineChart != "undefined" &&
      this.mylineChart != 0
    ) {
      this.lineChart = document.getElementById("lineChart");
      this.mylineChart = echarts.init(this.lineChart);
    }
  },
};
</script>
<style>
</style>