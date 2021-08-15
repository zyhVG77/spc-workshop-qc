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
                      <div class="card-title">选择用户</div>
                      <!--todo:添加用户的具体逻辑是什么，添加的是用户名还是用户id，新用户如何选择车间-->
<!--                      <a href="javascript:void(0);" @click = "changeMordifychoose()">选择用户</a> |-->
<!--                      <a href="javascript:void(0);" @click = "changeMordify()">添加用户</a>-->
                  </div>
              </div>
              <div class="card-body">
                  <div class="row gutters">
                      <div class="col-xl-4 col-lg col-md-4 col-sm-4 col-12">
                          <div class="form-group" v-show="myform.modify">
                             <select class="custom-select" value="default" v-model="myform.userid" @click="findRole()">
                                 <option v-for="(item,k) in useridform" :key="k" :value="item.id">{{item.name}}</option>    	<!--fixme: 显示用户名较为合理，同时设置:value为用户id-->
                             </select>
                          </div>
                          <div class="form-group" v-show="!myform.modify">
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
                                 <option value="viewer">普通员工</option> <!--fixme: 这里使用click是不会触发的 -->
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
              modify:true, // fixme: mordify -> modify
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
      changeMordifychoose:function(){this.myform.modify = !this.myform.modify;this.myform.userid = ""},
      changeMordify:function(){this.myform.modify = !this.myform.modify;this.myform.userid = ""},
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
        console.log("OK2")
        for (var i = 0; i < this.useridform.length; i++){
            if(this.useridform[i]["id"] === this.myform.userid){
                this.myform.checkrole = this.useridform[i]["checkrole"]
            }
        }

        if(this.myform.checkrole === 'viewer') this.getRelations() // fixme: 判断是否是viewer，更新relations信息
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
          console.log("OK")
          this.myform.relations = [] //fixme: 将列表初始化为空
          for (var i = 0; i < this.workshopform.length;i++){
              this.myform.relations.push({}) //fixme: this.relations -> this.myform.relations
              this.myform.relations[i]["workshopId"] = this.workshopform[i]["id"]
              for (var j = 0; j < this.relationshipform.length;j++) {
                  this.myform.relations[i]["checked"] = false
                  if (this.relationshipform[j]['workshopid'] === this.workshopform[i]["id"]) {
                      this.myform.relations[i]["checked"] = true
                      break
                  }
              }
          }
      },
      // todo: 有时候未选中的workshop中没有‘checked’键，会导致提交失败
      submitRelatonship:function () {
          WorkshopApi.submitRelatonship(this.myform) // fixme: 我把这个API移到了workshop中
      }
    },
    mounted() { // fixme: 挂载组件之后应当调用GetUserId，否则useridform是空的，无法选择用户；workshop同理
        this.getUserId()
        this.getAllWorkshopsId()
    }
}
</script>

<style scoped>
    .card-header >>> a:hover {
        color: #42b983;
    }
</style>
