<template>
  <div class="user" style="minHeight:calc(100vh - 139px)">
    <a-layout style="minHeight:calc(100vh - 139px)">
      <a-layout-sider width="250" style="background: #fff">
          <sideNav></sideNav>
      </a-layout-sider>
      <a-layout style="padding: 24px 24px 0">
        <a-layout-content
          :style="{ background: '#fff', padding: '24px 24px', margin: 0, minHeight: '280px' }"
        >
          <router-view />   <!-- 子组件嵌套，在router.js里设置children -->
        </a-layout-content>
      </a-layout>
    </a-layout>
  </div>
</template>

<script>
import sideNav from '../../components/sideNav.vue'

export default {
  name: 'User',
  components: {
      'sideNav':sideNav
  }
}
</script>
