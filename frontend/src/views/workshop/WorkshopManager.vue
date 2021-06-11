<template>
  <div class="main-container">
    <div class="page-header">
      <!-- Breadcrumb start -->
      <ol class="breadcrumb">
        <li>车间管理</li>
      </ol>
      <!-- Breadcrumb end -->
    </div>
    <div class="row gutters">
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
        <div class="card">
          <div class="card-body">
            <div class="table-responsive">
              <table class="table m-0">
                <thead>
                  <tr>
                    <th>车间号</th>
                    <th>车间名</th>
                    <th>生产零件</th>
                    <th>样本容量</th>
                    <th>观察点数目</th>
                    <th>备注</th>
                    <th>操作</th>
                  </tr>
                </thead>
                <tbody>
                <tr v-for="(workshop, k) in workshops" :key="k">
                  <td>{{ workshop.id }}</td>
                  <td>{{ workshop.name }}</td>
                  <td>{{ getProductName(workshop.productId) }}</td>
                  <td>{{ workshop.batchSize }}</td>
                  <td>{{ workshop.windowSize }}</td>
                  <td>{{ workshop.description }}</td>
                  <td>
                    <div class="btn-group-sm">
                      <button class="btn btn-warning mr-2" @click="modifyWorkshop(k)">修改</button>
                      <button class="btn btn-danger" @click="deleteWorkshop(k)">删除</button>
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

    <!-- Modal Starts -->
    <div :class='["modal", "fade", showModal ? "show" : ""]' tabindex="-1" role="dialog" :style='showModal ? MODAL_STYLE_WHEN_ACTIVE : MODAL_STYLE_WHEN_HIDE'>
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="vCenterModalTitle">修改车间</h5>
            <button type="button" class="close" @click="closeForm">
              <span>×</span>
            </button>
          </div>
          <div class="modal-body">
            <div class="row gutters">
              <div class="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-12">
                <div class="form-group">
                  <label>车间名</label>
                  <input type="text" class="form-control" placeholder="输入车间名" v-model="workshopOnEditing.name">
                </div>
              </div>
              <div class="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-12">
                <div class="form-group">
                  <label>生产零件</label>
                  <select class="form-control" v-model="workshopOnEditing.productId">
                    <option value="">选择零件</option>
                    <option v-for="(product, k) in products"
                            :key="k"
                            :value="product.id">
                      {{ product.name }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-12">
                <div class="form-group">
                  <label>样本容量</label>
                  <input type="text"
                         class="form-control"
                         placeholder="输入样本容量"
                         v-model="workshopOnEditing.batchSize">
                </div>
              </div>
              <div class="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-12">
                <div class="form-group">
                  <label>观察点数目</label>
                  <input type="text" class="form-control" placeholder="输入观察点数目" v-model="workshopOnEditing.windowSize">
                </div>
              </div>
              <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
                <div class="form-group">
                  <label>备注</label>
                  <input type="text" class="form-control" placeholder="输入备注" v-model="workshopOnEditing.description">
                </div>
              </div>
              <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12" v-show="modifying >= 0">
                <h6 style="background-color: lightgrey">注：修改样本容量将导致样本的级联删除！</h6>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeForm">取消</button>
            <button type="button" class="btn btn-primary" @click="resetForm">重置</button>
            <button type="button" class="btn btn-success" @click="saveWorkshop">保存</button>
          </div>
          <div class="row gutters">
            <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
              <HintMessage ref="modal_hint" :is-error="true" :hint-msg="modalHintMsg"></HintMessage>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- Modal Ends -->

    <v-dialog-modal
        title='确认删除'
        text='您真的要删除吗？'
        @on-confirm="confirmDelete"
        ref="dialog">
    </v-dialog-modal>

    <div class="row gutters">
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
        <HintMessage
            :hint-msg="hintMsg.text"
            :is-error="hintMsg.isError"
            ref="hint">
        </HintMessage>
      </div>
    </div>
    <div class="row gutters">
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
        <button class="btn btn-primary btn-lg" @click="addWorkshop">添加新车间</button>
      </div>
    </div>
  </div>
</template>

<script>
import WorkshopApi from "@/api/workshop";
import VDialogModal from "@/components/utils/DialogModal";
import HintMessage from "@/components/utils/HintMessage";

export default {
  name: "WorkshopManager",
  components: {HintMessage, VDialogModal},
  data: function () {
    return {
      workshops: null,
      workshopOnEditing: {
        id: '',
        name: '',
        productId: '',
        batchSize: '',
        windowSize: '',
        description: ''
      },
      hintMsg: {
        isError: false,
        text: ''
      },
      modalHintMsg: '',
      modifying: -1,
      showModal: false,
      deleting: -1,
      MODAL_STYLE_WHEN_HIDE: "display: none",
      MODAL_STYLE_WHEN_ACTIVE: "display: block; padding-right: 16px;",
    }
  },
  computed: {
    products: function () {
      return this.$store.getters['products/allProducts']
    }
  },
  methods: {
    getProductName: function (id) {
      let products = this.$store.getters['products/allProducts']
      for (let i = 0; i < products.length; ++i)
        if (products[i].id === id)
          return products[i].name
    },
    clearForm: function () {
      this.workshopOnEditing = {
        id: '',
        name: '',
        productId: '',
        batchSize: '',
        windowSize: '',
        description: ''
      }
    },
    addWorkshop: function() {
      // Consider 'adding workshop' as a special
      // type of modification
      this.modifying = -1
      this.showModal = true
    },
    modifyWorkshop: function (index) {
      this.modifying = index
      // Deep Copy
      this.workshopOnEditing = JSON.parse(JSON.stringify(this.workshops[index]))
      this.showModal = true
    },
    deleteWorkshop: function (index) {
      this.deleting = index
      // Show warning modal
      this.$refs.dialog.show()
    },
    // Modal related methods here
    resetForm: function () {
      if (this.modifying >= 0)
        this.workshopOnEditing = JSON.parse(JSON.stringify(this.workshops[this.modifying]))
      else
        this.clearForm()
    },
    closeForm: function () {
      this.clearForm()
      this.showModal = false
    },
    saveWorkshop: function () {
      WorkshopApi.submitWorkshop({ workshop: this.workshopOnEditing, modify: this.modifying >= 0 },
          w => {
            if (this.modifying >= 0)
              this.workshops[this.modifying] = w
            else
              this.workshops.push(w)

            this.hintMsg.isError = false
            this.hintMsg.text = (this.modifying >= 0) ? '修改成功！' : '添加成功！'
            this.$refs.hint.show()
            this.showModal = false
            this.clearForm()

            // # Warning! # INTERIM ADDITION
            // REMOVE LATER
            this.$store.dispatch('products/getAllProducts')
          },
          err => {
            this.modalHintMsg = err
            this.$refs.modal_hint.show()
          },
          err => {
            this.modalHintMsg = err
            this.$refs.modal_hint.show()
          })
    },
    confirmDelete: function () {
      WorkshopApi.deleteWorkshop(
          this.workshops[this.deleting].id,
          () => {
            this.workshops.splice(this.deleting, 1)
            this.hintMsg.isError = false
            this.hintMsg.text = '删除成功！'
            this.$refs.hint.show()
          },
          err => {
            this.hintMsg.isError = true
            this.hintMsg.text = err
            this.$refs.hint.show()
          },
          err => {
            this.hintMsg.isError = true
            this.hintMsg.text = err
            this.$refs.hint.show()
          })
    }
  },
  mounted() {
    WorkshopApi.getAllWorkshopsInfo(
        w => this.workshops = w,
        err => {
          console.log(err)
          /*
              Handle Error Messages
           */
        }
    )
  }
}
</script>

<style scoped>

</style>