<template>
  <div class="main-container">
    <div class="page-header">
      <ol class="breadcrumb">
        <li class="breadcrumb-item">欢迎, {{ currentUser.username }}</li>
      </ol>
      <div class="app-actions">
<!--        <button type="button" :class='periodTime === "today"?TAG_ACTIVE:TAG_SHUT' @click='changePeriod("today")'>今天</button>-->
        <button type="button" :class='periodTime === "7days"?TAG_ACTIVE:TAG_SHUT' @click='changePeriod("7days")'>近7天</button>
        <button type="button" :class='periodTime === "15days"?TAG_ACTIVE:TAG_SHUT' @click='changePeriod("15days")'>近15天</button>
        <button type="button" :class='periodTime === "1month"?TAG_ACTIVE:TAG_SHUT' @click='changePeriod("30days")'>近30天</button>
        <button type="button" :class='periodTime === "1year"?TAG_ACTIVE:TAG_SHUT' @click='changePeriod("1year")'>近1年</button>
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
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
        <div class="card">
          <div class="card-header">
            <div class="card-title">出入库数量变化</div>
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
            <!--
              <li class="product-list clearfix">
                <div class="product-time">
                  <p class="date center-text">11:30 am</p>
                  <span class="badge badge-info">出库</span>
                </div>
                <div class="product-info">
                  <div class="activity">
                    <h6>出库前照灯A303 * 200个 总价20000元</h6>
                    <p>操作员：小李</p>
                  </div>
                </div>
              <li class="product-list clearfix">
                <div class="product-time">
                  <p class="date center-text">12:50 pm</p>
                  <span class="badge badge-success">预警</span>
                </div>
                <div class="product-info">
                  <div class="activity">
                    <h6>损耗警告：储位B3243 齿轮K303损耗超限</h6>
                    <p>报告人：Tambourine</p>
                  </div>
                </div>
              </li>
              -->
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

// E-charts configuration
// import {
//   TitleComponent,
//   ToolboxComponent,
//   TooltipComponent,
//   GridComponent,
//   LegendComponent,
//   MarkLineComponent,
//   VisualMapComponent,
// } from 'echarts/components';
// import {
//   LineChart,
//   HeatmapChart,
// } from 'echarts/charts';
// import {
//   CanvasRenderer
// } from 'echarts/renderers';
//
// echarts.use(
//         [TitleComponent, ToolboxComponent, TooltipComponent, GridComponent, LegendComponent, MarkLineComponent, LineChart, HeatmapChart, VisualMapComponent, CanvasRenderer]
// );

export default {
  name: "KanBan",
  data: function () {
    return {
      TAG_SHUT: ["btn"],
      TAG_ACTIVE: ["btn", "active"],

      basicInfo: {
        storeBatches: 1000,
        storeAmount: 1000,
        deliverBatches: 1000,
        deliverAmount: 1000,
        storeMoney: 1000,
        deliverMoney: 1000
      },
      storeDeliverGraph:null,
      occupationStateGraph:null,
      periodTime: "7days",

      affairs: [
        {
          time: "5/13 11:41pm",
          type: "store",
          detail: "入库前照灯A303 * 200个 总价20000元",
          operator: "操作员：小王"
        },
        {
          time: "5/13 11:41pm",
          type: "deliver",
          detail: "出库前照灯A303 * 200个 总价20000元",
          operator: "操作员：小李"
        },
        {
          time: "5/13 11:41pm",
          type: "store",
          detail: "入库前照灯A303 * 200个 总价20000元",
          operator: "操作员：小王"
        }
      ]
    }
  },
  computed: {
    currentUser: function () {
      // return this.$store.getters['user/currentUser']
      return {
        username: "test"
      }
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
        info.storeDeliverGraphOpiton && this.storeDeliverGraph.setOption(info.storeDeliverGraphOpiton,true)
        info.occupationStateGraphOption && this.occupationStateGraph.setOption(info.occupationStateGraphOption,true)
      })
    }
  },
  mounted() {
    const lineRevenueGraphDom = document.getElementById('lineRevenueGraph')
    this.storeDeliverGraph = echarts.init(lineRevenueGraphDom)
    const my = this.storeDeliverGraph
    const occupationStateGraphDom = document.getElementById('occupationStateGraph')
    this.occupationStateGraph = echarts.init(occupationStateGraphDom)
    const myOccup = this.occupationStateGraph
    window.onresize = function () {
      my.resize()
      myOccup.resize()
    }
    // Fetch basic information about the warehouse
    WarehouseApi.getWarehouseKanbanInfo(this.periodTime, info => {
      this.basicInfo = info.basicInfo;console.log(info.storeDeliverGraphOpiton)
      info.storeDeliverGraphOpiton && this.storeDeliverGraph.setOption(info.storeDeliverGraphOpiton,true)
      info.occupationStateGraphOption && this.occupationStateGraph.setOption(info.occupationStateGraphOption,true)
    })
    // Fetch notifications of the warehouse
    WarehouseApi.getWarehouseAffairs(affairs => this.affairs = affairs)
  }
}
</script>


<style scoped>
.chart {
  width: 100%;
  height: 320px;
}
.chart2 {
  width: 100%;
  height: 350px;
}
</style>