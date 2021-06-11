<template>
  <div class="container">
    <form action="" onsubmit="return false">
      <div class="row justify-content-md-center">
        <div class="col-xl-4 col-lg-5 col-md-6 col-sm-12">
          <div class="login-screen">
            <div class="login-box">
              <a href="#" class="login-logo">登录</a>
              <h5>欢迎来到汽车零部件质量控制平台，<br />请登录您的账户</h5>
              <div class="form-group">
                <input type="text" class="form-control" placeholder="账号" v-model="username"/>
              </div>
              <div class="form-group">
                <input type="password" class="form-control" placeholder="密码" v-model="password"/>
              </div>
              <div class="actions mb-4">
                <div class="custom-control custom-checkbox">
                  <input type="checkbox" class="custom-control-input" id="remember_pwd" v-model="rememberMe">
                  <label class="custom-control-label" for="remember_pwd">记住我</label>
                </div>
                <button type="button" class="btn btn-success" @click="login">登录</button>
              </div>
              <div class="forgot-pwd">
                <a class="link" href="javascript:void(0);" @click="forgetPwd">忘记密码？</a>
              </div>
              <HintMessage ref="error" :hintMsg="errorMsg" :isError="true"></HintMessage>
            </div>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import bcrypt from "bcryptjs"
import HintMessage from "@/components/utils/HintMessage";

export default {
  name: "Login",
  data: () => ({
      username: "",
      password: "",
      rememberMe: false,
      errorMsg: ""
  }),
  components: {
    HintMessage
  },
  methods: {
    forgetPwd: function () {
      this.errorMsg = "请联系管理员修改密码！";
      this.$refs.error.show();
    },
    login: function () {
      const _this = this;
      /*
          Validate Here!
      */
      bcrypt.genSalt(10, function(err, salt) {
        bcrypt.hash(_this.password, salt, function(err, hash) {
          // console.log(hash);
          let username = _this.username
          let password = hash
          console.log(hash)
          let rememberMe = _this.rememberMe
          _this.$store.dispatch('user/login', { username, password, rememberMe})
              .then(() => {
                _this.$router.push({path: '/home'}).catch(() => {})
              })
              .catch(err => {
                _this.errorMsg = err
                _this.$refs.error.show()
              })
        });
      });
    }
  }
}
</script>

<style scoped>

</style>