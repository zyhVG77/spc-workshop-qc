<template>
  <div class="main-container">
    <div class="page-header">
      <ol class="breadcrumb">
        <li class="breadcrumb-item">欢迎, {{ currentUser.username }}</li>
      </ol>
      <div class="app-actions">
        <!--        <button type="button" :class='periodTime === "today"?TAG_ACTIVE:TAG_SHUT' @click='changePeriod("today")'>今天</button>-->
        <button type="button" :class='periodTime === "7days"?TAG_ACTIVE:TAG_SHUT' @click='changePeriod("7days")'>近7天
        </button>
        <button type="button" :class='periodTime === "15days"?TAG_ACTIVE:TAG_SHUT' @click='changePeriod("15days")'>
          近15天
        </button>
        <button type="button" :class='periodTime === "1month"?TAG_ACTIVE:TAG_SHUT' @click='changePeriod("30days")'>
          近30天
        </button>
        <button type="button" :class='periodTime === "1year"?TAG_ACTIVE:TAG_SHUT' @click='changePeriod("1year")'>近1年
        </button>
      </div>
    </div>
    <div class="row gutters">
      <div class="col-xl-3 col-lg-6 col-md-6 col-sm-6 col-12">
        <div class="info-stats2">
          <div class="info-icon info">
            <i class="icon-download"></i>
          </div>
          <div class="sale-num">
            <h3>{{ basicInfo.storeBatches }}</h3>
            <p>入库批数</p>
          </div>
        </div>
      </div>
      <div class="col-xl-3 col-lg-6 col-md-6 col-sm-6 col-12">
        <div class="info-stats2">
          <div class="info-icon info">
            <i class="icon-download"></i>
          </div>
          <div class="sale-num">
            <h3>{{ basicInfo.storeAmount }}</h3>
            <p>入库量</p>
          </div>
        </div>
      </div>
      <div class="col-xl-3 col-lg-6 col-md-6 col-sm-6 col-12">
        <div class="info-stats2">
          <div class="info-icon success">
            <i class="icon-upload"></i>
          </div>
          <div class="sale-num">
            <h3>{{ basicInfo.deliverBatches }}</h3>
            <p>出库批数</p>
          </div>
        </div>
      </div>
      <div class="col-xl-3 col-lg-6 col-md-6 col-sm-6 col-12">
        <div class="info-stats2">
          <div class="info-icon success">
            <i class="icon-upload"></i>
          </div>
          <div class="sale-num">
            <h3>{{ basicInfo.deliverAmount }}</h3>
            <p>出库量</p>
          </div>
        </div>
      </div>
    </div>
    <div class="row gutters">
      <div class="col-xl-3 col-lg-3 col-md-3 col-sm-3 col-3">
        <div class="card">
          <div class="card-body">
            <div id="todayPutInGraph" class="tiny-pie-chart"></div>
          </div>
        </div>
        <div class="card">
          <div class="card-body">
            <div id="todayShippingGraph" class="tiny-pie-chart"></div>
          </div>
        </div>
      </div>
      <div class="col-xl-9 col-lg-9 col-md-9 col-sm-9 col-9">
        <div class="card">
          <div class="card-header">
            <div class="card-title">出入库月份变化</div>
          </div>
          <div class="card-body">
            <div id="dynamicLineGraph" class="dynamic-chart"></div>
          </div>
        </div>
      </div>
    </div>
    <div class="row gutters">
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
        <div class="card">
          <div class="card-header">
            <div class="card-title">出入库动态</div>
          </div>
          <div class="card-body">
            <div class="row gutters align-items-center">
              <div class="col-xl-10 col-lg-9 col-md-12 col-sm-12 col-12">
                <div id="lineRevenueGraph" class="chart"></div>
              </div>
              <div class="col-xl-2 col-lg-3 col-md-12 col-sm-12 col-12">
                <div class="monthly-avg">
                  <h5>{{ period_for_show }}</h5>
                  <div class="avg-block">
                    <h3 class="avg-total text-info">{{ basicInfo.storeMoney }}</h3>
                    <h6 class="avg-label">入库总金额</h6>
                  </div>
                  <div class="avg-block">
                    <h3 class="avg-total text-success">{{ basicInfo.deliverMoney }}</h3>
                    <h6 class="avg-label">出库总金额</h6>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="row gutters">
      <div class="col-xl-4 col-lg-12 col-md-12 col-sm-12 col-12">
        <div class="card">
          <div class="card-header">
            <div class="card-title">仓库占用情况</div>
          </div>
          <div class="card-body pt-0">
            <div id="occupationStateGraph" class="chart2"></div>
          </div>
        </div>
      </div>
      <div class="col-xl-4 col-lg-12 col-md-12 col-sm-12 col-12">
        <div class="card">
          <div class="card-header">
            <div class="card-title">动态</div>
          </div>
          <div class="card-body">
            <ul class="team-activity">
              <li class="product-list clearfix" v-for="(affair, k) in affairs" :key="k">
                <div class="product-time">
                  <p class="date center-text">{{ affair.time }}</p>
                  <span :class='["badge", affair.type === "store"?"badge-info":"badge-success"]'>
                    {{ affair.type === "store" ? "入库" : "出库" }}
                  </span>
                </div>
                <div class="product-info">
                  <div class="activity">
                    <h6>{{ affair.detail }}</h6>
                    <p>{{ affair.operator }}</p>
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <div class="col-xl-4 col-lg-12 col-md-12 col-sm-12 col-12">
        <div class="card">
          <div class="card-header">
            <div class="card-title">待处理的货物</div>
          </div>
          <div class="card-body pt-0">
            <div id="radialTasks"></div>
            <ul class="task-list-container">
              <li class="task-list-item">
                <div class="task-icon bg-info">
                  <i class="icon-clipboard"></i>
                </div>
                <div class="task-info">
                  <h6 class="task-title">待处理</h6>
                  <p class="amount-spend text-info">12</p>
                </div>
              </li>
              <li class="task-list-item">
                <div class="task-icon bg-success">
                  <i class="icon-clipboard"></i>
                </div>
                <div class="task-info">
                  <h6 class="task-title">已处理</h6>
                  <p class="amount-spend text-success">15</p>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import WarehouseApi from "@/api/warehouse";
