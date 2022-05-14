<template>
  <div class="user-profile">
    <div class="user-avatar">
      <img :src="user.avatar">
    </div>
    <h5 class="user-name">{{ user.username }}</h5>
    <h6 class="user-email">{{ user.email }}</h6>
  </div>
</template>

<script>
export default {
  name: "UserDetail",
  computed: {
    user: function () {
      return this.$store.getters['user/currentUser']
    }
  }
}
</script>

<style scoped>

</style>