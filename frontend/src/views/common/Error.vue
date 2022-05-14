<template>
  <div class="main-container">
    <div class="page">
      <h1>{{ error_title }}</h1>
      <div class="mb-4"></div>
      <h5>{{ error_message }}</h5>
      <router-link to="/home/welcome" style="text-decoration: underline">返回主页</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "Error",
  data: function () {
    return {
      error_title: '404错误',
      error_message: '抱歉，找不到您需要的资源'
    }
  },
  mounted() {
    const title = this.$route.params.error_title
    const message = this.$route.params.error_message
    if (title && message) {
      this.error_title = title
      this.error_message = message
    }
  }
}
</script>

<style scoped>
.page {
  text-align: center;
  padding-top: 20%
}
</style>
