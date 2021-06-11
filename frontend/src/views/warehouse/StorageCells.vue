<template>
  <div class="main-container">
    <div class="page-header">
      <ol class="breadcrumb">
        <li class="breadcrumb-item">储位状态图</li>
      </ol>
    </div>
    <div class="row gutters">
      <div class="col-xl-12 col-lg-12 col-sm-12 col-md-12">
        <div class="card">
          <div class="card-body">
            <label class="mr-2">排序方式：</label>
            <div class="custom-control custom-radio custom-control-inline">
              <input type="radio" id="defaultOrder" name="displayOrder" class="custom-control-input" checked
                     @change="changeOrder(0)">
              <label class="custom-control-label" for="defaultOrder">默认排序</label>
            </div>
            <div class="custom-control custom-radio custom-control-inline" @change="changeOrder(1)">
              <input type="radio" id="freeFirst" name="displayOrder" class="custom-control-input">
              <label class="custom-control-label" for="freeFirst">空闲数量从大到小</label>
            </div>
            <div class="custom-control custom-radio custom-control-inline">
              <input type="radio" id="occupyFirst" name="displayOrder" class="custom-control-input"
                     @change="changeOrder(2)">
              <label class="custom-control-label" for="occupyFirst">空闲数量从小到大</label>
            </div>
            <div class="m-3"></div>
            <div class="form-inline">
              <label class="my-1 mr-2">当前仓库</label>
              <select class="form-control form-control-sm col-2" v-model="current_warehouse_id">
                <option value="all">全部</option>
                <option v-for="(wh, k) in warehouses" :key="k" :value="wh.id">
                  {{ wh.name }}
                </option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="row gutters">
      <div class="col-xl-12 col-lg-12 col-sm-12 col-md-12">
        <div class="card">
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-bordered table-dark m-0">
                <tbody>
                <tr v-for="row in Math.ceil(storage_cells.length/10)" :key="row">
                  <td
                      v-for="col in (row*10<storage_cells.length)?10:(storage_cells.length-(row-1)*10)"
                      :key="col"
                      :bgcolor="getColor(storage_cells[(row-1)*10+(col-1)])"
                      @click="seeCellDetail(storage_cells[(row-1)*10+(col-1)].id)">
                    {{ storage_cells[(row - 1) * 10 + (col - 1)].id }}
                  </td>
                </tr>
                </tbody>
              </table>
            </div>
            <div class="m-4"></div>
            <nav aria-label="Page navigation example">
              <ul class="pagination justify-content-center info">
                <li :class='["page-item", current_page===1?"disabled":""]'>
                  <a class="page-link" href="javascript: void(0);" @click="changePage(current_page-1)">
                    <i class="icon-chevron-left1"></i> 上页
                  </a>
                </li>
                <li :class='["page-item", current_page===p?"active":""]' v-for="p in total_pages" :key="p">
                  <a class="page-link" href="javascript: void(0);" @click="changePage(p)">
                    {{ p }}
                  </a>
                </li>
                <li :class='["page-item", current_page===total_pages?"disabled":""]'>
                  <a class="page-link" href="javascript: void(0);" @click="changePage(current_page+1)">
                    下页 <i class="icon-chevron-right1"></i>
                  </a>
                </li>
              </ul>
            </nav>

            <!-- Modal for the detail information of a cell -->
            <div :class='["modal", "fade", "bd-example-modal-lg", detail_show?"show":""]' tabindex="-1" role="dialog"
                 :style="detail_show?MODAL_STYLE_WHEN_ACTIVE:MODAL_STYLE_WHEN_HIDE">
              <div class="modal-dialog modal-lg" role="document">
                <div class="modal-content">
                  <div class="modal-header">
                    <h5 class="modal-title">储位详情</h5>
                    <button type="button" class="close" @click="closeDetail">
                      <span>×</span>
                    </button>
                  </div>
                  <div class="modal-body">
                    <h6>储位编号：{{ cell_detail.id }} | 仓库编号：{{ cell_detail.warehouse_id }}</h6>
                    <h6>容量：{{ cell_detail.capacity }} | 占用：{{ cell_detail.occupy }} | 余量： {{ cell_detail.capacity - cell_detail.occupy }}</h6>
                    <div class="m-2"></div>
                    <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
                      <div class="card">
                        <div class="card-body">
                          <div class="table-responsive">
                            <table class="table m-0">
                              <thead>
                              <tr>
                                <th>产品编号</th>
                                <th>产品名称</th>
                                <th>产品数量</th>
                                <th>存储开始时间</th>
                              </tr>
                              </thead>
                              <tbody>
                              <tr v-for="(p, k) in cell_detail.products" :key="k">
                                <td>{{ p.id }}</td>
                                <td>{{ p.name }}</td>
                                <td>{{ p.quantity }}</td>
                                <td>{{ p.start_time }}</td>
                              </tr>
                              </tbody>
                            </table>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="modal-footer">
                    <button type="button" class="btn btn-primary" @click="closeDetail">关闭</button>
                  </div>
                </div>
              </div>
            </div>
            <!-- End of Modal-->

          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import {generateColor} from '@/assets/js/color_gradient'
