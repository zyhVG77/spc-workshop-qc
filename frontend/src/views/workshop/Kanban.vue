<template>
  <div class="main-container">
    <div class="page-header">
      <div class="col-xl-3 col-lg-3 col-md-3 col-sm-3 col-12">
        <div class="form-group">
          <select class="form-control" v-model="currentWorkshop">
            <option :value="-1">全部车间</option>
            <option v-for="(w, k) in workshops"
                    :key="k"
                    :value="k">
              {{ w.name }}
            </option>
          </select>
        </div>
      </div>

      <ol class="breadcrumb">
        <h2 class="breadcrumb-item">大屏看板</h2>
      </ol>

      <div class="col-xl-3 col-lg-3 col-md-3 col-sm-3 col-12">
        <clock class="float-right"></clock>
      </div>
    </div>

    <div class="row gutters">
      <div class="col-xl-3 col-lg-3 col-md-3 col-sm-3 col-12">
        <div class="card">
          <div class="card-body">
            <p class="card-title">生产数量</p>
            <h1 class="text-center">{{ numSplit(doneAmount) }}</h1>
            <h5 class="float-right">计划数：{{ numSplit(planAmount) }}</h5>
          </div>
        </div>
        <div class="card">
          <div class="card-body">
            <p class="card-title">生产进度</p>
            <div id="workFinishGraph" class="chart work-finish-chart"></div>
          </div>
        </div>
      </div>
      <div class="col-xl-9 col-lg-9 col-md-9 col-sm-9 col-12">
        <div class="card">
          <div class="card-body">
            <div id="realTimeProductGraph" class="chart real-time-chart"></div>
          </div>
        </div>
      </div>
    </div>
    <div class="row gutters">
      <div class="col-xl-8 col-lg-8 col-md-8 col-sm-8 col-12">
        <div class="card">
          <div class="card-body">
            <div class="card-title">
              安灯状态
              <div class="custom-control custom-switch float-right">
                <input type="checkbox" class="custom-control-input" id="customSwitch1" v-model="antonOnlyAb">
                <label class="custom-control-label" for="customSwitch1">只看异常</label>
              </div>
            </div>
            <div class="table-responsive">
              <table class="table m-0">
                <thead>
                <tr>
                  <th>设备号</th>
                  <th>安灯</th>
                  <th>分类</th>
                  <th>发生时间</th>
                  <th>安灯时长</th>
                  <th>状态</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="(a, k) in antonInfo" :key="k">
                  <td>{{ a.id }}</td>
                  <td><span :class='["badge badge-pill", a.color]'>{{ a.state1 }}</span></td>
                  <td>{{ a.state2 }}</td>
                  <td>{{ a.beginTime }}</td>
                  <td>{{ a.passTime }}</td>
                  <td>{{ a.hdl }}</td>
                </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
        <div class="card">
          <div class="card-body">
            <p class="card-title">设备详情</p>
            <div class="table-responsive">
              <table class="table m-0">
                <thead>
                <tr>
                  <th>设备号</th>
                  <th>产品</th>
                  <th>计划数</th>
                  <th>加工数</th>
                  <th>进度</th>
                  <th>加工状态</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="(m, k) in machineInfo" :key="k">
                  <td>{{ m.id }}</td>
                  <td>{{ m.product }}</td>
                  <td>{{ m.plan }}</td>
                  <td>{{ m.done }}</td>
                  <td>{{ m.rate }}</td>
                  <td>{{ m.state }}</td>
                </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
      <div class="col-xl-4 col-lg-4 col-md-4 col-sm-4 col-12">
        <div class="card">
          <div class="card-body">
            <div id="machineStateGraph" class="chart state-chart"></div>
          </div>
        </div>
      </div>
    </div>
    <div class="row gutters">
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
        <div class="form-group float-right">
          <div class="input-group">
            <div class="input-group-prepend">
              <label class="input-group-text">刷新频率</label>
            </div>
            <select class="custom-select" v-model="freq">
              <option :value="1">1s</option>
              <option :value="2">2s</option>
              <option :value="5">5s</option>
              <option :value="10">10s</option>
              <option :value="-1">不刷新</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import WorkshopApi from "@/api/workshop"
