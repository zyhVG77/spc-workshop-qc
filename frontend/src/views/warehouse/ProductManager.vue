<template>
  <div class="main-container">
    <div class="page-header">
      <!-- Breadcrumb start -->
      <ol class="breadcrumb">
        <li><a href="javascript:void(0);" :class='modificationShown ? "active" : ""'
               @click="showOrHideModification(false)">添加零件</a></li>
        |
        <li><a href="javascript:void(0);" :class='modificationShown ? "" : "active"'
               @click="showOrHideModification(true)">修改零件</a></li>
      </ol>
      <!-- Breadcrumb end -->
    </div>

    <!-- Row start -->
    <div class="row gutters">
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
        <HintMessage ref="deleteHint" :hintMsg="hintMsgDelete.text" :isError="hintMsgDelete.isError"></HintMessage>
        <!-- Modify Product Panel Start -->
        <div class="card" v-show="modificationShown">
          <div class="card-header">
            <div class="card-title">选择零件</div>
          </div>
          <div class="card-body">
            <div class="row gutters">
              <div class="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-12">
                <div class="form-group">
                  <div class="input-group">
                    <select class="custom-select" v-model="modifyData.select" :disabled="modifyData.selected">
                      <option value="default" disabled>选一个零件</option>
                      <option v-for="(product, k) in allProducts"
                              :key="k"
                              :value="k">
                        {{ product.name }}
                      </option>
                    </select>
                    <div class="input-group-append">
                      <button class="btn btn-primary" type="button" @click="loadProduct">{{ modifyData.selected ? "重选" : "确定" }}</button>
                    </div>
                  </div>
                </div>
              </div>
              <div class="col-xl-2 col-lg-2 col-md-2 col-sm-2 col-12">
                <div class="form-group">
                  <div class="input-group">
                    <button class="btn btn-danger" type="button" v-show="modifyData.selected" @click="deleteProduct">
                      删除该零件
                    </button>
                  </div>
                </div>
              </div>
              <div class="col-xl-4 col-lg-4 col-md-4 col-sm-4 col-12">
                <div class="form-group float-right">
                  <div class="input-group">
                    <button class="btn btn-primary" type="button" v-show="modifyData.selected" @click="reloadProduct">
                      重置表单
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- Modify Product Panel End -->
      </div>
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12" v-show="!modificationShown || modifyData.selected">
        <div class="card">
          <div class="card-header">
            <div class="card-title">基本信息</div>
          </div>
          <div class="card-body">
            <div class="row gutters">
              <div class="col-xl-4 col-lg-4 col-md-4 col-sm-4 col-12">
                <div class="form-group">
                  <label for="productName">零件名称</label>
                  <input type="text" class="form-control" id="productName" placeholder="输入零件名称"
                         v-model="productForm.name">
                </div>
              </div>
              <div class="col-xl-4 col-lg-4 col-md-4 col-sm-4 col-12">
                <div class="form-group">
                  <label for="productClass">零件型号</label>
                  <input type="text" class="form-control" id="productClass" placeholder="输入型号"
                         v-model="productForm.type">
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12" v-show="!modificationShown || modifyData.selected">
        <div class="card">
          <div class="card-header">
            <div class="card-title">参数信息</div>
          </div>
          <div class="card-body">
            <div class="row gutters">
              <div class="col-xl-1 col-lg-1 col-md-1 col-sm-1 col-12"><h6 class="text-center">编号</h6></div>
              <div class="col-xl-2 col-lg-2 col-md-2 col-sm-2 col-12"><h6 class="text-center">属性名称</h6></div>
              <div class="col-xl-1 col-lg-1 col-md-1 col-sm-1 col-12"><h6 class="text-center">数值类型</h6></div>
              <div class="col-xl-1 col-lg-1 col-md-1 col-sm-1 col-12"><h6 class="text-center">小数位数</h6></div>
              <div class="col-xl-1 col-lg-1 col-md-1 col-sm-1 col-12"><h6 class="text-center">参数单位</h6></div>
              <div class="col-xl-2 col-lg-2 col-md-2 col-sm-2 col-12"><h6 class="text-center">控制图模型</h6></div>
              <div class="col-xl-1 col-lg-1 col-md-1 col-sm-1 col-12"><h6 class="text-center">上规格限</h6></div>
              <div class="col-xl-1 col-lg-1 col-md-1 col-sm-1 col-12"><h6 class="text-center">下规格限</h6></div>
              <div class="col-xl-1 col-lg-1 col-md-1 col-sm-1 col-12"><h6 class="text-center">备注</h6></div>
            </div>
            <div class="row gutters" v-for="(para, k) in productForm.parameters" :key="k">
              <div class="col-xl-1 col-lg-1 col-md-1 col-sm-1 col-12"><div class="form-group"><input type="text" class="form-control" style="text-align: center" :value="k+1" readonly></div></div>
              <div class="col-xl-2 col-lg-2 col-md-2 col-sm-2 col-12"><div class="form-group"><input type="text" class="form-control" v-model="para.name"></div></div>
              <div class="col-xl-1 col-lg-1 col-md-1 col-sm-1 col-12">
                <div class="form-group">
                  <select class="custom-select" v-model="para.value_type" :disabled="modifyData.selected">
                    <option value="variable_data">计量型</option>
                    <option value="attribute_data">计数型</option>
                  </select>
                </div>
              </div>
              <div class="col-xl-1 col-lg-1 col-md-1 col-sm-1 col-12"><div class="form-group"><input type="number" class="form-control" v-model="para.scale"></div></div>
              <div class="col-xl-1 col-lg-1 col-md-1 col-sm-1 col-12"><div class="form-group"><input type="text" class="form-control" v-model="para.unit"></div></div>
              <div class="col-xl-2 col-lg-2 col-md-2 col-sm-2 col-12">
                <div class="form-group">
                  <select class="custom-select" v-model="para.graph_type">
                    <option value="default" disabled>选择控制图类型</option>
                    <option v-for="(model, k) in getModels(para)" :value="model" :key="k">{{ model }}</option>
                  </select>
                </div>
              </div>
              <div class="col-xl-1 col-lg-1 col-md-1 col-sm-1 col-12"><div class="form-group"><input type="number" class="form-control" v-model="para.usl"></div></div>
              <div class="col-xl-1 col-lg-1 col-md-1 col-sm-1 col-12"><div class="form-group"><input type="number" class="form-control" v-model="para.lsl"></div></div>
              <div class="col-xl-1 col-lg-1 col-md-1 col-sm-1 col-12"><div class="form-group"><input type="text" class="form-control" v-model="para.description"></div></div>
              <div class="col-xl-1 col-lg-1 col-md-1 col-sm-1 col-12" v-show="!modificationShown && productForm.parameters.length > 1">
                <div class="form-group"><button class="btn btn-danger icon-delete" @click="remove(k)"></button></div>
              </div>
            </div>
            <button id="addItem" type="button" class="btn btn-primary" @click="add" v-show="!modificationShown">增加一项</button>
          </div>
        </div>
      </div>
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12" v-show="!modificationShown || modifyData.selected">
        <div class="card">
          <div class="card-body">
            <div class="form-group">
              <label for="summary">批注</label>
              <textarea class="form-control" id="summary" rows="3" v-model="productForm.description"></textarea>
            </div>
          </div>
        </div>
      </div>
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12" v-show="!modificationShown || modifyData.selected">
        <div class="card">
          <div class="card-body">
            <HintMessage ref="resultHint" :isError="hintMsg.isError" :hintMsg="hintMsg.text"></HintMessage>
            <button type="submit" class="btn btn-primary mb-2" @click="submitProduct">提交</button>
          </div>
        </div>
      </div>
    </div>
    <!-- Row end -->
  </div>
