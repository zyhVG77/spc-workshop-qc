<template>
  <div class="main-container">
    <div class="page">
      <h1>欢迎，{{ this.$store.getters['user/currentUser'].fullname }}</h1>
      <div class="mb-3"></div>
      <h3>您的权限组：<span style="color: #33b35a">{{ this.$store.getters['user/currentUser'].role }}</span></h3>
      <div class="mb-5"></div>
      <h4>请选择<span style="color: #33b35a">左侧边栏</span>上的服务</h4>
    </div>
  </div>
</template>

<script>
export default {
  name: "Welcome"
}
</script>

<style scoped>
.page {
  text-align: center;
  padding-top: 20%
}
</style>
