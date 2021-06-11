<template>
  <div class="main-container">
    <div class="page-header">
      <div class="page-header">
        <h4>用户管理</h4>
      </div>
    </div>
    <div class="row gutters">
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
        <div class="card">
          <div class="card-body">
            <div class="row gutters">
              <div class="col-xl-4 col-lg-4 col-md-4 col-sm-4 col-12">
                <div class="form-group">
                  <label>选择用户</label>
                  <select value="default" v-model="userid" @change="selectChange">
                    <option v-for="(item,k) in getUserId()" :key="k">{{ item }}</option>
                  </select>
                  <label>选择角色</label>
                  <select class="custom-select" v-model="this.checkrole">
                    <option value="admin">用户管理员</option>
                    <option value="super_editor">厂长</option>
                    <option value="viewer">普通员工</option>
                  </select>
                </div>
              </div>

              <div class="col-xl-4 col-lg-4 col-md-4 col-sm-4 col-12">
                <div class="form-group">
                  <div v-for="(item,k) in getworkshopid()" :key="k" v-show="true">
                    <input type="checkbox" v-model="msg" value="item">{{ item }}
                  </div>
                </div>
                <button @click="submitRelatonship()">
                  提交
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: "UserManage.vue",
  data: function () {
    return {
      msg: this.getrelationshipform(),
      checkrole: "",
      userid: "",
      mordify: "false",
    }
  },
  methods: {
    getworkshopid: function () {
      return ["车间一", "车间二", "车间三"]
    },
    getrelationshipform: function () {
      return ["车间二", "车间三"]
    },
    submitRelatonship: function () {

    },
    selectChange: function (val) {
      this.userid = val
      if (this.userid in this.getUserId()) {
        this.mordify = false
      } else {
        this.mordify = true
      }
    },
    getUserId: function () {

    }
  }
}
</script>

<style scoped>

</style>
