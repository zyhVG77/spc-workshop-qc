<template>
  <div class="main-container">
    <div class="page-header">
      <ol class="breadcrumb">
        <li class="breadcrumb-item">所有异常</li>
      </ol>
    </div>

    <div class="row gutters">
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
        <div class="accordion toggle-icons" id="toggleIcons">
          <div class="accordion-container">
            <AnalysisReport v-for="(report, k) in reports" :report="report" :index="k" :key="k" :drop_downs="drop_downs"></AnalysisReport>
          </div>
        </div>
      </div>
    </div>
    <!-- Row end -->
  </div>
  <!-- Main container end -->
</template>

<script>
import AnalysisReport from "@/components/workshop/AnalysisReport";

export default {
  name: "AnalysisReports",
  components: {AnalysisReport},
  data: function () {
    return {
      drop_downs: []
    }
  },
  computed: {
    reports: function () {
      return this.$store.getters['exceptions/reports']
    }
  },
  beforeCreate() {
    if (this.$store.getters['exceptions/reports'].length === 0)
      this.$store.dispatch('exceptions/getAllExceptionReports')
  }
}
</script>

<style scoped>

</style>