import * as echarts from 'echarts';

export default {
  name: "KanBan",
  data: function () {
    return {
      TAG_SHUT: ["btn"],
      TAG_ACTIVE: ["btn", "active"],

      basicInfo: {
        warehouseId: '',
        storeBatches: 0,
        storeAmount: 0,
        deliverBatches: 0,
        deliverAmount: 0,
        storeMoney: 0,
        deliverMoney: 0
      },
      storeDeliverGraph: null,
      occupationStateGraph: null,
      dynamicLineGraph: null,
      todayPutInGraph: null,
      todayShippingGraph: null,

      periodTime: "7days",
      affairs: []
    }
  },
  computed: {
    currentUser: function () {
      return this.$store.getters['user/currentUser']
    },
    period_for_show: function () {
      let dic = {
        "today": "今天",
        "7days": "近7天",
        "15days": "近15天",
        "1month": "近30天",
        "1year": "近1年"
      }
      return dic[this.periodTime]
    }
  },
  methods: {
    changePeriod: function (p) {
      this.periodTime = p
      // Fetch information of the period
      WarehouseApi.getWarehouseKanbanInfo(this.periodTime, info => {
        this.basicInfo = info.basicInfo
        info.storeDeliverGraphOpiton && this.storeDeliverGraph.setOption(info.storeDeliverGraphOpiton, true)
        info.occupationStateGraphOption && this.occupationStateGraph.setOption(info.occupationStateGraphOption, true)
      })
    },
    _dataFormatter(obj) {
      // Generate a sequence of numbers
      let pList = Array.from({length: 31}, (v, i) => i + 1)
      let start = new Date().getMonth()
      let temp;
      for (let i = 0; i < 12; i++) {
        // var max = 0;
        let month = (start + i) % 12 + 1
        let sum = 0
        temp = obj[month]
        for (let j = 0, l = temp.length; j < l; j++) {
          // max = Math.max(max, temp[j]);
          sum += temp[j];
          obj[month][j] = {
            name: pList[j],
            value: temp[j]
          }
        }
        // obj[month + 'max'] = Math.floor(max / 100) * 100;
        obj[month + 'sum'] = sum;
      }
      return obj;
    },
    dataToOptionForDynamic(data) {
      const months = []
      let current_month = new Date().getMonth()
      for (let i = 0; i < 12; i++)
        months.push((current_month + i) % 12 + 1)
      const timelineData = months
      /*
      const timelineData = [
        '2002-01-01',
        {
          value: '2005-01-01',
          tooltip: {
            formatter: '{b} GDP达到一个高度'
          },
          symbol: 'diamond',
          symbolSize: 16
        }
      ]
      */
      const options = []
      const dataMap = {
        putInData: this._dataFormatter(data.putInData),
        shippingData: this._dataFormatter(data.shippingData)
      }
      for (let i = 0; i < 12; ++i) {
        let m = months[i]
        options.push({
          title: {text: (m > current_month ? '去年' : '') + m + '月出入库情况'},
          series: [
            {data: dataMap.putInData[m]},
            {data: dataMap.shippingData[m]},
            {
              data: [
                {name: '入库', value: dataMap.putInData[m+'sum']},
                {name: '出库', value: dataMap.shippingData[m+'sum']},
              ]
            }
          ]
        })
      }

      return {
        baseOption: {
          timeline: {
            axisType: 'category',
            // realtime: false,
            // loop: false,
            autoPlay: true,
            // currentIndex: 2,
            playInterval: 1000,
            // controlStyle: {
            //     position: 'left'
            // },
            data: timelineData,
            label: {
              formatter: function (s) {
                /*
                if (s > current_month)
                  return '去年' + s + '月'
                else
                  return '今年' + s + '月'
                */
                return s + '月'
              }
            }
          },
          title: {
            subtext: '仓库编号' + this.basicInfo.warehouseId
          },
          tooltip: {},
          legend: {
            left: 'right',
            data: ['入库', '出库'],
            selected: {}
          },
          calculable: true,
          grid: {
            top: 80,
            bottom: 100,
            tooltip: {
              trigger: 'axis',
              axisPointer: {
                type: 'shadow',
                label: {
                  show: true,
                  /*
                  formatter: function (params) {
                    return params.value.replace('\n', '');
                  }
                  */
                }
              }
            }
          },
          xAxis: [
            {
              'type': 'category',
              'axisLabel': {'interval': 0},
              'data': Array.from({ length: 31 }, (v, i) => i + 1),
              splitLine: {show: false}
            }
          ],
          yAxis: [
            {
              type: 'value',
              name: '商品数（个）'
            }
          ],
          series: [
            {name: '入库', type: 'bar'},
            {name: '出库', type: 'bar'},
            {
              name: '出入库占比',
              type: 'pie',
              center: ['75%', '35%'],
              radius: '28%',
              z: 100
            }
          ]
        },
        options
      }
    },
    dataToOptionForToday(data, type) {
      let products = []
      let _data = []
      for (let i = 0; i < data.length; ++i) {
        products.push(data[i][0])
        _data.push({
          value: data[i][1],
          name: data[i][0]
        })
      }

      return {
        title: {
          text: '今日' + (type === 0 ? '入库' : '出库') + '产品',
          left: 'center'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        legend: {
          left: 'center',
          top: 'bottom',
          data: products.slice(products.length - Math.min(products.length, 3))
        },
        toolbox: {
          show: true,
          feature: {
            mark: {show: true},
            dataView: {show: true, readOnly: false},
            // restore: {show: true},
            // saveAsImage: {show: true}
          }
        },
        series: [
          {
            name: (type === 0 ? '入库' : '出库') + '情况',
            type: 'pie',
            radius: ['20%', '70%'],
            center: ['50%', '50%'],
            roseType: 'area',
            label: {
              show: false
            },
            itemStyle: {
              borderRadius: 5
            },
            data: _data
          }
        ]
      }
    }
  },
  mounted() {
    const lineRevenueGraphDom = document.getElementById('lineRevenueGraph')
    this.storeDeliverGraph = echarts.init(lineRevenueGraphDom)
    const occupationStateGraphDom = document.getElementById('occupationStateGraph')
    this.occupationStateGraph = echarts.init(occupationStateGraphDom)
    const dynamicLineGraphDom = document.getElementById('dynamicLineGraph')
    this.dynamicLineGraph = echarts.init(dynamicLineGraphDom)
    const todayPutInGraphDom = document.getElementById('todayPutInGraph')
    this.todayPutInGraph = echarts.init(todayPutInGraphDom)
    const todayShippingGraphDom = document.getElementById('todayShippingGraph')
    this.todayShippingGraph = echarts.init(todayShippingGraphDom)

    const my1 = this.storeDeliverGraph
    const my2 = this.occupationStateGraph
    const my3 = this.dynamicLineGraph
    const my4 = this.todayPutInGraph
    const my5 = this.todayShippingGraph

    window.onresize = function () {
      my1.resize()
      my2.resize()
      my3.resize()
      my4.resize()
      my5.resize()
    }
    // Fetch basic information about the warehouse
    WarehouseApi.getWarehouseKanbanInfo(this.periodTime, info => {
      this.basicInfo = info.basicInfo // ;console.log(info.storeDeliverGraphOpiton)
      info.storeDeliverGraphOpiton && this.storeDeliverGraph.setOption(info.storeDeliverGraphOpiton, true)
      info.occupationStateGraphOption && this.occupationStateGraph.setOption(info.occupationStateGraphOption, true)
    })
    // Fetch notifications of the warehouse
    WarehouseApi.getWarehouseAffairs(affairs => this.affairs = affairs)
    // Fetch today's statistics
    // let tmp = [['产品一', 10], ['产品二', 20], ['产品三', 30], ['产品四', 40], ['产品五', 40]]
    WarehouseApi.getTodayStatistics(
        statistics => {
          this.todayPutInGraph.setOption(this.dataToOptionForToday(statistics.putInData, 0))
          this.todayShippingGraph.setOption(this.dataToOptionForToday(statistics.shippingData, 1))
        },
        err => console.log(err))
    // this.todayPutInGraph.setOption(this.dataToOptionForToday(tmp, 0))
    // tmp = [['产品一', 20], ['产品二', 50], ['产品三', 70], ['产品四', 70], ['产品五', 70]]
    // this.todayShippingGraph.setOption(this.dataToOptionForToday(tmp, 1))

    // Fetch dynamic statistics
    /*
    const d = {
      putInData: {},
      shippingData: {}
    }
    const months = []
    let start = new Date().getMonth()
    for (let i = 0; i < 12; i++)
      months.push((start + i) % 12 + 1)
    months.forEach(m => {
      let arr = [], arr1 = []
      for (let i = 0; i < 15; ++i)
        arr.push(Math.round(Math.random() * 5000))
      for (let i = 15; i < 31; ++i)
        arr.push(Math.round(Math.random() * 3000))
      d['putInData'][m] = arr
      for (let i = 0; i < 31; ++i)
        arr1.push(Math.round(Math.random() * 3000))
      d['shippingData'][m] = arr1
    })
    */
    WarehouseApi.getFullYearStatistics(
        statistics => {
          this.dynamicLineGraph.setOption(this.dataToOptionForDynamic(statistics), true)
        },
        err => console.log(err))
    // this.dynamicLineGraph.setOption(this.dataToOptionForDynamic(d), true)
  }
}
</script>


<style lang="sass" scoped>
.chart
  width: 100%
  height: 320px

.chart2
  width: 100%
  height: 350px

.dynamic-chart
  width: 100%
  height: 468px

.tiny-pie-chart
  width: 100%
  height: 230px
</style>