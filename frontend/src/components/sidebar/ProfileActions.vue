<template>
  <div class="profile-actions">
    <router-link to="/home/accountSettings">
      <i class="icon-settings1"></i>
    </router-link>
    <router-link to="/">
      <i class="icon-home"></i>
    </router-link>
    <a href="javascript:void(0);" class="red" @click="logout">
      <i class="icon-power1"></i>
    </a>
  </div>
</template>

<script>
export default {
  name: "ProfileActions",
  methods: {
    logout: function () {
      this.$store.dispatch('user/logout').then(() => {
        this.$router.push('/login')
      })
    }
  }
}
</script>

<style scoped>

</style>