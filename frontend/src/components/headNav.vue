<template>
<div>
    <div class="logo">
        <img src="@/assets/logo.png">
    </div>
    <a-menu
        theme="light"
        mode="horizontal"
        :default-selected-keys="['1']"
        :style="{ lineHeight: '64px' }"
      >
        <a-menu-item key="1" @click="goTo('/home')">
            <a-icon type="home" />
          首页
        </a-menu-item>
        <a-menu-item key="2" @click="goTo('/help')">
            <a-icon type="question" />
          使用帮助
        </a-menu-item>
        <a-menu-item key="3" @click="goTo('/contact')">
            <a-icon type="phone" />
          联系我们
        </a-menu-item>
        <a-sub-menu style="float:right;margin-right:20px" v-if="showlogin!=null">
            <span slot="title" class="submenu-title-wrapper"><a-icon type="user" />
          {{showlogin}}
            </span>
            <a-menu-item key="4"  @click="goTo('/user/info')">
            个人中心
            </a-menu-item>
            <a-menu-item key="5" @click="exit()">
              登出
            </a-menu-item>
        </a-sub-menu>
        <a-menu-item key="6" style="float:right;margin-right:20px" v-else @click="goToLogin('/login')">
            <a-icon type="user" />
          登录
        </a-menu-item>
      </a-menu>

    
</div>
</template>
<style scoped>
.logo{
    width: 120px;
    height: 32px;
    margin: 16px 24px 16px 24px;
    float: left;
}.logo img  {
        max-width: 100%;
        max-height: 100%;
        display: block;
        margin: auto;
    }
</style>

<script>
export default {
  data() {
    return {
        showlogin:localStorage.getItem("email"),
    };
  },
  methods:{
      handleSelect(key, keyPath) {
        console.log(key, keyPath);
      },
      goTo(path){
          this.$router.push(path);
      },
      exit(){
          this.$store.commit('logout')
          this.showlogin=null;
      },
      goToLogin(path){
        this.axios.post('/api/tokenLogin',{
          token:this.$store.state.user.token
        }).then((res)=>{
          if(res.data.code == 0){
            this.$router.push("/user/info");
          }
          else
            this.$router.push(path);
        })
      }
  }
};
</script>
