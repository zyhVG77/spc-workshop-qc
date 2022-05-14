<template>
  <body class="page-wrapper">
  <Sidebar></Sidebar>
  <div class="page-content my-wrapper">
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
@import '../assets/css/main.css';
@import '../assets/fonts/style.css';
@import '../assets/css/style-default.css';

.my-wrapper {
  padding-left: 16%;
}
</style>
