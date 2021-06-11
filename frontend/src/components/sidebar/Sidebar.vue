<template>
  <nav id="sidebar" class="sidebar-wrapper">
    <div class="sidebar-brand">
      <!-- <a href="index.html" class="logo">
        <img src="img/logo.png" alt="Logo" />
      </a> -->
      <router-link to="/" class="logo">车间生产质量管理</router-link>
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
  components: { ProfileActions, SidebarMenu, UserProfile }
}
</script>

<style scoped>

</style>