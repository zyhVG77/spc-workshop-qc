<template>
 <div class="my-login-page my-back">
   <section class="h-100">
     <div class="container h-100">
       <div class="row justify-content-md-center h-100">
         <div class="card-wrapper">
           <div class="brand">
             <img src="../../assets/img/logo-2.png" alt="logo">
           </div>
           <div class="card fat">
             <div class="card-body">
               <h4 class="card-title">SPC质量控制系统</h4>
               <form action="" onsubmit="return false"  class="my-login-validation">
                 <div class="form-group">
                   <label>账号</label>
                   <input type="text" class="form-control" name="email" value="" required autofocus v-model="username">
                 </div>

                 <div class="form-group">
                   <label for="password">密码
                     <a href="#" class="float-right" @click="forgetPwd">
                       忘记密码?
                     </a>
                   </label>
                   <input id="password" type="password" class="form-control" name="password" required v-model="password">
                 </div>

                 <div class="form-group">
                   <div class="custom-control custom-checkbox">
                     <input type="checkbox" class="custom-control-input" id="customCheck1" v-model="rememberMe">
                     <label class="custom-control-label" for="customCheck1">记住我</label>
                   </div>
                 </div>

                 <div class="form-group m-0">
                   <button type="submit" class="btn btn-primary btn-block" @click="login">
                     登录
                   </button>
                 </div>
                 <div class="mt-4 text-center">
                   内部系统不开放注册
                 </div>
               </form>
             </div>
           </div>
           <div class="footer">
             问题咨询 - zyhvg77@gmail.com
           </div>
         </div>
       </div>
     </div>
   </section>
 </div>
</template>

<script>

export default {
  name: "NewLogin",
  data: () => ({
    username: "",
    password: "",
    rememberMe: false,
    errorMsg: ""
  }),
  methods: {
    forgetPwd: function () {
      this.$toast.info('请联系管理员修改密码！')
    },
    login: function () {
      let username = this.username
      let password = this.password
      let rememberMe = this.rememberMe
      this.$store.dispatch('user/login', { username, password, rememberMe})
          .then(() => {
            this.$router.push({path: '/home'}).catch(() => {})
          })
          .catch(err => {
            this.$toast.error(err)
          })
    }
  }
}
</script>

<style scoped>
@import '../../assets/css/my-login.css';

.my-back {
  background-color: #f7f9fb;
}

.btn-primary {
  background-color: #33b35a;
}

a {
  color: #33b35a;
}

a:focus {
  color: #33b35a;
}

</style>
