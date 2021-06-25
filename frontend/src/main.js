import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './plugins/ant-design-vue.js'
import axios from 'axios'
import VueAxios from 'vue-axios'
import md5 from 'js-md5'
import BaiduMap from 'vue-baidu-map'

Vue.use(BaiduMap, {
  // ak 是在百度地图开发者平台申请的密钥 详见 http://lbsyun.baidu.com/apiconsole/key */
  ak: 'Ur6D7GxIvSY4eegG2qw9Ukr2UhNneZxt'
})
Vue.use(VueAxios,axios)
Vue.prototype.$md5 = md5
Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
