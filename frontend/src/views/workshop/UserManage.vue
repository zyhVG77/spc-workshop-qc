<template>
    <div class="main-container">
      <div class="page-header">
        <ol class="breadcrumb">
          <li>用户管理</li>
        </ol>
      </div>
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
          <div class="card">
              <div class="card-header">
                <div class="card-title">选择用户</div>
              </div>
              <div class="card-body">
                  <div class="row gutters">
                      <div class="col-xl-4 col-lg col-md-4 col-sm-4 col-12">
                          <div class="form-group">
                             <select class="form-control" v-model="myform.userid">
                               <option value="default" disabled>请选一个用户</option>
                               <option v-for="(item,k) in useridform" :key="k" :value="item.id">{{item.name}}</option>
                               <option :key="-1" :value="-1">新增</option>
                             </select>
                          </div>
                          <!--
                          <div class="form-group" v-show="!myform.modify">
                             <input class="form-control" type="text" v-model="myform.userid">
                          </div>
                          -->
                      </div>

                  </div>
              </div>
          </div>
      </div >
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12" v-show="!myform.modify">
        <div class="card">
          <div class="card-header">
            <div class="card-title">用户名</div>
          </div>
          <div class="card-body">
            <div class="row gutters">
              <div class="col-xl-4 col-lg-4 col-md-4 col-sm-4 col-12">
              <div class="form-group">
                <label for="newName">用户名</label>
                <input type="text" class="form-control" id="newName" placeholder="输入全名" v-model="newUserId">
              </div>
            </div>
              </div>
          </div>
        </div>
      </div>

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
                               <option value="default" disabled>请选择要授予的角色</option>
                               <option value="admin">管理员</option>
                               <!-- 新系统只有两种角色 -->
                               <!-- <option value="super_editor">用户管理员</option> -->
                               <option value="viewer">质检员</option>
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
          newUserId: '',
          myform:{
              checkrole:"default",
              userid:"default",
              modify:true,
              relations: []
          }
      }
  },
  watch: {
    'myform.userid': function () {
      if (!this.myform.userid)
        return

      const _this = this
      function handleSuccess(r) {
        _this.relationshipform = r
        // Update myform
        for (let i = 0; i < _this.useridform.length; i++) {
          if (_this.useridform[i]["id"] === _this.myform.userid) {
            _this.myform.checkrole = _this.useridform[i]["checkrole"]
            break
          }
        }
        // find roles
        _this.myform.relations = []
        for (let i = 0; i < _this.workshopform.length;i++){
          _this.myform.relations.push({
            workshopId: _this.workshopform[i]['id'],
            checked: false
          })
          _this.myform.relations[i]["workshopId"] = _this.workshopform[i]["id"]
          for (var j = 0; j < _this.relationshipform.length;j++) {
            _this.myform.relations[i]["checked"] = false
            if (_this.relationshipform[j]['workshopid'] === _this.workshopform[i]["id"]) {
              _this.myform.relations[i]["checked"] = true
              break
            }
          }
        }
      }

      if (this.myform.userid === -1) {
        this.myform.modify = false
        this.myform.checkrole = 'admin'
        this.myform.relations = []
        this.workshopform.forEach(w => {
          this.myform.relations.push({ workshopId: w.id, checked: false })
        })
      } else {
        this.myform.modify = true
        WorkshopApi.getRelationshipForm(this.myform.userid, handleSuccess, () => {}, () => {})
      }
    }
  },
  methods:{
      submitRelatonship:function () {
          const form = Object.assign({}, this.myform)
          if (!this.myform.modify) {
            form.userid = this.newUserId
          }
          WorkshopApi.submitRelatonship(form, () => {
            this.$toast.success('成功！')

            this.myform = {
              checkrole:"",
              userid:"",
              modify:true,
              relations: []
            }
            this.newUserId = ''
            UserApi.getUserId(r => this.useridform = r, () => {}, () => {})
          }, (err) => {
            this.$toast.error(err)
          })
      }
    },
    mounted() {
      UserApi.getUserId(r => this.useridform = r, () => {}, () => {})
      WorkshopApi.getAllWorkshopsId(r => this.workshopform = r, () => {}, () => {})
    }
}
</script>

<style scoped>
.card-header >>> a:hover {
        color: #42b983;
    }
</style>
