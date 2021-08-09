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
                             <select class="custom-select" value="default" v-model="myform.userid" @click="findRole()">
                                 <option v-for="(item,k) in useridform" :key="k" >{{item.id}}</option>    	<!--getUserId()  -->
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
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12" v-show="myform.checkrole === 'viewer'" >
          <div class="card" >
              <div class="card-header">
                  <div class="card-title" >选择车间</div>
              </div>
              <div class="card-body">
                  <div class="custom-control custom-checkbox custom-control-inline">
                      <div v-for="(item,k) in myform.relations" :key="k" >
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
import UserApi from '@/api/user';
import WorkshopApi from "@/api/workshop";
export default {
  name: "UserManage.vue",
  data: function() {
      return {
          workshopform:[],
          useridform:[],
          relationshipform:[],
          myform:{
              checkrole:"",
              userid:"",
              mordify:true,
              relations: [
                  // {
                  //     workshopId: "车间一",
                  //     checked: false
                  // },
                  // {
                  //     workshopId: "车间二",
                  //     checked: false
                  // },
                  // {
                  //     workshopId: "车间四",
                  //     checked: false
                  // }
              ]
          }
      }
},
  methods:{
      changeMordifychoose:function(){this.myform.mordify = !this.myform.mordify;this.myform.userid = ""},
      changeMordify:function(){this.myform.mordify = !this.myform.mordify;this.myform.userid = ""},
      selectChange:function(val){
        this.userid = val
        if (this.userid in this.getUserId()){
            this.mordify = false
        }
        else {
          this.mordify = true
        }
      },
      findRole:function(){
        for (var i = 0; i < this.useridform.length; i++){
            if(this.useridform[i]["id"] === this.myform.userid){
                this.myform.checkrole = this.useridform[i]["checkrole"]
            }
            else{
                continue
            }
        }
      },
      getUserId:function(){
          UserApi.getUserId(
          r => this.useridform = r,
          () => {},
          () => {},
      )
      },
      getRelationshipForm:function(){
          WorkshopApi.getRelationshipForm(
          this.myform.userid,
          r => this.relationshipform = r,
          () => {},
          () => {},
          )
      },
      getAllWorkshopsId:function() {
            WorkshopApi.getAllWorkshopsId(
                r => this.workshopform = r,
                () => {},
                () => {},
            )
      },
      getRelations:function (){
          for (var i = 0; i < this.workshopform.length;i++){
              this.relations.push({})
              this.relations[i]["workshopId"] = this.workshopform[i]["id"]
              for (var j = 0; j < this.relationshipform.length;j++) {
                  this.relations[i]["checked"] = false
                  if (this.relationshipform[j]['workshopid'] === this.workshopform[i]["id"]) {
                      this.relations[i]["checked"] = true
                      break
                  }
                  else {
                    continue
                  }
              }
          }
      },
      submitRelatonship:function () {
          UserApi.submitRelatonship(this.myform)
      }

  }
}
</script>

<style scoped>
    .card-header >>> a:hover {
        color: #42b983;
    }
</style>