</template>

<script>
import HintMessage from "@/components/utils/HintMessage"

export default {
  name: "ProductManager",
  components: { HintMessage },
  data: function () {
    return {
      productForm: {
        name: "",
        type: "",
        description: "",
        parameters: [{name: "", value_type: "variable_data", scale: "", unit: "", graph_type: "default", usl: "", lsl: "", description: ""}],
      },
      hintMsg: {
        isError: false,
        text: ""
      },
      hintMsgDelete: {
        isError: false,
        text: ""
      },
      modificationShown: false,
      modifyData: {
        selected: false,
        select: "default",
      }
    }
  },
  computed: {
    allProducts: function () {
      if (this.$store.getters['warehouse_products/allProducts'].length === 0) {
        this.$store.dispatch('warehouse_products/getAllProducts')
      }
      return this.$store.getters['warehouse_products/allProducts']
    }
  },
  methods: {
    getEmptyParameter: () => ({ name: "", value_type: "variable_data", scale: "", unit: "", graph_type: "default", usl: "", lsl: "", description: ""}),
    clearForm: function (_this) { _this.productForm = { productName: "", productType: "", description: "", parameters: [_this.$options.methods.getEmptyParameter()]}},
    add: function () { this.productForm.parameters.push(this.$options.methods.getEmptyParameter()) },
    remove: function (index) { this.productForm.parameters.splice(index, 1) },
    getModels: function (para) {
      if (para.value_type === 'attribute_data')
        return ['p', 'np', 'u', 'c']
      if (!this.modifyData.selected)
        return ['Xbar-s', 'Xbar-R', 'I-MR']
      if (para.graph_type !== 'IMR')
        return ['Xbar-s', 'Xbar-R']
      return ['I-MR']
    },
    submitProduct: function () {
      this.$store.dispatch(
          'warehouse_products/submitProduct',
          {
            productForm: this.productForm,
            modification: { modify: this.modifyData.selected, index: this.modifyData.select }
          })
          .then(msg => {
            this.hintMsg.isError = false
            this.hintMsg.text = msg
            this.$refs.resultHint.show()
            setTimeout(() => {
              this.$options.methods.clearForm(this)
              this.modifyData.selected = false
            }, 1600)
          })
          .catch(err => {
            this.hintMsg.isError = true
            this.hintMsg.text = err
            this.$refs.resultHint.show()
          })
    },
    showOrHideModification: function (dest) {
      /*
          ### Add product: false
          ### Modify product: true
          Only show or hide the view of modification when
          The 'dest' and 'modificationShown' are different
       */
      if (dest ^ this.modificationShown) {
        this.modificationShown = !this.modificationShown
        // Must Reset the Form
        this.$options.methods.clearForm(this)
        this.modifyData.selected = false
        this.modifyData.select = "default"
      }
    },
    loadProduct: function () {
      if (this.modifyData.selected) {
        this.modifyData.selected = false
        this.$options.methods.clearForm(this)
        return
      }
      if (this.modifyData.select !== "default") {
        // Deep Copy
        this.productForm = JSON.parse(JSON.stringify(this.allProducts[this.modifyData.select]))
        // Adjust value type
        this.productForm.parameters.forEach(para => {
          if (para.value_type === 'UNCOUNTABLE')
            para.value_type = 'variable_data'
          else
            para.value_type = 'attribute_data'
        })
        // Toggle selected state
        this.modifyData.selected = true
      }
    },
    reloadProduct: function () {
      // Deep Copy
      this.productForm = JSON.parse(JSON.stringify(this.allProducts[this.modifyData.select]))
    },
    deleteProduct: function () {
      this.$store.dispatch('warehouse_products/deleteProduct', this.modifyData.select)
          .then(() => {
            this.hintMsgDelete.isError = false
            this.hintMsgDelete.text = "删除成功！"
            this.$refs.deleteHint.show()
            // Reset States
            this.modifyData.selected = false
            this.$options.methods.clearForm(this)
          })
          .catch(err => {
            this.hintMsgDelete.isError = true
            this.hintMsgDelete.text = err
            this.$refs.deleteHint.show()
          })
    }
  }
}
</script>

<style scoped>
a {
  color: #42b983;
}
a.active {
  color: #0b2e13;
}
</style>