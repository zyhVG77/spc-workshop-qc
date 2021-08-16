<template>
  <nav id="sidebar" class="sidebar-wrapper">
    <div class="sidebar-brand">
      <!-- <a href="index.html" class="logo">
        <img src="img/logo.png" alt="Logo" />
      </a> -->
      <router-link to="/" class="logo">{{ title }}</router-link>
    </div>
    <div class="sidebar-user-details">
      <UserProfile></UserProfile>
      <ProfileActions></ProfileActions>
    </div>
    <SidebarMenu></SidebarMenu>
  </nav>
</template>

<script>
import UserProfile from "@/components/sidebar/UserProfile";
import SidebarMenu from "@/components/sidebar/SidebarMenu";
import ProfileActions from "@/components/sidebar/ProfileActions";

export default {
  name: "Sidebar",
  components: { ProfileActions, SidebarMenu, UserProfile },
  computed: {
    title() {
      if (this.$store.getters['subsystem_state/current_sub_sys'] === 'workshop')
        return '车间生产质量监管'
      else
        return '仓储管理平台'
    }
  }
}
</script>

<style scoped>

</style>