import Clock from "@/components/workshop/Clock"
import * as echarts from "echarts"

const timeFormat = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09']
const wrapTime = function (n) {
  return timeFormat[n] || n
}

export default {
  name: "Kanban",
  components: { Clock },
  data: function () {
    return {
      // User-interface
      workshops: null,
      machines: null,
      currentWorkshop: -1,
      antonOnlyAb: false,

      // refresh
      freq: 1,
      int: null,

      // cache
      productionData: [],

      // graph objs
      workFinishGraph: null,
      machineStateGraph: null,
      realTimeProductGraph: null
    }
  },
  computed: {
    planAmount: function() {
      let res = 0
      if (this.workshops && this.machines) {
        if (this.currentWorkshop === -1) {
          this.machines.forEach(m => res += m.Plan)
        } else {
          this.machines.filter(m => m.MeasurePlanId === this.workshops[this.currentWorkshop].id)
              .forEach(m => res += m.Plan)
        }
      }
      return res
    },
    doneAmount: function() {
      let res = 0
      if (this.workshops && this.machines) {
        if (this.currentWorkshop === -1) {
          this.machines.forEach(m => res += m.Done)
        } else {
          this.machines.filter(m => m.MeasurePlanId === this.workshops[this.currentWorkshop].id)
              .forEach(m => res += m.Done)
        }
      }
      return res
    },
    machineInfo: function() {
      const info = []
      const products = this.$store.getters['products/allProducts']
      if (this.machines) {
        var _machines = this.machines
        if (this.currentWorkshop >= 0)
          _machines = this.machines.filter(m => m.MeasurePlanId === this.workshops[this.currentWorkshop].id)
        _machines && _machines.forEach(m => {
          info.push({
            id: m.Id,
            product: products.find(p => p.id === this.workshops.find(w => w.id === m.MeasurePlanId).productId).name,
            plan: m.Plan,
            done: m.Done,
            rate: ((m.Plan === 0) ? 0 : (m.Done/m.Plan*100).toFixed(2)) + '%',
            state: m.State
          })
        })
      }
      return info
    },
    antonInfo: function () {
      const info = []
      if (this.machines) {
        var _machines = this.machines
        if (this.currentWorkshop >= 0)
          _machines = this.machines.filter(m => m.MeasurePlanId === this.workshops[this.currentWorkshop].id)
        if (this.antonOnlyAb) {
          _machines = _machines.filter(m => m.Anton.State1 === '坏机' || m.Anton.State1 === '损失')
        }
        _machines && _machines.forEach(m => {
          var beg = new Date(m.Anton.BeginTime)
          var dist = new Date() - beg;
          var d = parseInt(dist/1000/60/60/24)
          var h = parseInt(dist/1000/60/60) - d*24
          var mi = parseInt(dist/1000/60) - d*24*60 - h*60
          var p = ''
          if (d !== 0)
            p += d + '天'
          p += h + '时' + mi + '分'
          var c
          switch (m.Anton.State1) {
            case "工作":
              c = 'badge-success';
              break;
            case "坏机":
              c = 'badge-danger';
              break;
            case "损失":
            case "换机":
              c = 'badge-warning';
              break;
            case "计划停机":
              c = 'badge-light';
              break;
            case "停产":
              c = 'badge-dark';
              break;
            default:
              break;
          }
          info.push({
            id: m.Id,
            state1: m.Anton.State1,
            state2: m.Anton.State2,
            desc: m.Anton.Description,
            hdl: m.Anton.Handle,
            beginTime: m.Anton.BeginTime.substr(m.Anton.BeginTime.length - 8),
            passTime: p,
            color: c
          })
        })
      }
      return info
    },
    workFinishOption: function() {
      var rate
      if (this.planAmount === 0)
        rate = 0
      else {
        rate = +(this.doneAmount / this.planAmount * 100).toFixed(2)
      }

      const gaugeData = [{
        value: rate,
        name: '进度',
        title: {
          offsetCenter: ['0%', '-20%']
        },
        detail: {
          valueAnimation: true,
          offsetCenter: ['0%', '20%']
        }
      }];
      return {
        series: [
          {
            type: 'gauge',
            startAngle: 90,
            endAngle: -270,
            pointer: {
              show: false
            },
            progress: {
              show: true,
              overlap: false,
              roundCap: true,
              clip: false,
              itemStyle: {
                borderWidth: 1,
                borderColor: '#464646'
              }
            },
            axisLine: {
              lineStyle: {
                width: 10
              }
            },
            splitLine: {
              show: false,
              distance: 0,
              length: 10
            },
            axisTick: {
              show: false
            },
            axisLabel: {
              show: false,
              distance: 50
            },
            data: gaugeData,
            title: {
              fontSize: 16
            },
            detail: {
              width: 40,
              height: 14,
              fontSize: 14,
              color: 'auto',
              borderColor: 'auto',
              borderRadius: 20,
              borderWidth: 1,
              formatter: '{value}%'
            }
          }
        ]
      }
    },
    machineStateOption: function() {
      var states = [0, 0, 0, 0]
      if (this.machines) {
        var _machines = this.machines
        if (this.currentWorkshop >= 0)
          _machines = this.machines.filter(m => m.MeasurePlanId === this.workshops[this.currentWorkshop].id)
        _machines && _machines.forEach(m => {
          switch (m.State) {
            case "运行":
              states[0]++;
              break;
            case "停止":
              states[1]++;
              break;
            case "离线":
              states[2]++;
              break;
            case "故障":
              states[3]++;
              break;
            default:
              break;
          }
        })
      }
      return {
        title: {
          text: '设备状态',
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left'
        },
        series: [
          {
            name: '机器状态',
            type: 'pie',
            radius: '50%',
            data: [
              { value: states[1], name: '停止' },
              { value: states[0], name: '运行' },
              { value: states[2], name: '离线' },
              { value: states[3], name: '故障' }
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
    },
    realTimeProductOption: function () {
      var data = []
      if (this.currentWorkshop >= 0) {
        const id = this.workshops[this.currentWorkshop].id
        this.productionData.forEach(d => {
          data.push({
            name: d.name,
            value: [d.value[0], d.value[1][id]]
          })
        })
      } else {
        this.productionData.forEach(d => {
          data.push({
            name: d.name,
            value: [d.value[0], d.value[1]['total']]
          })
        })
      }
      return {
        title: {
          left: 'center',
          text: '实时产量变化'
        },
        tooltip: {
          trigger: 'axis',
              formatter: function (params) {
            params = params[0];
            var date = new Date(params.name);
            return (
                date.toLocaleString() +
                '<br/>数量：' +
                params.value[1] +
                '个'
            );
          },
          axisPointer: {
            animation: false
          }
        },
        xAxis: {
          type: 'category',
          name: '时间（分:秒）',
          splitLine: {
            show: false
          }
        },
        yAxis: {
          type: 'value',
          name: '产量/个',
          boundaryGap: [0, '100%'],
          splitLine: {
            show: true
          },
          // max: this.planAmount,
          min: data.length > 0 ? Math.floor(data[0].value[1] * 0.95) : 0
        },
        series: [
          {
            name: 'Data',
            type: 'line',
            showSymbol: false,
            data: data,
            markLine: {
              silent: true,
              data: [{
                name: 'plan',
                yAxis: this.planAmount,
                label: {
                  formatter: '计划数'
                }
              }],
              lineStyle: {
                normal: {
                  type: 'solid',
                  color: "green"
                }
              }
            },
            markPoint: {
              label: {
                normal: {
                  formatter: function (param) {
                    param = param.data
                    let date = new Date(param.name)
                    return wrapTime(date.getMinutes()) + ':' + wrapTime(date.getSeconds()) + ' ' + param.yAxis + '个'
                  },
                  textStyle: {
                    color: '#000'
                  },
                  position: 'top'
                }
              },
              data: [
                data.length > 0 ? {
                  name: data[data.length - 1].name,
                  yAxis: data[data.length - 1].value[1],
                  xAxis: data[data.length - 1].value[0]
                } : {}
              ],
              symbol: 'circle',
              symbolSize: 10,
              itemStyle: {
                color: '#FF4747'
              }
            }
          }
        ]
      }
    }
  },
  watch: {
    freq: function (newF) {
      clearInterval(this.int)
      if (newF > 0) {
        this.int = setInterval(this.synchronize, newF * 1000)
      }
    },
    workFinishOption: function (option) {
      this.workFinishGraph.setOption(option)
    },
    machineStateOption: function (option) {
      this.machineStateGraph.setOption(option)
    },
    currentWorkshop: function () {
      this.realTimeProductGraph.setOption(this.realTimeProductOption, true)
    }
  },
  methods: {
    numSplit: function (n) {
      let str = ''
      let numStr = n.toString()
      for (let i = 0; i < numStr.length; ++i) {
        str += numStr[i]
        let r = numStr.length - i - 1
        if (r !== 0 && r % 3 === 0)
          str += ', '
      }
      return str
    },
    updateProductionGraph: function (info) {
      if (this.productionData.length >= 1000)
        this.productionData.shift()
      let now = new Date()
      var data = {}
      var total = 0
      info.forEach(m => {
        total += m.Done
        if (m.MeasurePlanId in data) {
          data[m.MeasurePlanId] += m.Done
        } else {
          data[m.MeasurePlanId] = m.Done
        }
      })
      data['total'] = total

      this.productionData.push({
        name: now.toString(),
        value: [
            wrapTime(now.getMinutes()) + ':' + wrapTime(now.getSeconds()),
            data
        ]
      })

      this.realTimeProductGraph.setOption(this.realTimeProductOption)
    },
    synchronize: function () {
      WorkshopApi.getKanbanInfo(
          m => {
            this.machines = m
            this.updateProductionGraph(m)
          },
          err => console.log(err)
      )
    }
  },
  mounted() {
    WorkshopApi.getAllWorkshopsInfo(
        w => {
          this.workshops = w
        },
        err => console.log(err)
    )
    this.int = setInterval(this.synchronize, this.freq * 1000)
    this.synchronize()

    // Graphs
    const workFinishGraphDom = document.getElementById('workFinishGraph')
    const machineStateGraphDom = document.getElementById('machineStateGraph')
    const realTimeProductGraphDom = document.getElementById('realTimeProductGraph')
    this.workFinishGraph = echarts.init(workFinishGraphDom)
    this.machineStateGraph = echarts.init(machineStateGraphDom)
    this.realTimeProductGraph = echarts.init(realTimeProductGraphDom)
    const my1 = this.workFinishGraph
    const my2 = this.machineStateGraph
    const my3 = this.realTimeProductGraph
    window.onresize = function () {
      my1.resize()
      my2.resize()
      my3.resize()
    }
    this.workFinishOption && this.workFinishGraph.setOption(this.workFinishOption)
    this.machineStateOption && this.machineStateGraph.setOption(this.machineStateOption)
    this.realTimeProductOption && this.realTimeProductGraph.setOption(this.realTimeProductOption)
  },
  beforeRouteEnter (to, from, next) {
    next(vm => {
      if (!vm.$store.getters['opcua/uaConnected']) {
        vm.$router.push({ name: 'Small404', params: { error_title: '404错误', error_message: '请先连接OPC UA服务器！'}})
      }
    })
  },
  beforeDestroy() {
    clearInterval(this.int)
  }
}
</script>

<style lang="sass" scoped>
.chart
  width: 100%

.work-finish-chart
  height: 200px

.state-chart
  height: 350px

.real-time-chart
  height: 400px

</style>
