<template>
    
        <a-menu
          mode="inline"
          :default-selected-keys="[]"
          :default-open-keys="['sub1']"
          :style="{ height: '100%', borderRight: 0 }"
        >
          <a-sub-menu key="sub1">
            <span slot="title"><a-icon type="bars" />信息收集</span>
            <a-menu-item key="1" @click="goTo('/user/total')">
                <a-icon type="line-chart" />
              总览
            </a-menu-item>
            <a-menu-item key="2" @click="goTo('/user/message')">
                <a-icon type="message" />
              数据统计
            </a-menu-item>
            <a-menu-item key="3" @click="goTo('/user/device')">
                <a-icon type="link" />
              设备中心
            </a-menu-item>
          </a-sub-menu>
          <a-menu-item key="4" @click="goTo('/user/info')">
              <a-icon type="team" />
              用户中心
          </a-menu-item>
        </a-menu>
        
      
</template>

<script>
export default {
  data() {
    return {
    };
  },
  methods:{
      goTo(path){
          this.$router.push(path);
      }
  }
};
</script>