import WarehouseApi from "@/api/warehouse";

export default {
  name: "StorageCells",
  data: function () {
    return {
      warehouses: [],
      storage_cells: [],
      current_warehouse_id: 'all',
      order: 0,
      current_page: 1,
      total_pages: 1,

      // For a specific cell detail
      detail_show: false,
      MODAL_STYLE_WHEN_HIDE: "display: none",
      MODAL_STYLE_WHEN_ACTIVE: "display: block; padding-right: 16px;",
      cell_detail: {
        id: '',
        warehouse_id: '',
        capacity: 0,
        occupy: 0,
        products: [
          {
            id: "PID00001",
            name: "产品一",
            quantity: 100,
            start_time: "2021年1月1日"
          }
        ]
      }
    }
  },
  computed: {
    colorGradients: function () {
      return generateColor("#DB2F23", "#3BD64E", 100)
    }
  },
  watch: {
    // In case of changing warehouse
    current_warehouse_id: function () {
      WarehouseApi.getStorageCells(
          this.order,
          0,
          this.current_warehouse_id,
          cells => this.storage_cells = cells
      )
      // Update number of cells
      WarehouseApi.getNumberOfStorageCells(this.current_warehouse_id)
    }
  },
  methods: {
    getColor: function (cell) {
      let rate = Math.floor(cell.occupy * 100 / cell.capacity)
      return this.colorGradients[rate >= 1 ? rate - 1 : 0]
    },
    changeOrder: function (order) {
      WarehouseApi.getStorageCells(
          order,
          0,
          '',
          cells => {
            this.storage_cells = cells
            this.order = order
          })
    },
    changePage(p) {
      WarehouseApi.getStorageCells(
          this.order,
          p,
          this.current_warehouse_id,
          cells => {
            this.storage_cells = cells
            this.current_page = p
          })
    },
    seeCellDetail: function (cell_id) {
      WarehouseApi.getStorageCellDetail(cell_id, cell_detail => {
        this.cell_detail = cell_detail
        this.detail_show = true
      })
    },
    closeDetail: function () {
      this.detail_show = false
    }
  },
  mounted() {
    // Get all warehouse info
    WarehouseApi.getWarehouseInfo(warehouses => this.warehouses = warehouses)
    // Get default storage cells
    WarehouseApi.getStorageCells(
        0,
        0,
        'all',
        cells => this.storage_cells = cells
    )
    // Get the number of storage cells
    WarehouseApi.getNumberOfStorageCells('all', n => {
      this.total_pages = Math.ceil(n / 100)
    })
  }
}
</script>

<style scoped>
td:hover {
  box-shadow: 0 0 21px 5px rgba(33,33,33,.2);
  cursor: pointer;
}
</style>