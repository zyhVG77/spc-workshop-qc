<template>
  <div class="main-container">
    <div class="page-header">
      <ol class="breadcrumb">
        <li class="breadcrumb-item">SPC控制图</li>
      </ol>
    </div>

    <div class="row gutters" v-show="current === 0">
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
        <div class="card">
          <div class="card-header">
            <div class="title">测量计划列表</div>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table m-0">
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

    <div class="row gutters" v-show="current === 1">
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12" @click="back">
        <div class="ml-2 back-btn">
          <span class="icon-log-out"></span> 返回
        </div>
      </div>
      <div class="mb-4"></div>

      <div class="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-6">
        <div class="card">
          <div class="card-header">
            <div class="card-title">基本信息</div>
          </div>
          <div class="card-body">
            <p class="desc">
              测量计划编号：{{ measurePlanSelected.id }}|
              仓库名：{{ measurePlanSelected.warehouse.name }}|
              储位编号：{{ measurePlanSelected.storageCellId }}|
              产品名：{{ measurePlanSelected.product.name }}
              属性名：{{ measurePlanSelected.parameterSelected.id }}|
              单位：{{ measurePlanSelected.parameterSelected.unit }}|
              小数位数：{{ measurePlanSelected.parameterSelected.scale }}|
              控制图类型：{{ measurePlanSelected.parameterSelected.graph_type }}|
              USL：{{ measurePlanSelected.parameterSelected.usl }}|
              LSL：{{ measurePlanSelected.parameterSelected.lsl }}
            </p>
          </div>
        </div>
      </div>
      <div class="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-6">
        <div class="card">
          <div class="card-body">
            <p class="card-title">指定时间段</p>
            <DateRangePicker :triggered="timeTriggered" @submit-date-range="getControlGraphByDateRange($event)" @back="backToDefault"></DateRangePicker>
          </div>
        </div>
      </div>

      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
        <div class="card">
          <div class="card-header">
            <div class="card-title">控制图</div>
          </div>
          <div class="card-body">
            <div id="main" class="chart"></div>
          </div>
        </div>
      </div>

      <!-- Add a button to access abnormality report -->
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
        start_time: '',
        end_time: '',
        analyze: false
      }
      return Object.assign({}, temp)
    }
  },
  data() {
    return {
      // Measure plan infos
      measurePlans: [{
        id: 'M#001',
        warehouse: { id: 'W#001', name: 'Warehouse1' },
        storageCellId: 'S#001',
        product: {
          id: 'P#001',
          name: 'Product',
          parameters: [{
            id: 'Pa#001',
            name: 'Parameter1'
          }, {
            id: 'Pa#002',
            name: 'Parameter2'
          }, {
            id: 'Pa#003',
            name: 'Parameter3'
          }],
        },
        batchSize: 12,
        batch: 100,
        parameterSelected: { id: 'Pa#001' }
      }, {
        id: 'M#001',
        warehouse: { id: 'W#001', name: 'Warehouse1' },
        storageCellId: 'S#001',
        product: {
          id: 'P#001',
          name: 'Product',
          parameters: [{
            id: 'Pa#001',
            name: 'Parameter1'
          }, {
            id: 'Pa#002',
            name: 'Parameter2'
          }, {
            id: 'Pa#003',
            name: 'Parameter3'
          }]
        },
        batchSize: 12,
        batch: 100,
        parameterSelected: { id: 'Pa#001' }
      }],
      measurePlanSelected: {},
      timeRange: null,
      timeTriggered: false,
      // E-charts obj
      myChart: null,
      // Page controls
      current: 1,
    }
  },
  methods: {
    getControlGraphByDefault(k) {
      this.measurePlanSelected = this.measurePlans[k]
      this.measurePlanSelected.parameterSelected =
          this.measurePlanSelected.product.parameters.find(p => p.id = this.measurePlanSelected.parameterSelected.id)

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
      req.start_time = this.range.start
      req.end_time = this.range.end
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
      this.measurePlanSelected = {}
      this.timeRange = null
    }
  },
  mounted() {
    // Get all the measure plans to choose
    WarehouseApi.getMeasurePlans(
        plans => {
          this.measurePlans = plans
        },
        err => console.log(err)
    )
    // Add extra info
    this.measurePlans.forEach(item => {
      item['parameterSelected'] = item.product.parameters[0]
    })
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