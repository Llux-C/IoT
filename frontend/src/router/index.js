import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../views/Login/Login.vue'
import Home from '../views/Home/Home.vue'
import Help from '../views/Home/Help.vue'
import Contact from '../views/Home/Contact.vue'

import User from '../views/User/User.vue'
import userInfo from '../views/User/UserInfo.vue'
import Total from '../views/User/Total.vue'
import Message from '../views/User/Message.vue'
import Device from '../views/User/Device.vue'



Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/home',
    name: 'Home',
    component: Home
  },
  {
    path: '/help',
    name: 'Help',
    component: Help
  },
  {
    path: '/contact',
    name: 'Contact',
    component: Contact
  },
  {
    path:'/user',
    name:'User',
    component:User,
    children:[
      {
        path:'total',
        component:Total
      },
      {
        path:'message',
        component:Message
      },
      {
        path:'device',
        component:Device
      },
      {
        path:'info',
        component:userInfo
      },
    ]
  },
  {
    path:'/login',
    name:'Login',
    component:Login
  }
]

const router = new VueRouter({
  routes
})

export default router
