<template>
  <div class="main-container">
    <div class="page-header">
      <ol class="breadcrumb">
        <li class="breadcrumb-item">
          <a href='javascript: void(0);' @click="changeTag">
            <span :class='[(currentTag === 0) ? "current-tag" : ""]'>添加控制计划</span>
          </a>
        </li>
        <li class="breadcrumb-item">
          <a href='javascript: void(0);' @click="changeTag">
            <span :class='[(currentTag === 1) ? "current-tag" : ""]'>管理控制计划</span>
          </a>
        </li>
      </ol>
    </div>

    <div class="row gutters" v-show="currentTag === 1">
      <hint-message ref="top_hint" :hintMsg="hint.message" :isError="hint.isError"></hint-message>

      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
        <div class="card">
          <div class="card-header">
            <div class="title">控制计划列表</div>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table m-0">
                <thead>
                <tr>
                  <th>控制计划编号</th>
                  <th>测量计划编号</th>
                  <th>仓库名</th>
                  <th>零件名</th>
                  <th>批容量</th>
                  <th>批数</th>
                  <th>控制属性</th>
                  <th>操作</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="(p, k) in controlPlans" :key="k">
                  <td>{{ p.id }}</td>
                  <td>{{ p.measurePlanId }}</td>
                  <td>{{ p.warehouseName }}</td>
                  <td>{{ p.productName }}</td>
                  <td>{{ p.batchSize }}</td>
                  <td>{{ p.batch }}</td>
                  <td>{{ p.parameter }}</td>
                  <td>
                    <div class="btn-group-sm">
                      <button class="btn btn-danger" @click="deleteControlPlan(p.id, k)">删除</button>
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

    <div class="row gutters" v-show="currentTag === 0">
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
        <div class="card">
          <div class="card-header">
            <div class="title">基本参数</div>
          </div>
          <div class="card-body">
            <div class="row gutters">
              <div class="col-xl-4 col-lg-4 col-md-6 col-sm-6 col-12">
                <div class="form-group">
                  <label>绑定测量计划</label>
                  <select class="custom-select" v-model='controlPlan.measurePlanId' @change="loadParameters">
                    <option value="default">选择测量计划</option>
                    <option v-for="(m, k) in measurePlans" :key="k" :value="m.id">
                      {{ m.id }}
                    </option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="card">
          <div class="card-header">
            <div class="card-title">控制属性</div>
          </div>
          <div class="card-body">
            <div class="row gutters">
              <div class="col-xl-4 col-lg-4 col-md-6 col-sm-6 col-12">
                <div class="form-group">
                  <label>选择控制属性</label>
                  <select class="custom-select" v-model="controlPlan.parameterId">
                    <option value="default">选择控制属性</option>
                    <option v-for="(p, k) in parameters" :value="p.id" :key="k">{{ p.name }}</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
        <div class="card">
          <div class="card-body">
            <div class="form-group">
              <label for="summary">批注</label>
              <textarea class="form-control" id="summary" rows="3" v-model="controlPlan.description"></textarea>
            </div>
          </div>
        </div>
      </div>
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
        <div class="card">
          <div class="card-body">
            <hint-message ref="hint" :hintMsg="hint.message" :isError="hint.isError"></hint-message>
            <button type="submit" class="btn btn-primary mb-2" @click="submitControlPlan">提交</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import WarehouseApi from "@/api/warehouse";
import HintMessage from "@/components/utils/HintMessage";

export default {
  name: "ControlSchedule",
  components: { HintMessage },
  data: function () {
    return {
      measurePlans: [],
      parameters: [],
      controlPlan: {
        measurePlanId: 'default',
        parameterId: 'default',
        description: ''
      },
      // Hint
      hint: {
        message: "",
        isError: false
      },
      // Operation
      currentTag: 0,
      // Control plan management
      controlPlans: []
    }
  },
  methods: {
    loadParameters: function () {
      return this.measurePlans.find(plan => plan.id = this.controlPlan.measurePlanId).parameters
    },
    submitControlPlan: function () {
      WarehouseApi.submitControlPlan(
          this.controlPlan,
          () => {
            this.hint.message = '保存成功!'
            this.hint.isError = false
            this.$refs.hint.show()
          },
          (error) => {
            this.hint.message = error
            this.hint.isError = true
            this.$refs.hint.show()
          }
      )
    },
    changeTag: function () {
      if (this.currentTag === 0) {
        this.currentTag = 1
        // Get all the measure plans to display
        WarehouseApi.getControlPlans(
            plans => this.controlPlans = plans,
            err => console.log(err)
        )
      } else {
        this.currentTag = 0
      }
    },
    deleteControlPlan: function (id, index) {
      WarehouseApi.deleteControlPlan(id,
          () => {
            this.hint.message = '删除成功！'
            this.hint.isError = false
            this.$refs.top_hint.show()
            // Delete the plan locally
            this.controlPlans.splice(index, 1)
          },
          () => {
            this.hint.message = '删除失败！！'
            this.hint.isError = true
            this.$refs.top_hint.show()
          }
      )
    }
  },
  mounted() {
    WarehouseApi.getMeasurePlans(plans => this.measurePlans = plans)
  }
}
</script>

<style scoped>
a:hover {
  color: #42b983
}

.current-tag {
  color: #42b983
}
</style>