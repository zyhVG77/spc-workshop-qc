<template>
  <div class="main-container">
      <div class="page-header">
          <div class="page-header">
            <h4>出库单</h4>
          </div>
      </div>
      <div class="row gutters">
						<div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
							<div class="card">
								<div class="card-body">
									<div class="row gutters">
										<div class="col-xl-4 col-lg-4 col-md-6 col-sm-6 col-12">
											<div class="form-group">
												<label class="label">出库日期</label>
												<div class="custom-date-input">
													<v-date-picker  v-model="takeOutForm.takeoutDate">
														<template v-slot="{ inputValue, togglePopover }">
															<div class="flex items-center">
																<button  class="icon-calendar" @click="togglePopover()">
																</button>
																<input :value="takeOutForm.takeoutDate" class="bg-white text-gray-700 w-full py-1 px-2 appearance-none border rounded-r focus:outline-none focus:border-blue-500" readonly>
															</div>
														</template>
													</v-date-picker>

													<!--<input type="text" name="" class="form-control datepicker" placeholder="输入入库日期" v-model = "putInForm.inputDate" >-->
												</div>
											</div>
										</div>
									</div>
									<div class="row gutters">
										<div class="col-xl-4 col-lglg-4 col-md-4 col-sm-4 col-12">
											<div class="form-group">
												<label for="seller">供货商</label>
												<input type="text" class="form-control" id="seller" placeholder="输入供货商名称" v-model = "takeOutForm.seller">
											</div>
										</div>
										<div class="col-xl-4 col-lglg-4 col-md-4 col-sm-4 col-12">
											<div class="form-group">
												<label for="qualityChecker">质检员</label>
												<input type="text" class="form-control" id="qualityChecker" placeholder="输入全名" v-model = "takeOutForm.qualityChecker">
											</div>
										</div>
										<div class="col-xl-4 col-lglg-4 col-md-4 col-sm-4 col-12">
											<div class="form-group">
												<label for="holder">保管员</label>
												<input type="text" class="form-control" id="holder" placeholder="输入全名" v-model = "takeOutForm.holder">
											</div>
										</div>
									</div>
									<div class="row gutters">
										<div class="col-xl-4 col-lglg-4 col-md-4 col-sm-4 col-12">
											<div class="form-group">
												<label for="passer">经手人</label>
												<input type="text" class="form-control" id="passer" placeholder="输入全名" v-model = "takeOutForm.passer">
											</div>
										</div>
										<div class="col-xl-4 col-lglg-4 col-md-4 col-sm-4 col-12">
											<div class="form-group">
												<label for="manager">主管</label>
												<input type="text" class="form-control" id="manager" placeholder="输入全名" v-model = "takeOutForm.manager">
											</div>
										</div>
										<div class="col-xl-4 col-lglg-4 col-md-4 col-sm-4 col-12">
											<div class="form-group">
												<label for="accountant">会计</label>
												<input type="text" class="form-control" id="accountant" placeholder="输入全名" v-model = "takeOutForm.accountant">
											</div>
										</div>
									</div>
								</div>
							</div>
						</div>
						<div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12" >
                              <div class="card">
                                <div id="itemList" class="card-body">
                                    <div class="row gutters" v-for="(para, k) in takeOutForm.parameters" :key="k">
                                        <div class="col-xl-1 col-lglg-1 col-md-1 col-sm-1 col-12" >
                                            <div class="form-group">
												<label >编号</label>
												<input type="text" class="form-control" style="text-align: center" :value= "k+1" readonly>
											</div>
										</div>
										<div class="col-xl-2 col-lglg-2 col-md-2 col-sm-2 col-12" >
											<div class="form-group">
												<label for="compName">零件名称</label>
												<select class="custom-select" id="compName" v-model="para.index">
													<option v-for='(w, k) in products' :key='k' :value="w.id">{{ w.name }}</option>
												</select>
											</div>
										</div>
										<div class="col-xl-2 col-lglg-2 col-md-2 col-sm-2 col-12">
											<div class="form-group">
												<label for="model">规格</label>
												<input type="text" class="form-control" id="model" value="I型" v-model = "para.model">
											</div>
										</div>
										<div class="col-xl-1 col-lglg-1 col-md-1 col-sm-1 col-12">
											<div class="form-group">
												<label for="unit">单位</label>
												<input type="text" class="form-control" id="unit" value="个" v-model = "para.unit">
											</div>
										</div>
										<div class="col-xl-1 col-lglg-1 col-md-1 col-sm-1 col-12">
											<div class="form-group">
												<label for="quantity">数量</label>
												<input type="text" class="form-control" id="quantity" value="100" v-model = "para.quantity">
											</div>
										</div>
										<div class="col-xl-1 col-lglg-1 col-md-1 col-sm-1 col-12">
											<div class="form-group">
												<label for="price">单价</label>
												<input type="text" class="form-control" id="price" value="40" v-model = "para.price">
											</div>
										</div>
										<div class="col-xl-1 col-lglg-1 col-md-1 col-sm-1 col-12">
											<div class="form-group">
												<label for="totalPrice">总价</label>
												<input type="text" class="form-control" id="totalPrice" value="4000" v-model = "para.totalPrice">
											</div>
										</div>
										<div class="col-xl-2 col-lglg-2 col-md-2 col-sm-2 col-12">
											<div class="form-group">
												<label for="comment">备注</label>
												<input type="text" class="form-control" id="comment" value="良品率98.70%" v-model = "para.comment">
											</div>
										</div>
										<div class="col-x1-1 col-lg-1 col-md-1 col-sm-1 col-12" v-show="takeOutForm.parameters.length > 1">
											<div>
												<div class="form-group">
													<br>
													<button class="btn btn-danger icon-delete" @click="remove(k)"></button>
												</div>
											</div>
										</div>

									</div>
									<button id="addItem" type="button" class="btn btn-primary" @click = "addItem()">增加一项</button>
								</div>
                            </div>
						</div>
						<div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
							<div class="card">
								<div class="card-body">
									<div class="form-group">
										<label for="summary">批注</label>
										<textarea class="form-control" id="summary" rows="3" v-model="takeOutForm.totalcomment"></textarea>
									</div>
								</div>
							</div>
						</div>
						<div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
							<div class="card">
								<div class="card-body">
									<div class="custom-control custom-switch">
										<input type="checkbox" class="custom-control-input" checked="" id="customSwitch3" @click="distribute()">
										<label class="custom-control-label" for="customSwitch3">自动选择储位</label>
									</div>
									<div class="form-group" v-show="!takeOutForm.autodistribute">
										<input type="text" class="form-control" id="store" placeholder="请手动输入仓库号" v-model = "takeOutForm.storeid">
									</div>
								</div>
							</div>
						</div>

						<div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
							<div class="card">
								<div class="card-body">
										<button type="submit" class="btn btn-primary mb-2" @click = "submitTakeOutForm()">提交</button>
								</div>
							</div>
						</div>
					</div>
  </div>
