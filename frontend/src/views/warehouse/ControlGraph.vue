<template>
  <div class="main-container">
    <div class="page-header">
      <ol class="breadcrumb">
        <li class="breadcrumb-item">SPC控制图</li>
      </ol>
    </div>
    <!-- Modal for the detail information of a cell -->
    <div :class='["modal", "fade", "bd-example-modal-xl", "show"]' tabindex="-1" role="dialog"
         :style="current === 0?MODAL_STYLE_WHEN_ACTIVE:MODAL_STYLE_WHEN_HIDE">
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">选择测量计划</h5>
            <button type="button" class="close" @click="closeModal">
              <span>×</span>
            </button>
          </div>
          <div class="modal-body">

    <div class="row gutters" v-show="current === 0">
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
        <div class="card">
          <div class="card-header">
            <div class="title">测量计划列表</div>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-bordered table-danger m-0">
                <thead>
                <tr>
                  <th>测量计划编号</th>
                  <th>仓库名</th>
                  <th>储位编号</th>
                  <th>零件名</th>
                  <th>批容量</th>
                  <th>批数</th>
                  <th>属性</th>
                  <th>操作</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="(p, k) in measurePlans" :key="k">
                  <td>{{ p.id }}</td>
                  <td>{{ p.warehouse.name }}</td>
                  <td>{{ p.storageCellId }}</td>
                  <td>{{ p.product.name }}</td>
                  <td>{{ p.batchSize }}</td>
                  <td>{{ p.batch }}</td>
                  <td class="col-2">
                    <div>
                      <div class="form-group">
                        <select class="form-control form-control-sm" v-model="p.parameterSelected.id">
                          <option v-for="(para, pk) in p.product.parameters" :value="para.id" :key="pk">{{ para.name }}</option>
                        </select>
                      </div>
                    </div>
                  </td>
                  <td>
                    <div class="btn-group-sm">
                      <button class="btn btn-danger" @click="getControlGraphByDefault(k)">查看控制图</button>
                    </div>
                  </td>
                </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

          </div>
        </div>
      </div>
      </div>
      <!-- End of Modal-->

    <div class="row gutters">
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12" @click="back">
        <div class="ml-2 back-btn">
          <span class="icon-log-out"></span><span class="font-weight-bolder">选择测量计划</span>
        </div>
        <div class="mb-4"></div>
      </div>
    </div>

    <div class="row gutters">
    <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
      <div class="card">
        <div class="card-body">
          <p class="font-weight-bold">指定时间段</p>
          <DateRangePicker :triggered="timeTriggered" @submit-date-range="getControlGraphByDateRange($event)" @back="backToDefault"></DateRangePicker>
        </div>
      </div>
    </div>
    </div>

    <div class="row gutters">
      <div class="col-xl-3 col-lg-3 col-md-3 col-sm-3 col-3">
        <div class="card">
          <div class="card-header">
            <div class="card-title">基本信息</div>
          </div>
          <div class="card-body">
            <div class="slimScrollDiv" style="position: relative; width: auto; height: 800px;">
              <ul class="statistics">
                <li>
                  <span class="stat-icon bg-info">
                    <i class="icon-eye1"></i>
                  </span>
                  测量计划编号：{{ measurePlanSelected.id }}
                </li>
                <li>
                  <span class="stat-icon bg-danger">
                    <i class="icon-thumbs-up1"></i>
                  </span>
                  仓库名：{{ measurePlanSelected.warehouse.name }}
                </li>
                <li>
                  <span class="stat-icon bg-warning">
                    <i class="icon-star2"></i>
                  </span>
                  储位编号：{{ measurePlanSelected.storageCellId }}
                </li>
                <li>
                  <span class="stat-icon bg-success">
                    <i class="icon-shopping-bag1"></i>
                  </span>
                  产品名：{{ measurePlanSelected.product.name }}
                </li>
                <li>
                  <span class="stat-icon bg-info">
                    <i class="icon-check-circle"></i>
                  </span>
                  属性名：{{ measurePlanSelected.parameterSelected.id }}
                </li>
                <li>
                  <span class="stat-icon bg-danger">
                    <i class="icon-clipboard"></i>
                  </span>
                  单位：{{ measurePlanSelected.parameterSelected.unit }}
                </li>
                <li>
                  <span class="stat-icon bg-warning">
                    <i class="icon-eye1"></i>
                  </span>
                  小数位数：{{ measurePlanSelected.parameterSelected.scale }}
                </li>
                <li>
                  <span class="stat-icon bg-success">
                    <i class="icon-thumbs-up1"></i>
                  </span>
                  控制图类型：{{ measurePlanSelected.parameterSelected.graph_type }}
                </li>
                <li>
                  <span class="stat-icon bg-info">
                    <i class="icon-star2"></i>
                  </span>
                  USL：{{ measurePlanSelected.parameterSelected.usl }}
                </li>
                <li>
                  <span class="stat-icon bg-danger">
                    <i class="icon-shopping-bag1"></i>
                  </span>
                  LSL：{{ measurePlanSelected.parameterSelected.lsl }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <div class="col-xl-9 col-lg-9 col-md-9 col-sm-9 col-9">
        <div class="card">
          <div class="card-header">
            <div class="card-title">控制图</div>
          </div>
          <div class="card-body">
            <div id="main" class="chart"></div>
          </div>
        </div>
      </div>
      </div>

    <!-- Add a button to access abnormality report -->
    <div class="row gutters">
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
        <div class="card">
          <div class="card-body">
            <button type="button" class="btn btn-primary float-right" @click="getAbnormalityReport">查看当前异常分析报告</button>
          </div>
        </div>
      </div>
    </div>

    </div>
</template>

<script>
import WarehouseApi from "@/api/warehouse"
import * as echarts from 'echarts/core'
import DateRangePicker from "@/components/warehouse/DateRangePicker";

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
  components: {DateRangePicker},
  computed: {
    requestTemplate() {
      let temp = {
        measurePlanId: this.measurePlanSelected.id,
        parameterId: this.measurePlanSelected.parameterSelected.id,
        start_time: null,
        end_time: null,
        analyze: false
      }
      return Object.assign({}, temp)
    }
  },
  data() {
    return {
      // Measure plan infos
      measurePlans: [],
      measurePlanSelected: {
        id: '',
        warehouse: {
          name: '',
          id: ''
        },
        product: {
          name: ''
        },
        parameterSelected: {
          id: '',
          unit: '',
          scale: '',
          graph_type: '',
          usl: '',
          lsl: ''
        }
      },
      timeRange: null,
      timeTriggered: false,
      // E-charts obj
      myChart: null,
      // Page controls
      current: 1,
      MODAL_STYLE_WHEN_HIDE: "display: none",
      MODAL_STYLE_WHEN_ACTIVE: "display: block",
    }
  },
  methods: {
    closeModal() {
      this.current = 1
    },
    getControlGraphByDefault(k) {
      this.measurePlanSelected = this.measurePlans[k]
      this.measurePlanSelected.parameterSelected =
          this.measurePlanSelected.product.parameters.find(p => p.id === this.measurePlanSelected.parameterSelected.id)

      let req = this.requestTemplate
      req.analyze = false
      WarehouseApi.getControlGraph(req,
          option => {
            this.current = 1
            option && this.myChart.setOption(option, true)
            this.timeTriggered = false
          },
          err => {
            console.log(err)
          }
      )
    },
    backToDefault() {
      let req = this.requestTemplate
      req.analyze = false
      WarehouseApi.getControlGraph(req,
          option => {
            option && this.myChart.setOption(option, true)
            this.timeTriggered = false
          },
          err => {
            console.log(err)
          }
      )
    },
    getControlGraphByDateRange(range) {
      this.timeRange = range

      let req = this.requestTemplate
      req.analyze = false
      req.start_time = range.start
      req.end_time = range.end
      WarehouseApi.getControlGraph(req,
          option => {
            option && this.myChart.setOption(option, true)
            this.timeTriggered = true
          },
          err => {
            console.log(err)
          }
      )
    },
    getAbnormalityReport() {
      let req = this.requestTemplate
      if (this.timeTriggered) {
        req.start_time = this.timeRange.start
        req.end_time = this.timeRange.end
      }
      req.analyze = true
      WarehouseApi.getControlGraph(req,
          html => {
            localStorage.removeItem('analysisReportHtml')
            localStorage.setItem('analysisReportHtml', html)
            const { href } = this.$router.resolve({path: '/analysis_report_detail'})
            window.open(href, '_blank')
          },
          err => console.log(err)
      )
    },
    back() {
      this.current = 0
      /*
      this.measurePlanSelected = {
        id: '',
        warehouse: {
          name: '',
          id: ''
        },
        product: {
          name: ''
        },
        parameterSelected: {
          id: '',
          unit: '',
          scale: '',
          graph_type: '',
          usl: '',
          lsl: ''
        }
        this.timeRange = null
        this.myChart.clear()
      }
      */
    }
  },
  mounted() {
    // Get all the measure plans to choose
    WarehouseApi.getMeasurePlans(
        plans => {
          this.measurePlans = plans
          // Add extra info
          this.measurePlans.forEach(item => {
            item['parameterSelected'] = Object.assign({}, item.product.parameters[0])
          })
          // Set default
          this.getControlGraphByDefault(0)
        },
        err => console.log(err)
    )
    // Initialize e-charts
    const chartDom = document.getElementById('main');
    this.myChart = echarts.init(chartDom);
    const my = this.myChart
    window.onresize = function () {
      my.resize()
    }
  }
}
</script>

<style lang="sass" scoped>
.chart
  width: 100%
  height: 800px

.back-btn
  cursor: pointer

.back-btn:hover
  color: #42b983

</style>