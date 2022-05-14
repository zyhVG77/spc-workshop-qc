<template>
  <div class="main-container">
    <div class="page-header">
      <!-- Breadcrumb start -->
      <ol class="breadcrumb">
        <li>OPC UA</li>
      </ol>
    </div>
    <div class="row gutters">
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
        <div class="card">
          <div class="card-header">
            <div class="card-title">服务器地址</div>
          </div>
          <div class="card-body">
            <div class="form-group">
              <div class="input-group">
                <input type="text" class="form-control" placeholder="输入OPC UA服务器地址" v-model="uaAddress">
                <div class="input-group-append">
                  <button class="btn btn-dark" type="button" @click="testConnection">测试连接</button>
                  <div class="mr-1"></div>
                  <button class="btn btn-primary" type="button" @click="connectUa">确认</button>
                </div>
              </div>
              <small class="form-text text-muted">
                例：opc.tcp://localhost:4840/
              </small>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="row gutters">
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
        <div class="card">
          <div class="card-header">
            <div class="card-title" v-show="showGraph">信息模型</div>
          </div>
          <div class="card-body">
            <div id="modelGraph" class="model-graph"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import WorkshopApi from "@/api/workshop"
import { testConnection } from "@/api/opc-ua-api"
import * as echarts from "echarts"

export default {
  name: "OpcuaManage",
  data: function() {
    return {
      workshops: null,
      uaAddress: '',
      infoModel: null,
      modelGraph: null,

      // operation
      showGraph: false
    }
  },
  methods: {
    testConnection() {
      testConnection(this.uaAddress)
          .then(resp => {
            if (resp.data.ok) {
              this.$toast.success('可接通！')
            }
            else {
              throw Error('不可接通！')
            }
          })
          .catch(err => {
            this.$toast.error(err.message)
          })
    },
    connectUa() {
      this.$store.dispatch('opcua/connectUaServer', this.uaAddress)
          .then(() => {
            this.$toast.success('连接成功！')
            // fetch information model
            this.$store.dispatch('opcua/fetchInfoModel')
                .then(model => {
                  console.log(model)
                  this.showGraph = true
                  this.infoModel = model
                  // Draw graph
                  model && this.modelGraph.setOption(this.generateGraphOption(model))
                })
                .catch(err => console.log(err))
          })
          .catch(err => {
            this.$toast.error(err.message)
          })
    },
    generateGraphOption(modelData) {
      var infoPerWorkshop = []
      this.workshops.forEach(w => {
        var measureMachines = []
        modelData.measure.filter(m => m.measurePlanId === w.id).forEach(m => {
          measureMachines.push({
            name: m.name,
            children: [
              {name: '机器编号', children: [{name: m.operatorId, value: ''}]},
              {name: '属性个数', children: [{name: m.parameterNumber, value: ''}]}
            ]
          })
        })
        var productionMachines = []
        modelData.production.filter(m => m.MeasurePlanId === w.id).forEach(m => {
          productionMachines.push({
            name: m.Name,
            children: [
              {name: '机器编号', children: [{name: m.Id, value: ''}]},
            ]
          })
        })
        infoPerWorkshop.push({
          name: '车间'+parseInt(w.id),
          children: [
            {
              name: '测量机器',
              children: measureMachines
            },
            {
              name: '生产机器',
              children: productionMachines
            }
          ]
        })
      })

      const data = {
        name: '工厂',
        children: infoPerWorkshop
      }
      return {
        tooltip: {
          trigger: 'item',
          triggerOn: 'mousemove'
        },
        series: [
          {
            type: 'tree',
            id: 0,
            name: 'tree1',
            data: [data],
            top: '10%',
            left: '8%',
            bottom: '10%',
            right: '20%',
            symbolSize: 7,
            edgeShape: 'polyline',
            edgeForkPosition: '63%',
            initialTreeDepth: 5,
            lineStyle: {
              width: 2
            },
            label: {
              backgroundColor: '#fff',
              position: 'left',
              verticalAlign: 'middle',
              align: 'right'
            },
            leaves: {
              label: {
                position: 'right',
                verticalAlign: 'middle',
                align: 'left'
              }
            },
            emphasis: {
              focus: 'descendant'
            },
            expandAndCollapse: true,
            animationDuration: 550,
            animationDurationUpdate: 750
          }
        ]
      }
    }
  },
  mounted() {
    WorkshopApi.getAllWorkshopsInfo(
        w => {
          this.workshops = w
        },
        err => console.log(err)
    )
    if (this.$store.getters['opcua/uaConnected']) {
      this.uaAddress = this.$store.getters['opcua/uaAddress']
      this.$store.dispatch('opcua/fetchInfoModel')
          .then(model => {
            this.showGraph = true
            this.infoModel = model
            // Draw graph
            model && this.modelGraph.setOption(this.generateGraphOption(model))
          })
          .catch(err => { console.log(err) })
    }
    const modelGraphDom = document.getElementById('modelGraph')
    this.modelGraph = echarts.init(modelGraphDom)
    const my1 = this.modelGraph

    window.onresize = function () {
      my1.resize()
    }
  }
}
</script>

<style scoped>

.model-graph {
  width: 100%;
  height: 600px;
}

</style>
