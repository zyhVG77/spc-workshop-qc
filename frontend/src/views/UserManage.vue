<template>
    <div class="main-container">
      <div class="page-header">
      <div class="page-header">
        <h4>用户管理</h4>
      </div>
      </div>
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
          <div class="card">
              <div class="card-header">
                  <div class="card-title">
                      <a href="javascript:void(0);" @click = "changeMordifychoose()">选择用户</a> |
                      <a href="javascript:void(0);" @click = "changeMordify()">添加用户</a>
                  </div>
              </div>
              <div class="card-body">
                  <div class="row gutters">
                      <div class="col-xl-4 col-lg col-md-4 col-sm-4 col-12">
                          <div class="form-group" v-show="myform.mordify">
                             <select class="custom-select" value="default" v-model="myform.userid">
                                 <option v-for="(item,k) in getUserId()" :key="k" >{{item.id}}</option>    	<!--getUserId()  -->
                             </select>
                          </div>
                          <div class="form-group" v-show="!myform.mordify">
                             <input  class="form-control" type="text" v-model="myform.userid">
                          </div>
                      </div>
                  </div>
              </div>
          </div>
      </div >
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
          <div class="card">
              <div class="card-header">
                  <div class="card-title">选择角色</div>
              </div>
              <div class="card-body">
                  <div class="row gutters">
                      <div class="col-xl-4 col-lg col-md-4 col-sm-4 col-12">
                          <div class="form-group">
                             <select class="custom-select" v-model="myform.checkrole" >
                                 <option value="admin">用户管理员</option>
                                 <option value="super_editor">厂长</option>
                                 <option value="viewer" onclick="getRelations()">普通员工</option>
                             </select>
                          </div>
                      </div>
                  </div>
              </div>
          </div>
      </div >
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12" >
          <div class="card" >
              <div class="card-header">
                  <div class="card-title" >选择车间</div>
              </div>
              <div class="card-body">
                  <div class="custom-control custom-checkbox custom-control-inline">
                      <div v-for="(item,k) in myform.relations" :key="k" v-show="myform.checkrole === 'viewer'" >
                        <input type="checkbox" class="custom-control-input" :id='"checkbox_"+k' v-model="item.checked" :value = "item.workshopId">
                        <label class="custom-control-label mr-5" :for='"checkbox_"+k'>{{item.workshopId}}</label>
                      </div>
                  </div>
              </div>
          </div>
      </div>
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
          <button class="btn btn-primary" @click="submitRelatonship()">
              提交
          </button>
      </div>
    </div>
</template>

<script>
// import { Message } from 'element-ui';
export default {
  name: "UserManage.vue",
  data: function() {
      return {
          myform:{
              checkrole: "viewer",
              userid:"",
              mordify:"false",
              relations: [
                  {
                      workshopId: "车间一",
                      checked: false
                  },
                  {
                      workshopId: "车间二",
                      checked: false
                  },
                  {
                      workshopId: "车间四",
                      checked: false
                  }
              ]
          }
      }
     // relations:getRelationshipForm()
},
  methods:{
      changeMordifychoose:function(){this.myform.mordify = !this.myform.mordify},
      changeMordifyedit:function(){this.myform.mordify = !this.myform.mordify

                                  },
      selectChange:function(val){
        this.userid = val
        if (this.userid in this.getUserId()){
            this.mordify = false
        }
        else {
          this.mordify = true
        }
      },
      getUserId:function () {
          return [{"id":"哈哈哈","checkrole":"viewer"},{"id":"呵呵呵","checkrole":"super_editor"}]
      },
      getUserIdi:function(success,fail,error){
          this.$http.get('/api/user/getUserId')
              .then(resp => {
                  if (resp.data.status === 'success') {
                      success(resp.data.userid)
                  }
                  else {
                    fail(resp.data.errorMsg)
                  }
              })
              .catch(() => error('请求错误！'))
      },
      getRelationshipForm:function () {
          //this.$http.post("/api/user/getRelationshipForm",{"userid": this.data.userid})
          //.then(resp => {
          return  [{'workshopid':'车间二'},{'workshopid':'车间三'}]
      },
      getAllWorkshopsId:function(success, error,fail) {
          //return [{"id": "车间一"}, {"id": "车间二"}, {"id": "车间三"}]
          this.$http.get("/api/workshop/getAllWorkshopsId")
              .then(resp => {
                  if (resp.data.status === 'success') {
                      success(resp.data.workshopid)
                  }
                  else {
                    fail(resp.data.errorMsg)
                  }
              })
              .catch(() => error('请求错误！'))
      },
      getAllWorkshopsIdi:function() {
          const {data:res} = this.$http.get("/api/workshop/getAllWorkshopsId")
          if (res.status == 'success') {
              return res.workshopid
          }
          else
          {
              // Message.error("获取车间信息失败")
          }

      },
      getRelations:function (){
          var relationshipForm = this.getRelationshipForm().relationshipform
          var workshops = this.getAllWorkshopsId()
          for (var i = 0; i<workshops.length;i++){
              this.relations[i] = {}
              this.relations[i]["workshopId"] = workshops[i]["id"]
              for (var j = 0; j< relationshipForm.length;j++) {
                  this.relations[i]["checked"] = false
                  if (relationshipForm[j]['workshopid'] == workshops[i]["id"]) {
                      this.relations[i]["checked"] = true
                      break
                  }
                  else {
                    continue
                  }
              }
          }
      },
      submitRelatonship:function(){
          const {data:res} = this.$http.post("/api/user/getRelationshipForm",this.myform)
          if(res.status == "success"){
              // Message.success('提交成功')
          }
          else
          {
              // Message.error('提交失败')
          }
      }
  }
}
</script>

<style scoped>
    .card-header >>> a:hover {
        color: #42b983;
    }
</style>
