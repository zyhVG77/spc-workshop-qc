<template>
  <header class="header">
    <div></div>
    <div class="header-items" >

      <ul class="header-actions">
        <router-link to="/home/analysisReports" v-if="subsys === 'workshop'">
          <i class="icon-calendar1"></i>
        </router-link>
        <li class="dropdown d-none d-sm-block" v-if="subsys === 'workshop'">
          <a href="#" id="notifications" data-toggle="dropdown" aria-haspopup="true">
            <i class="icon-bell"></i>
            <span class="count-label"></span>
          </a>
          <div class="dropdown-menu dropdown-menu-right lrg scrollable-menu" aria-labelledby="notifications">
            <div class="dropdown-menu-header">异常警报 ({{ numberOfUnreadReports }})</div>
            <ul class="header-notifications">
              <li v-for="(report, k) in unreadReports" :key="k">
                <a href="javascript:void(0);" @click="seeDetail(k)">
                  <div class="user-img away">
                    <span class="glyphicon glyphicon-cog"></span>
                  </div>
                  <div class="details">
                    <div class="user-title">{{ report.product }}</div>
                    <div class="noti-details">{{ report.information.substring(0, 15) }}{{ (report.information.length > 15) ? "..." : "" }}</div>
                    <div class="noti-date">{{ report.time }}</div>
                  </div>
                </a>
              </li>
            </ul>
          </div>
        </li>
        <li class="dropdown user-settings">
          <a href="#" id="userSettings" data-toggle="dropdown" aria-haspopup="true">
            <img :src="currentUser.avatar" class="user-avatar" alt="Avatar">
          </a>
          <div class="dropdown-menu dropdown-menu-right" aria-labelledby="userSettings">
            <div class="header-profile-actions">
              <div class="header-user-profile">
                <div class="header-user">
                  <img :src="currentUser.avatar" alt="Admin Template">
                </div>
                <h5>{{ currentUser.name }}</h5>
                <p>{{ currentUser.role }}</p>
              </div>
              <router-link to="/home/accountSettings"><i class="icon-settings1"></i>账户设置</router-link>
              <a href="javascript:void(0);" @click="logout"><i class="icon-log-out1"></i>退出</a>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </header>
</template>

<script>
export default {
  name: "HeaderBar",
  computed: {
    numberOfUnreadReports: function () {
      return this.$store.getters['exceptions/numberOfUnreadReports']
    },
    unreadReports: function () {
      return this.$store.getters['exceptions/reports'].slice(0, this.numberOfUnreadReports)
    },
    currentUser: function () {
      return this.$store.getters['user/currentUser']
    },
    subsys: function () {
      return this.$store.getters['subsystem_state/current_sub_sys']
    }
  },
  methods: {
    seeDetail: function (index) {
      this.$router.push({path: `/home/analysisReportDetail/${index}`})
    },
    logout: function () {
      this.$store.dispatch('user/logout').then(() => {
        this.$router.push('/login')
      })
    }
  },
  mounted() {
    if (!this.$store.getters['exceptions/hasReport'])
      this.$store.dispatch('exceptions/getAllExceptionReports')
  }
}
</script>

<style scoped>

.scrollable-menu {
  height: auto;
  max-height: 400px;
  overflow-x: hidden;
}

</style>