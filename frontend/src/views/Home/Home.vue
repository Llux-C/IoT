<template>
  <div class="home" style="minheight: calc(100vh - 139px)">
    <br />
    <a-carousel autoplay autoplaySpeed="100" style="">
      <!-- photo 1 -->
      <div>
        <a @click="goTo('/login')"><img src="../../assets/1.jpeg" /></a>
      </div>
      <!-- photo 2 -->
      <div>
        <a @click="goTo('/login')"><img src="../../assets/2.jpeg" /></a>
      </div>
    </a-carousel>

    <div class="home-body">
      <h1 class="h1">IoT物联网在线信息系统</h1>
      <p class="text"></p>
    </div>
  </div>
</template>



<script>
export default {
  name: "Home",
  components: {},
  methods: {
    goTo(path) {
      console.log(this.$store.state.user.token);
      this.axios
        .post("/api/tokenLogin", {
          token: this.$store.state.user.token,
        })
        .then((res) => {
          if (res.data.code == 0) {
            this.$router.push("/user/info");
          } else this.$router.push(path);
        });
    },
    
  },
  mounted(){
      console.log(this.$store.state.user.token)
  }
};
</script>

<style scoped>
.home {
  text-align: center;
  background-color: white;
}
.text {
  font-size: 16px;
}
.h1 {
  margin-top: 30px;
  font-size: 30px;
}
.home-body {
  padding: 0 30px;
}
.ant-carousel >>> .slick-slide {
  text-align: center;
  overflow: hidden;
}
.ant-carousel >>> .slick-slide img {
  display: block;
  margin: auto;
  max-width: 100%;
}
</style>