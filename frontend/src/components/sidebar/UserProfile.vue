<template>
  <div>
    <div class="user-profile">
      <img :src="user.avatar" class="profile-thumb" alt="User Thumb">
      <span class="status-label"></span>
    </div>
    <h6 class="profile-name">{{ user.username }}</h6>
  </div>
</template>

<script>
export default {
  name: "UserProfile",
  computed: {
    user: function () {
      return this.$store.getters['user/currentUser']
    }
  }
}
</script>

<style scoped>

</style>