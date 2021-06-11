import axios from 'axios'

const WorkshopApi = {
    // Add or Modify a Product
    submitProduct: function(product, modify, success, fail, error) {
        axios.post("/api/workshop/SubmitProduct", { product, modify })
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
    // Get All Exception Reports
    getAllExceptionReports: function(success, fail, error) {
        axios.get("/api/workshop/GetAllExceptionReports")
            .then(resp => {
                if (resp.data.status === 'success')
                    success(resp.data.reports)
                else
                    fail(resp.data.errorMsg)
            })
            .catch(() => {
                error('请求失败！')
            })
    },
    // Get the report html with a given report id
    getReportDetailHtml: function (id, success, fail, error) {
      axios.get('/api/workshop/GetReportDetailHtml?id='+id)
          .then(resp => {
              if (resp.data.status === 'success')
                  success(resp.data.content)
              else
                  fail(resp.data.errorMsg)
          })
          .catch(() => {
              error('请求失败！')
          })
    },
    // Get All Products for Showing in the Sidebar Menu
    getAllProducts: function(success, fail, error) {
        axios.get('/api/workshop/GetAllProducts')
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
    // Delete One Product
    deleteProduct: function (id, success, fail, error) {
        axios.get("/api/workshop/DeleteProduct?id="+id)
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
    // Get A Control Graph
    getControlGraph: function (data, success) {
        axios.post("/api/workshop/GetControlGraph", data)
            .then(resp => {
                let respData = resp.data
                if (respData.status === 'success' && respData.updated)
                    success(respData.options, respData.tmp_point_id)
            })
            .catch(err => console.log(err))
    },
    // Get analysis report in dynamic control
    getDynamicAnalysisReport: function (data, success, error) {
        axios.post("/api/workshop/GetControlGraph", data)
            .then(resp => {
                let respData = resp.data
                if (respData.status === 'success')
                    success(respData.content)
            })
            .catch(() => error('请求失败！'))
    },
    // Get all workshops' information
    getAllWorkshopsInfo: function (success, error) {
        axios.get("/api/workshop/GetAllWorkshopsInfo")
            .then(resp => {
                if (resp.data.status === 'success')
                    success(resp.data.workshops)
                else
                    error(resp.data.errorMsg)
            })
            .catch(() => error('请求错误！'))
    },
    // Add or modify a workshop
    submitWorkshop: function (workshopForm, success, fail, error) {
        axios.post("/api/workshop/SubmitWorkshop", workshopForm)
            .then(resp => {
                if (resp.data.status === 'success')
                    success(resp.data.workshop)
                else
                    fail(resp.data.errorMsg)
            })
            .catch(() => error('请求失败！'))
    },
    // Delete a workshop
    deleteWorkshop: function (id, success, fail, error) {
        axios.get('/api/workshop/DeleteWorkshop?id='+id)
            .then(resp => {
                if (resp.data.status === 'success')
                    success()
                else
                    fail(resp.data.errorMsg)
            })
            .catch(() => error('请求失败！'))
    },
}

export default WorkshopApi