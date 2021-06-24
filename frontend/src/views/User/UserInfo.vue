<template>
<div>
 <a-card hoverable style="width: 100%" :bordered="false">
    <a-card-meta :title=nickname :description=email>
      <a-avatar
        slot="avatar"
        :src=avatar
        :size="64"
      />
    </a-card-meta>
</a-card>
<a-divider dashed />
<a-row>
      <a-col :span="6">
        昵称修改：
      </a-col>
      <a-col :span="6">
        <a-input ref="nicknameInput" v-model="nickname" :placeholder=nickname>
            <a-icon slot="prefix" type="user" />
        </a-input>
      </a-col>
      <a-col :span="6">
        <a-button type="dashed" style="margin-left:10px" @click="handleSubmitName">确定</a-button>
      </a-col>
      <a-col :span="6" />
</a-row>
<br>
    <a-row>
      <a-col :span="6">
        密码修改：
      </a-col>
      <a-col :span="6">
        <a-input-password
              placeholder="原密码"
              v-model="password1">
        </a-input-password>
      </a-col>
      <a-col :span="6"></a-col>
      <a-col :span="6" />
    </a-row>
<br>
    <a-row>
      <a-col :span="6"></a-col>
      <a-col :span="6">
        <a-input-password
              placeholder="新密码"
              v-model="password2">
        </a-input-password>
      </a-col>
      <a-col :span="6">
        <a-button type="dashed" style="margin-left:10px" @click="handleSubmitPsw">确定</a-button>
      </a-col>
      <a-col :span="6" />
    </a-row>
</div>
</template>

<script>
export default {
    data()
    {
      var email = this.$store.state.user.email
        return{
            avatar:"https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png",
            nickname:"USER",
            email:email,
            password1:'',
            password2:'',
        }
    },
    methods: {
        emitEmpty() {
            this.$refs.nicknameInput.focus();
            this.nickname = '';
        },
        handleSubmitName(e){
          e.preventDefault()
          this.axios.post('/api/alterName',{
            newName:this.nickname,
            token:this.$store.state.user.token
          }).then((res)=>{
            console.log(res)
            window.alert(res.data.msg)
            location.reload()
          })
        },
        handleSubmitPsw(e){
          e.preventDefault()
          var reg = /^[0-9a-zA-Z]+$/;
          if(!reg.test(this.password2)){
                alert("密码只能由数字和字母组成");
            }
          else{
            this.password1 = this.$md5(this.password1)
            this.password2 = this.$md5(this.password2)
            this.axios.post('api/alterPassword',{
              token:this.$store.state.user.token,
              oldPsw:this.password1,
              newPsw:this.password2,
            })
            .then((res)=>{
              console.log(res)
              if(res.data.code==0){
                window.alert("修改成功")
                location.reload()
              }
              else if(res.data.code==-2){
                window.alert("旧密码错误")
              }
              else
                window.alert("其他错误")
            })
          }
          console.log(this.password1,this.password2)
        },
    },
    mounted:function(){
      console.log(this.$store.state.user)
      console.log(this.$store.state.user.name)
      this.axios.get('/api/getUser',{
        params:{
          token:this.$store.state.user.token
        }
      }).then((res)=>{
        if(res.data.code==0){
          this.nickname=res.data.data
          this.$store.commit('setUser',res.data.data)
          
        }
        else
          window.alert("获取用户信息失败，请重新登录！")
      })
    }
}
</script>