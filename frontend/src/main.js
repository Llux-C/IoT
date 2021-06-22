import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './plugins/ant-design-vue.js'
import axios from 'axios'
import VueAxios from 'vue-axios'
import md5 from 'js-md5'

Vue.use(VueAxios,axios)
Vue.prototype.$md5 = md5
Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