</template>

<script>
import TakeOutFormApi from "@/api/takeoutform"
import WarehouseApi from "@/api/warehouse";
export default {
	name: "TakeOutForm",
    data: function() {
		return{
			products:[],
			takeOutForm:{
				takeoutDate:new Date(),
				seller:"",
				qualityChecker:"",
				holder:"",
				passer:"",
				manager:"",
				accountant:"",
				totalcomment:"",
				autodistribute:"true",
				storeid:[],
				parameters:[{index:"", model:"", unit:"", quantity:"", price:"", totalPrice:"", comment:"",}]
			},
		}
    },
	methods:{
		getEmptyParameter: () => ({index:"", model:"", unit:"", quantity:"", price:"", totalPrice:"", comment:"",}),
		addItem: function () { this.takeOutForm.parameters.push(this.getEmptyParameter()) },
        remove: function (index) { this.takeOutForm.parameters.splice(index, 1) },
		distribute: function()
        {
            this.takeOutForm.autodistribute = !this.takeOutForm.autodistribute
            this.takeOutForm.storeid = []
        },
        submitTakeOutForm:function () {
			TakeOutFormApi.submitTakeOutForm(this.takeOutForm)
            //this.$http.post("")
        }
	},
	mounted() {
		WarehouseApi.getAllProducts(
				products => this.products = products,
				err => console.log(err),
				err => console.log(err)
		)
	}
}
</script>

<style scoped>
</style>