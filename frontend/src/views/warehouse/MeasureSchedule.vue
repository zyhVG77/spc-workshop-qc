<template>
  <div class="main-container">
    <div class="page-header">
      <ol class="breadcrumb">
        <li class="breadcrumb-item">
          <a href='javascript: void(0);' @click="changeTag">
            <span :class='[(currentTag === 0) ? "current-tag" : ""]'>添加测量计划</span>
          </a>
        </li>
        <li class="breadcrumb-item">
          <a href='javascript: void(0);' @click="changeTag">
            <span :class='[(currentTag === 1) ? "current-tag" : ""]'>管理测量计划</span>
          </a>
        </li>
      </ol>
    </div>

    <div class="row gutters" v-show="currentTag === 1">
      <hint-message ref="top_hint" :hintMsg="hint.message" :isError="hint.isError"></hint-message>

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
                  <th>仓库</th>
                  <th>储位</th>
                  <th>零件</th>
                  <th>批容量</th>
                  <th>批数</th>
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
                  <td>
                    <div class="btn-group-sm">
                      <button class="btn btn-danger" @click="deleteMeasurePlan(p.id, k)">删除</button>
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
                  <label for="inputGroupSelect06">仓库</label>
                  <select class="custom-select" id="inputGroupSelect06" v-model="measurePlanInfo.warehouseId" @change="loadStorageCells">
                    <option value="default">选择仓库</option>
                    <option v-for='(w, k) in warehouseAvailable' :key='k' :value="w.id">{{ w.name }}</option>
                  </select>
                </div>
                <div class="form-group">
                  <label for="inputGroupSelect06">储位</label>
                  <select class="custom-select" id="inputGroupSelect07" v-model="measurePlanInfo.storageCellId" @change="loadProduct">
                    <option value="default">选择储位</option>
                    <option v-for='(w, k) in storageCells' :key='k' :value="w.id">{{ w.id }}</option>
                  </select>
                </div>
              </div>
            </div>
            <div class="row gutters">
              <div class="col-xl-4 col-lg-4 col-md-6 col-sm-6 col-12">
                <div class="form-group">
                  <label for="inputGroupSelect06">零件名称</label>
                  <select class="custom-select" v-model="measurePlanInfo.productId" @change="loadParameters">
                    <option value="default">选择零件</option>
                    <option v-for='(p, k) in products' :key="k" :value="p.id">{{ p.name }}</option>
                  </select>
                </div>
              </div>
            </div>
            <div class="row gutters">
              <div class="col-xl-4 col-lglg-4 col-md-4 col-sm-4 col-12">
                <div class="form-group">
                  <label for="holder">批容量</label>
                  <input type="text" class="form-control" id="holder" placeholder="输入批容量" v-model="measurePlanInfo.batchSize">
                </div>
              </div>
              <div class="col-xl-4 col-lglg-4 col-md-4 col-sm-4 col-12">
                <div class="form-group">
                  <label for="passer">批数</label>
                  <input type="text" class="form-control" id="passer" placeholder="输入批数" v-model="measurePlanInfo.batch">
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- [Deleted] Pick up measure parameters  -->
      <!--
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12" v-show="parameters.length > 0">
        <div class="card">
          <div class="card-header">
            <div class="card-title">测量属性列表</div>
          </div>
          <div class="card-body">
            <div class="custom-control custom-checkbox" v-for="(p, k) in parameters" :key="k">
              <input type="checkbox" class="custom-control-input" v-model="measurePlanInfo.parameters" :value="p.id" :id='"checkbox_"+k'>
              <label :for='"checkbox_"+k' class="custom-control-label">{{ p.name }}</label>
            </div>
          </div>
        </div>
      </div>
      -->
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
        <div class="card">
          <div class="card-body">
            <div class="form-group">
              <label for="summary">批注</label>
              <textarea class="form-control" id="summary" rows="3" v-model="measurePlanInfo.description"></textarea>
            </div>
          </div>
        </div>
      </div>
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
        <div class="card">
          <div class="card-body">
            <hint-message ref="hint" :hintMsg="hint.message" :isError="hint.isError"></hint-message>
            <button type="submit" class="btn btn-primary mb-2" @click="submitMeasurePlan">提交</button>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import WarehouseApi from "@/api/warehouse"
import HintMessage from "@/components/utils/HintMessage";

export default {
  name: "MeasureSchedule",
  components: { HintMessage },
  data: function () {
    return {
      warehouseAvailable: [],
      products: [],
      // parameters: [],
      storageCells: [],
      measurePlanInfo: {
        batchSize: null,
        batch: null,
        productId: 'default',
        warehouseId: 'default',
        storageCellId: 'default',
        // parameters: [],
        description: ''
      },
      // Hint
      hint: {
        message: "",
        isError: false
      },
      // Operation
      currentTag: 0,
      // Measure plan management
      measurePlans: [],
    }
  },
  methods: {
    // loadParameters: function () {
    //   this.parameters = this.products.find((p) => p.id === this.measurePlanInfo.productId).parameters
    // },
    loadStorageCells: function () {
      WarehouseApi.getStorageCells(2,'all',this.measurePlanInfo.warehouseId,d=>this.storageCells=d)
      // this.storageCells = this.warehouseAvailable.find(w => w.id === this.measurePlanInfo.productId).storageCells
    },
    loadProduct: function () {
      WarehouseApi.getAllProducts(
              products => this.products = products,
              err => console.log(err),
              err => console.log(err)
      )
      // this.products = this.storageCells.find(s => s.id === this.measurePlanInfo.storageCellId).products
    },
    submitMeasurePlan: function () {
      WarehouseApi.submitMeasurePlan(
          this.measurePlanInfo,
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
    deleteMeasurePlan: function (id, index) {
      WarehouseApi.deleteMeasurePlan(id,
          () => {
            this.hint.message = '删除成功！'
            this.hint.isError = false
            this.$refs.top_hint.show()
            // Delete the plan locally
            this.measurePlans.splice(index, 1)
          },
          () => {
            this.hint.message = '删除失败！！'
            this.hint.isError = true
            this.$refs.top_hint.show()
          }
      )
    },
    changeTag: function () {
      if (this.currentTag === 0) {
        this.currentTag = 1
        // Get all measure plans
        WarehouseApi.getMeasurePlans(
            plans => this.measurePlans = plans,
            err => console.log(err)
        )
      }
      else {
        this.currentTag = 0
      }
    }
  },
  mounted() {
    // Fetch all warehouse available for the user
    WarehouseApi.getWarehouseInfo(warehouses => this.warehouseAvailable = warehouses)
    // Fetch products
    // Needless: Products depend on storageCell

    // if (this.$store.getters['warehouse_products/allProducts'].length === 0) {
    //   this.$store.dispatch('warehouse_products/getAllProducts')
    //       .then(products => this.products = products)
    //       .catch(error => console.log(error))
    // } else {
    //   this.products = this.$store.getters['warehouse_products/allProducts']
    // }
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