import axios from 'axios'

const WarehouseApi = {
    // Storage Cells
    getStorageCells: function (order, page, warehouse_id, success) {
        axios.get('/api/warehouse/GetStorageCells', {
            params: {
                order, page, warehouse_id
            }
        })
            .then(resp => {
                success(resp.data)
            })
            .catch(e => console.log(e))
    },
    getWarehouseInfo: function (success) {
        axios.get('/api/warehouse/GetWarehouseInfo')
            .then(resp => {
                success(resp.data)
            })
            .catch(e => console.log(e))
    },
    getNumberOfStorageCells: function (warehouse_id, success) {
        axios.get('/api/warehouse/GetNumberOfStorageCells?warehouse_id?'+warehouse_id)
            .then(resp => {
                success(resp.data)
            })
            .catch(e => console.log(e))
    },
    getStorageCellDetail: function (cell_id, success) {
        axios.get('/api/warehouse/GetStorageCellDetail?id=' + cell_id)
            .then(resp => {
                success(resp.data)
            })
            .catch(e => console.log(e))
    },
    // Kanban
    getWarehouseKanbanInfo: function (period, success) {
        axios.get('/api/warehouse/GetWarehouseBasicInfo?period=' + period)
            .then(resp => {
                success(resp.data)
            })
            .catch(e => console.log(e))
    },
    getWarehouseAffairs: function (success) {
        axios.get('api/warehouse/GetWarehouseAffairs')
            .then(resp => {
                success(resp.data)
            })
            .catch(e => console.log(e))
    },
    // Product manager
    submitProduct: function(product, modify, success, fail, error) {
        axios.post("/api/warehouse/SubmitProduct", { product, modify })
            .then(resp => {
                if (resp.data.status === 'success')
                    success(resp.data.product)
                else
                    fail(resp.data.errorMsg)
            })
            .catch(() => {
                error('请求失败！')
            })
    },
    getAllProducts: function(success, fail, error) {
        axios.get('/api/warehouse/GetAllProducts')
            .then(resp => {
                if (resp.data.status === 'success')
                    success(resp.data.products)
                else
                    fail()
            })
            .catch(() => {
                error()
            })
    },
    deleteProduct: function (id, success, fail, error) {
        axios.get("/api/warehouse/DeleteProduct?id="+id)
            .then(resp => {
                if (resp.data.status === 'success')
                    success()
                else
                    fail(resp.data.errorMsg)
            })
            .catch(() => {
                error('请求失败！')
            })
    },
    // Measure plan Management
    submitMeasurePlan: function (measurePlan, success, error) {
        axios.post("/api/warehouse/SubmitMeasurePlan", { measurePlan })
            .then(resp => {
                if (resp.data.status === 'success')
                    success()
                else
                    error(resp.data.errorMsg)
            })
            .catch(() => {
                error('请求失败！')
            })
    },
    getMeasurePlans: function (success, error) {
        axios.get("/api/warehouse/GetMeasurePlans")
            .then(resp => {
                if (resp.data.status === 'success')
                    success(resp.data.measurePlans)
                else
                    error(resp.data.errorMsg)
            })
            .catch(() => {
                error('请求失败!')
            })
    },
    deleteMeasurePlan: function (id, success, error) {
      axios.get('/api/warehouse/DeleteMeasurePlan')
          .then(resp => {
              if (resp.data.status === 'success')
                  success()
              else
                  error(resp.data.errorMsg)
          })
          .catch(() => error('请求失败！'))
    },
    // Control graph
    getControlGraph: function (data, success, fail) {
        axios.post("/api/warehouse/getControlGraph", data)
            .then(resp => {
                if (resp.data.option)
                    success(resp.data.option)
                else if (resp.data.html)
                    success(resp.data.html)
                else
                    fail()
            })
            .catch(err => fail(err))
    }
}

export default WarehouseApi;