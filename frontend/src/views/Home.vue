<template>
  <body class="page-wrapper">
  <Sidebar></Sidebar>
  <div class="page-content">
    <HeaderBar></HeaderBar>
    <router-view></router-view>
  </div>
  </body>
</template>

<script>
import Sidebar from "@/components/sidebar/Sidebar";
import HeaderBar from "@/components/utils/HeaderBar";

export default {
  name: "index",
  components: {HeaderBar, Sidebar}
}
</script>

<style scoped>
</style>