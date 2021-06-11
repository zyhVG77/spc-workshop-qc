<template>
  <div class="main-container">
    <div id="loading-wrapper" v-show="loading">
      <div class="spinner-border" role="status">
        <span class="sr-only">Loading...</span>
      </div>
    </div>
    <div class="page-header">
      <ol class="breadcrumb">
        <li class="breadcrumb-item">异常详情</li>
      </ol>
    </div>

    <div class="row gutters">
      <div class="col-xl-9 col-lg-8 col-md-12 col-sm-12 col-12">
        <div class="card">
          <div class="card-header">
            <router-link to="/home/analysisReports">>返回</router-link>
            <div class="card-title">{{ report.title }}</div>
          </div>
          <div class="card-body">
            <div class="search-result">
              <p class="title">事件详情</p>
              <p class="desc">参数名：{{ report.parameter }}</p>
              <p class="desc">时间：{{ report.time }}</p>
              <p class="desc">测量计划：{{ report.measure_plan }}</p>
              <p class="desc">异常点：{{ report.measure_form_id }}</p>
              <p class="desc">描述：{{ report.information }}</p>
            </div>

            <div class="search-result">
              <p class="title">原因</p>
              <p class="desc">{{ report.reason }}</p>
            </div>

            <button type="button" class="btn btn-primary float-right" @click="toReportPage">查看异常报告</button>
          </div>
        </div>
        <HintMessage ref="error" :hintMsg="hintMsg" :isError="true"></HintMessage>
      </div>
    </div>
  </div>
</template>

<script>
import HintMessage from "@/components/utils/HintMessage";

export default {
  name: "AnalysisReportDetail",
  components: {HintMessage},
  data: function () {
    return {
      hintMsg: '',
      loading: false
    }
  },
  computed: {
    index: function () {
      return parseInt(this.$route.params.index)
    },
    report: function () {
      return this.$store.getters['exceptions/reports'][this.index]
    }
  },
  methods: {
    toReportPage: function () {
      // this.$router.push({path: `/api/test`})
      this.loading = true
      this.$store.dispatch('exceptions/getReportDetailHtml', {id: this.report.id, index: this.index})
          .then(html => {
            this.loading = false
            localStorage.removeItem('analysisReportHtml')
            localStorage.setItem('analysisReportHtml', html)
            const { href } = this.$router.resolve({path: '/analysis_report_detail'})
            window.open(href, '_blank')
          })
          .catch(err => console.log(err))
    }
  }
}
</script>

<style scoped>

</style>