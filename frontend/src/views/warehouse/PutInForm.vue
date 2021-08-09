<template>
  <div class="main-container">
      <div class="page-header">
          <div class="page-header">
            <h4>入库单</h4>
          </div>
      </div>
      <div class="row gutters">
						<div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
							<div class="card">
								<div class="card-body">
									<div class="row gutters">
										<div class="col-xl-4 col-lg-4 col-md-6 col-sm-6 col-12">
											<div class="form-group">
												<label class="label">入库日期</label>
												<div class="custom-date-input">
													<v-date-picker  v-model="putInForm.inputDate">
														<template v-slot="{ inputValue, togglePopover }">
															<div class="flex items-center">
																<button  class="icon-calendar" @click="togglePopover()">
																</button>
																<input :value="putInForm.inputDate" class="bg-white text-gray-700 w-full py-1 px-2 appearance-none border rounded-r focus:outline-none focus:border-blue-500" readonly>
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
												<input type="text" class="form-control" id="seller" placeholder="输入供货商名称" v-model = "putInForm.seller">
											</div>
										</div>
										<div class="col-xl-4 col-lglg-4 col-md-4 col-sm-4 col-12">
											<div class="form-group">
												<label for="qualityChecker">质检员</label>
												<input type="text" class="form-control" id="qualityChecker" placeholder="输入全名" v-model = "putInForm.qualityChecker">
											</div>
										</div>
										<div class="col-xl-4 col-lglg-4 col-md-4 col-sm-4 col-12">
											<div class="form-group">
												<label for="holder">保管员</label>
												<input type="text" class="form-control" id="holder" placeholder="输入全名" v-model = "putInForm.holder">
											</div>
										</div>
									</div>
									<div class="row gutters">
										<div class="col-xl-4 col-lglg-4 col-md-4 col-sm-4 col-12">
											<div class="form-group">
												<label for="passer">经手人</label>
												<input type="text" class="form-control" id="passer" placeholder="输入全名" v-model = "putInForm.passer">
											</div>
										</div>
										<div class="col-xl-4 col-lglg-4 col-md-4 col-sm-4 col-12">
											<div class="form-group">
												<label for="manager">主管</label>
												<input type="text" class="form-control" id="manager" placeholder="输入全名" v-model = "putInForm.manager">
											</div>
										</div>
										<div class="col-xl-4 col-lglg-4 col-md-4 col-sm-4 col-12">
											<div class="form-group">
												<label for="accountant">会计</label>
												<input type="text" class="form-control" id="accountant" placeholder="输入全名" v-model = "putInForm.accountant">
											</div>
										</div>
									</div>
								</div>
							</div>
						</div>
						<div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12" >
                              <div class="card">
                                <div id="itemList" class="card-body">
                                    <div class="row gutters" v-for="(para, k) in putInForm.parameters" :key="k">
                                        <div class="col-xl-1 col-lglg-1 col-md-1 col-sm-1 col-12" >
                                            <div class="form-group">
												<label >编号</label>
												<input type="text" class="form-control" style="text-align: center" :value= "k+1" readonly>
											</div>
										</div>
										<div class="col-xl-2 col-lglg-2 col-md-2 col-sm-2 col-12" >
											<div class="form-group">
												<label for="compName">零件名称</label>
												<input type="text" class="form-control" id="compName" value="齿轮H300" v-model = "para.compName">
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
										<div class="col-x1-1 col-lg-1 col-md-1 col-sm-1 col-12" v-show="putInForm.parameters.length > 1">
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
										<textarea class="form-control" id="summary" rows="3" v-model="putInForm.totalcomment"></textarea>
									</div>
								</div>
							</div>
						</div>
						<div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
							<div class="card">
								<div class="card-body">
									<div class="custom-control custom-switch">
										<input type="checkbox" class="custom-control-input" checked="" id="customSwitch3" @click="distribute()">
										<label class="custom-control-label" for="customSwitch3">自动分配储位</label>
									</div>
									<div class="form-group" v-show="!putInForm.autodistribute">
										<input type="text" class="form-control" id="store" placeholder="请手动输入仓库号" v-model = "putInForm.storeid">
									</div>
								</div>
							</div>
						</div>

						<div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
							<div class="card">
								<div class="card-body">
										<button type="submit" class="btn btn-primary mb-2" @click = "submitPutInForm()">提交</button>
								</div>
							</div>
						</div>
					</div>
  </div>
</template>

<script>
import PutInFormApi from "@/api/putinform"
export default {
	name: "PutInForm",
    data: function() {
		return{
			putInForm:{
				inputDate:new Date(),
				seller:"",
				qualityChecker:"",
				holder:"",
				passer:"",
				manager:"",
				accountant:"",
				totalcomment:"",
				autodistribute:"true",
				storeid:[],
				parameters:[{compName:"", model:"", unit:"", quantity:"", price:"", totalPrice:"", comment:"",}]
			},
		}
    },
	methods:{
		getEmptyParameter: () => ({compName:"", model:"", unit:"", quantity:"", price:"", totalPrice:"", comment:"",}),
		addItem: function () { this.putInForm.parameters.push(this.getEmptyParameter()) },
        remove: function (index) { this.putInForm.parameters.splice(index, 1) },
		distribute: function()
        {
            this.putInForm.autodistribute = !this.putInForm.autodistribute
            this.putInForm.storeid = []
        },
        submitPutInForm:function () {
			PutInFormApi.submitPutInForm(this.putInForm)
            //this.$http.post("")
        }
	}

}
</script>

<style scoped>
</style>