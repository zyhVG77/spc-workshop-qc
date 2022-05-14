<template>
  <nav id="sidebar" class="side-navbar">
    <div class="side-navbar-wrapper">
      <div class="sidenav-header  d-flex align-items-center justify-content-center">
        <!-- <a href="index.html" class="logo">
          <img src="img/logo.png" alt="Logo" />
        </a> -->
        <router-link to="/" class="logo"><h3>SPC质量控制系统</h3></router-link>
      </div>
      <div class="sidebar-user-details">
        <div class="sidenav-header-inner text-center">
          <!--
          <img  :src="user.avatar" class="my-avatar" alt="User Thumb">
          -->
          <div class="mb-0"></div>
          <span class="status-label"></span>
          <h5 class="profile-name">{{ user.fullname }}</h5>
          <div class="sidenav-heading">
            <!--
            <router-link to="/home/accountSettings">
              <i class="icon-settings1"></i>
            </router-link>
            <router-link to="/">
              <i class="icon-home"></i>
            </router-link>
            -->
            <a href="javascript:void(0);" class="red" @click="logout">
              <i class="icon-power1"></i>
            </a>
          </div>
        </div>
      </div>
      <SidebarMenu class="menu-text"></SidebarMenu>
    </div>
  </nav>
</template>

<script>
import SidebarMenu from "@/components/sidebar/SidebarMenu";

export default {
  name: "Sidebar",
  components: {SidebarMenu},
  computed: {
    user: function () {
      return this.$store.getters['user/currentUser']
    }
  },
  methods: {
    logout: function () {
      this.$store.dispatch('user/logout').then(() => {
        this.$router.push('/login')
        location.reload()
      })
    }
  }
}
</script>

<style scoped>

.menu-text >>> .btn {
  color: #fff;
}

a {
  color: #33b35a
}

nav {
  width: 16%;
  line-height: 1rem;
  height: 100%;
}

.my-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
}
</style>
