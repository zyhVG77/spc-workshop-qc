<template>
  <div class="main-container">
    <div class="page-header">
      <ol class="breadcrumb">
        <li class="breadcrumb-item">SPC控制监管</li>
      </ol>

      <div class="app-actions">
        <button type="button"
                v-for="(workshop, k) in workshops"
                :class='["btn", currentWorkshop === k ? "active" : ""]'
                @click="changeCurrentWorkshop(k)"
                :key="k">
          {{ workshop.workshop_name }}
        </button>
      </div>
    </div>

    <div class="row gutters">
      <div class="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-12">
        <div class="card">
          <div class="card-body">
            <p class="card-title">属性详情</p>
            <p class="desc">
              属性名：{{ para.name }} |
              单位：{{ para.unit }} |
              小数位数：{{ para.scale }} |
              控制图类型：{{ para.graph_type }} |
              USL: {{ para.usl }} |
              LSL: {{ para.lsl }}
            </p>
          </div>
        </div>
      </div>
      <div class="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-12">
        <div class="card">
          <div class="card-body">
            <p class="card-title">指定时间段</p>
            <DateRangePicker :dynamic="dynamic"
                             @submit-date-range="staticControl($event)"
                             @to-dynamic-control="startContinuousUpdating">
            </DateRangePicker>
          </div>
        </div>
      </div>
    </div>

    <div class="row gutters">
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
        <div class="card">
          <div class="card-body">
            <div id="main" class="chart"></div>
          </div>
        </div>
      </div>
    </div>

    <div class="row gutters">
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
        <div class="card">
          <div class="card-body">
            <HintMessage ref="hint" :hintMsg="hintMsg" :isError="true"></HintMessage>
            <button type="button" class="btn btn-primary float-right" @click="getDynamicAnalysisReport">查看当前异常分析报告</button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import DateRangePicker from "@/components/workshop/DateRangePicker";
import * as echarts from 'echarts/core';
import WorkshopApi from "@/api/workshop";
import HintMessage from "@/components/utils/HintMessage";

// E-charts configuration
import {
  TitleComponent,
  ToolboxComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  MarkLineComponent,
} from 'echarts/components';
import {
  LineChart
} from 'echarts/charts';
import {
  CanvasRenderer
} from 'echarts/renderers';

echarts.use(
    [TitleComponent, ToolboxComponent, TooltipComponent, GridComponent, LegendComponent, MarkLineComponent, LineChart, CanvasRenderer]
);

export default {
  name: "ControlGraph",
  components: {HintMessage, DateRangePicker},
  data: function () {
    return {
      currentWorkshop: 0,
      tmp_point_id: null,
      myChart: null,
      int_id: null,
      dynamic: true,
      hintMsg: '',
      dateRange: null
    }
  },
  computed: {
    currentProduct: function() {
      const proIndex = this.$route.params.proIndex
      return this.$store.getters['products/allProducts'][proIndex]
    },
    para: function() {
      const proIndex = this.$route.params.proIndex
      const parIndex = this.$route.params.parIndex
      return this.$store.getters['products/allProducts'][proIndex].parameters[parIndex]
    },
    workshops: function () {
      return this.currentProduct.workshop
    },
    requestTemplate: function () {
      let control_plan_id = this.para.control_plan_id
      let measure_plan_id
      if (this.currentProduct.workshop.length < 1)
        measure_plan_id = null
      else
        measure_plan_id = this.currentProduct.workshop[this.currentWorkshop].measure_plan_id

      return {
        control_plan_id, measure_plan_id,
        start_time: null, end_time: null, tmp_point_id: null,
        analyze: false
      }
    }
  },
  watch: {
    'workshops': function () {
      if (this.workshops.length < 1)
        this.$router.push({name: 'Small404', params: {error_title: '无车间错误', error_message: '抱歉，此产品暂时无车间生产！'}})
    }
  },
  methods: {
    changeCurrentWorkshop: function (k) {
      this.currentWorkshop = k
      // Refresh the Whole Graph
      // Different workshops have different data
      clearInterval(this.int_id)
      this.tmp_point_id = null
      this.startContinuousUpdating()
    },
    startContinuousUpdating: function () {
      this.dynamic = true
      this.getNewControlGraph()
      this.int_id = setInterval(this.getControlGraph, 2000)
    },
    staticControl: function (dateRange) {
      let req = Object.assign({}, this.requestTemplate)
      req.start_time = dateRange.start
      req.end_time = dateRange.end
      WorkshopApi.getControlGraph(req, (options, point) => {
        clearInterval(this.int_id)
        options && this.myChart.setOption(options, true)
        this.tmp_point_id = point
        this.dynamic = false
        this.dateRange = dateRange
      })
    },
    getControlGraph: function () {
      let req = Object.assign({}, this.requestTemplate)
      req.tmp_point_id = this.tmp_point_id
      WorkshopApi.getControlGraph(req, (options, point) => {
        options && this.myChart.setOption(options)
        this.tmp_point_id = point
      })
    },
    getNewControlGraph: function () {
      let req = Object.assign({}, this.requestTemplate)
      req.tmp_point_id = this.tmp_point_id
      WorkshopApi.getControlGraph(req, (options, point) => {
        options && this.myChart.setOption(options, true)
        this.tmp_point_id = point
      })
    },
    getDynamicAnalysisReport: function () {
      let req = Object.assign({}, this.requestTemplate)
      req.tmp_point_id = this.tmp_point_id
      req.analyze = true

      // Handle static one
      if (!this.dynamic) {
        if (this.dateRange) {
          req.start_time = this.dateRange.start
          req.end_time = this.dateRange.end
        }
      }

      WorkshopApi.getDynamicAnalysisReport(req,
          html => {
            localStorage.removeItem('analysisReportHtml')
            localStorage.setItem('analysisReportHtml', html)
            const { href } = this.$router.resolve({path: '/analysis_report_detail'})
            window.open(href, '_blank')
          },
          err => {
            this.hintMsg = err
            this.$refs.hint.show()
          })
    }
  },
  mounted() {
    /*
        Check whether the product is produced by at least one workshop
        if not, go to 404
     */
    if (this.workshops.length < 1)
      this.$router.push({name: 'Small404', params: {error_title: '无车间错误', error_message: '抱歉，此产品暂时无车间生产！'}})

    const chartDom = document.getElementById('main');
    this.myChart = echarts.init(chartDom);
    const my = this.myChart
    window.onresize = function () {
      my.resize()
    }
    this.startContinuousUpdating()
  },
  beforeDestroy() {
    clearInterval(this.int_id)
  }
}
</script>

<style scoped>
.chart {
  width: 100%;
  height: 800px;
}
</style>