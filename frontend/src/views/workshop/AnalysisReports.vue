<template>
  <div class="main-container">
    <div class="page-header">
      <ol class="breadcrumb">
        <li class="breadcrumb-item">所有异常</li>
      </ol>
      <div class="custom-control custom-switch float-right">
        <input type="checkbox" class="custom-control-input" id="customSwitch1" v-model="onlyUnread">
        <label class="custom-control-label" for="customSwitch1">只看未读</label>
      </div>
    </div>

    <v-dialog-modal
        title='确认删除'
        text='您真的要删除吗？'
        @on-confirm="_deleteReport"
        ref="dialog">
    </v-dialog-modal>

    <div class="row gutters">
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
        <div class="accordion toggle-icons" id="toggleIcons">
          <div class="accordion-container">
            <AnalysisReport v-for="(report, k) in reportsShown" :report="report" :index="k" :key="k" :drop_downs="drop_downs" @delete="deleteReport(k)"></AnalysisReport>
          </div>
        </div>
      </div>
    </div>

    <div class="row gutters" style="text-align: center">
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
        <a href="javascript:void(0);" @click="showMore">{{ hintBarText }}</a>
      </div>
    </div>
  </div>
  <!-- Main container end -->
</template>

<script>
import AnalysisReport from "@/components/workshop/AnalysisReport";
import VDialogModal from "@/components/utils/DialogModal";

const SHOW_INTERVAL = 10
const MORE = "- 查看更多 -"
const NO_MORE = "- 没有更多了 -"

export default {
  name: "AnalysisReports",
  components: {AnalysisReport, VDialogModal},
  data: function () {
    return {
      drop_downs: [],
      onlyUnread: false,
      reportsShown: [],
      reports: [],
      showIdx: 0,
      allShown: false,
      deletingIdx: -1
    }
  },
  computed: {
    hintBarText: function () {
      return this.allShown?NO_MORE:MORE;
    }
    /*reports: function () {
      if (this.onlyUnread)
        return this.$store.getters['exceptions/reports'].filter(r => !r.read)
      else
        return this.$store.getters['exceptions/reports']
    }*/
  },
  watch: {
    onlyUnread: function(val) {
      this.reportsShown = []
      this.showIdx = 0
      if (val)
        this.reports = this.$store.getters['exceptions/reports'].filter(r => !r.read)
      else
        this.reposts = this.$store.getters['exceptions/reports']
      this.expandList()
    }
  },
  methods: {
    showMore() {
      if (!this.allShown)
        this.expandList()
    },
    expandList() {
      this.reports.slice(this.showIdx, this.showIdx+SHOW_INTERVAL).forEach(r => this.reportsShown.push(r))
      this.showIdx += SHOW_INTERVAL
      if (this.showIdx >= this.reports.length) {
        this.showIdx = this.reports.length
        this.allShown = true
      } else {
        this.allShown = false
      }
    },
    deleteReport(idx) {
      this.deletingIdx = idx
      this.$refs.dialog.show()
    },
    _deleteReport() {
      let idx = this.deletingIdx
      this.$store.dispatch('exceptions/deleteReport', idx)
          .then(() => {
            this.reportsShown.splice(idx, 1)
            // shut dropdown
            this.drop_downs.splice(this.drop_downs.findIndex(i => i===idx), 1)
            // refill reports
            this.showIdx--
            // this.expandList()
          })
          .catch(err => console.log(err))
    }
  },
  mounted() {
    this.reports = this.$store.getters['exceptions/reports']
    this.expandList()
  },
  beforeCreate() {
    if (this.$store.getters['exceptions/reports'].length === 0)
      this.$store.dispatch('exceptions/getAllExceptionReports')
  }
}
</script>

<style scoped>

</style>
