<template>
  <div>
    <!-- Header Start -->
    <div class="accordion-header">
      <a  href="javascript:void(0);" class="collapsed" @click="showOrHideReport">
        {{ report.product+'-'+report.parameter }}
        <span :class='["badge", report.read ? "badge-primary" : "badge-warning"]'>{{ report.read ? "已读" : "未读"}}</span>
      </a>
    </div>
    <!-- Header End -->

    <!-- Detail Start -->
    <div :class='["collapse", drop_downs.indexOf(index) >= 0 ? "show" : ""]'>
      <div class="accordion-body">
        <p>参数名：{{ report.parameter }}</p>
        <p>时间：{{ report.time }}</p>
        <p>测量计划：{{ report.measure_plan }}</p>
        <p>异常点：{{ report.measure_form_id }}</p>
        <p>描述：{{ report.information }}</p>
        <p>原因：{{ report.reason }}</p>
        <button class="btn btn-default" style="float:right; color: cornflowerblue" @click="seeDetail">查看详情</button>
      </div>
    </div>
    <!-- Detail End -->
  </div>
</template>

<script>
export default {
  name: "AnalysisReport",
  props: ['report', 'index', 'drop_downs'],
  methods: {
    showOrHideReport: function () {
      let pos
      if ((pos = this.drop_downs.indexOf(this.index)) >= 0)
        this.drop_downs.splice(pos, 1)
      else
        this.drop_downs.push(this.index)
    },
    seeDetail: function () {
      this.$router.push(`/home/analysisReportDetail/${this.index}`)
    }
  }
}
</script>

<style scoped>

</style>