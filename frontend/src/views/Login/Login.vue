<template>
  <div class="login">
    <div class="login_form">
      <div class="login_head">
        <img class="logo" src="../../assets/logo.png" />
        <div class="title"> IoT物联网在线信息系统 </div>
      </div>

      <a-form
      id="formLogin"
      class="user-layout-login"
      ref="formLogin"
      :form="form"
      @submit="handleSubmit">
      <a-tabs
        default-active-key="tab1"
        :tabBarStyle="{ textAlign: 'center', borderBottom: 'unset' }"
        @change="handleTabClick"
      >
       <a-tab-pane key="tab1" tab="登录">
         <a-form-item>
            <a-input
              size="large"
              type="text"
              placeholder="邮箱地址"
              v-decorator="[
                'email',
                {rules: [{ required: true, message:'' }, { validator: checkEmail }], validateTrigger: 'blur'}
              ]"
            >
              <a-icon slot="prefix" type="mail" :style="{ color: 'rgba(0,0,0,.25)' }"/>
            </a-input>
          </a-form-item>
            
          <a-form-item>
            <a-input-password
              size="large"
              placeholder="密码"
              v-decorator="[
                'password',
                {rules: [{ required: true, message: '请输入密码'}, { validator: checkPassword }], validateTrigger: 'blur'}
              ]"
            >
              <a-icon slot="prefix" type="lock" :style="{ color: 'rgba(0,0,0,.25)' }"/>
            </a-input-password>
          </a-form-item>
          <a-form-item />
          <!-- TODO: 忘记密码 -->
          <!--
          <a-form-item>
            <router-link
              :to="{ path: '/findPwd'}"
              class="forge-password"
              style="float: right;"
            >忘记密码</router-link>
          </a-form-item>
          -->

          <a-form-item style="margin-top:24px">
            <a-button
              size="large"
              type="primary"
              htmlType="submit"
              class="login-button"
              block
            >登录</a-button>
          </a-form-item>

         </a-tab-pane>

        <a-tab-pane key="tab2" tab="注册">
          <a-form-item>
            <a-input
              size="large"
              type="text"
              placeholder="邮箱地址"
              v-decorator="[
                'email',
                {rules: [{ required: true, message: ''}, { validator: checkEmail }], validateTrigger: 'blur'}
              ]"
            >
              <a-icon slot="prefix" type="mail" :style="{ color: 'rgba(0,0,0,.25)' }"/>
            </a-input>
          </a-form-item>

          <a-form-item>
            <a-input
              size="large"
              type="text"
              placeholder="昵称"
              v-decorator="[
                'username',
                {rules: [{ required: true, message: '请设置昵称'}], validateTrigger: 'blur'}
              ]"
            >
              <a-icon slot="prefix" type="user" :style="{ color: 'rgba(0,0,0,.25)' }"/>
            </a-input>
          </a-form-item>
              
            <a-form-item>
              <a-input-password
                size="large"
                placeholder="密码"
                v-model="psw"
                v-decorator="[
                'password',
                {rules: [{ required: true, message: '请输入密码'}, { validator: checkPassword }], validateTrigger: 'blur'}
              ]"
              >
                <a-icon slot="prefix" type="lock" :style="{ color: 'rgba(0,0,0,.25)' }"/>
              </a-input-password>
            </a-form-item>

            <a-form-item>
              <a-input-password
                size="large"
                placeholder="确认密码"
                v-decorator="[
                'checkpassword',
                {rules: [{ required: true, message: '请确认密码'}, { validator: checkAlreadyPassword }], validateTrigger: 'blur'}
              ]"
              >
                <a-icon slot="prefix" type="lock" :style="{ color: 'rgba(0,0,0,.25)' }"/>
              </a-input-password>
            </a-form-item>

            <!-- TODO: 注册时候需要邮箱接受验证码 -->
            <!-- <a-form-item>
            <a-input-search
              size="large"
              type="text"
              placeholder="验证码"
              @search="sendcode"
              v-decorator="[
                'validcode',
                {rules: [{ required: true, message: '请输入验证码'}], validateTrigger: 'blur'}
              ]"
            >
              <a-icon slot="prefix" type="key" :style="{ color: 'rgba(0,0,0,.25)' }"/>
               <a-button v-if="issend"  slot="enterButton">获取验证码</a-button>
               <a-button v-if="!issend" disabled slot="enterButton">{{ count }}s后可再次发送</a-button>
            </a-input-search>
          </a-form-item> -->

            <a-form-item style="margin-top:24px">
            <a-button
              size="large"
              type="primary"
              htmlType="submit"
              class="login-button"
              block
            >注册</a-button>
          </a-form-item>

         </a-tab-pane>
         

      </a-tabs>
      </a-form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  components: {
  },
  data () {
    return {
      count: 30,
      issend: true,
      customActiveKey: 'tab1',
      psw:"",
      form: this.$form.createForm(this),
    }
  },

  methods:{
    checkEmail (rule, value, callback) {
      const regex = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/
      if (!regex.test(value)) {
        callback('请输入正确的邮箱')
      }
      callback()
    },
    checkPassword (rule, value, callback) {
      const regex =  /^[A-Za-z0-9]{6,}$/

      if (!regex.test(value)) {
        callback('密码只能由数字和字母组成且不少于6位')
      }
      callback()
    },
    checkAlreadyPassword (rule, value, callback) {
      if (value!=this.psw) {
        callback('两次密码不匹配')
      }
      callback()
    },
    // TODO: 注册时候需要邮箱接受验证码
    // sendcode() {
    //   const TIME_COUNT = 60
    //   this.form.validateFields(['email'],(emailError,value)=>{
    //     if(!emailError){
    //         // console.log(value.email)
    //       this.axios.post('/api/sendCaptcha', {
    //       email: value.email,
    //       })
    //       .then( ()=> {
    //         window.alert('验证码已发送，请检查邮箱')
    //         if (!this.timer) {
    //           this.count = TIME_COUNT
    //           this.issend = false
    //           this.timer = setInterval(() => {
    //             if (this.count > 0 && this.count <= TIME_COUNT) {
    //               this.count--;
    //             } else {
    //               this.issend = true;
    //               clearInterval(this.timer);
    //               this.timer = null;
    //             }
    //           }, 1000);
    //         }
    //       })
    //       .catch(function (error) {
    //         console.log(error)
    //         window.alert('验证码发送失败')
    //       });
    //     }
    //     else{
    //       console.log('********emailError');
    //     }
    //   });
    // },

    handleTabClick (key) {
      this.customActiveKey = key
      //this.form.resetFields()
    },

    handleSubmit (e) {
      e.preventDefault()
      const {
        form: { validateFields },
        customActiveKey,
      } = this

      let route = this.$router
      // 处理的是登录
      if(customActiveKey === 'tab1'){
        console.log("login")
        const validateFieldsKey = ['email', 'password']
        validateFields(validateFieldsKey, { force: true }, (err, values) => {
        if (!err) {
          values.password = this.$md5(values.password)
          // tips：该方式传递的参数是json格式
          console.log(values)
          this.axios.post('/api/login', {
            email: values.email,
            password: values.password,
          })
          .then( (response)=> {
            console.log(response);
            if(response.data.code==0)
            {
              window.alert("登录成功")
              // todo: 保存登录信息
              this.$store.commit('setEmail',values.email)
              this.$store.commit('setToken',response.data.data)
              console.log(this.$store.state.user.token)
              console.log(this.$store.state.user.email)
              route.push({path:'/user/info'});
              location.reload()
            }
            else if(response.data.code==1)
            {
              window.alert("密码错误")
            }
            else{
              window.alert("其他错误")
            }
          })
          .catch(function (error) {
            console.log(error);
          });        
        } else {
          console.log("login err")
        }
      })
      }
      // 处理的是注册
      else if(customActiveKey === 'tab2'){
        console.log("register")
         const validateFieldsKey = ['email', 'username', 'password']
        validateFields(validateFieldsKey, { force: true }, (err, values) => {
        if (!err) {
          console.log('login form', values)
          values.password = this.$md5(values.password)

         this.axios.post('/api/register', {
            email: values.email,
            password: values.password,
            name: values.username,
          })
          .then((response)=> {
            console.log(response);
            
            window.alert(response.data.message)
            if(response.data.code === 0){
                location.reload()
            }
          })
          .catch(function (error) {
            console.log(error);
          });
        } else {
          console.log("register err")
        }
      })
      }
    },
  }
}
</script>


<style scoped>
.login_head {
  display: flex;
  justify-content: center;
  align-items: center;
}
.logo {
  width: 40px;
  height: 40px;
}
.title {
  font-size:20px;
  margin-left: 10px;
}
.login {
  width: 100%;
  height: 100%;
  display: flex;
  background-color: #6fa8dc;
  min-width: 1200px;
  min-height: 600px;
}
.login_img {
  height: 100%;
  margin-left: 100px;
  margin-top: 100px;
}
.login_form {
  width: 400px;
  height: 100%;
  background-color: #f8f8f8;
  margin:auto;
  padding-left: 30px;
  padding-right: 30px;
  padding-top: 30px;
  padding-bottom: 30px;
}
</style>