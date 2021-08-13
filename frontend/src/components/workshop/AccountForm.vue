<template>
  <div class="card-body">
    <div class="row gutters">
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
        <h6 class="mb-2 text-primary">个人信息</h6>
      </div>
      <div class="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-12">
        <div class="form-group">
          <label for="fullName">全名</label>
          <input type="text" class="form-control" id="fullName" placeholder="输入全名" v-model="userOnSetting.fullname">
        </div>
      </div>
      <div class="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-12">
        <div class="form-group">
          <label for="eMail">Email</label>
          <input type="email" class="form-control" id="eMail" placeholder="输入电子邮件" v-model="userOnSetting.email">
        </div>
      </div>
      <div class="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-12">
        <div class="form-group">
          <label for="phone">电话</label>
          <input type="text" class="form-control" id="phone" placeholder="输入电话号码" v-model="userOnSetting.phone">
        </div>
      </div>
      <div class="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-12">
        <div class="form-group">
          <label for="website">工号</label>
          <input type="url" class="form-control" id="website" placeholder="输入工号" v-model="userOnSetting.workId">
        </div>
      </div>
    </div>
    <div class="row gutters">
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
        <div class="text-right">
          <button type="button" id="reset" name="submit" class="btn btn-secondary" @click="reset">还原</button>&nbsp;
          <button type="button" id="update" name="submit" class="btn btn-primary" @click="update">更新</button>
        </div>
      </div>
    </div>
    <div class="row gutters">
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
        <h6 class="mt-3 mb-2 text-primary">修改密码</h6>
      </div>
      <div class="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-12">
        <div class="form-group">
          <label>原密码</label>
          <input type="password" class="form-control" v-model="rawPwd">
        </div>
      </div>
      <div class="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-12">
        <div class="form-group">
          <label>新密码</label>
          <input type="password" class="form-control" v-model="newPwd">
        </div>
      </div>
    </div>
    <div class="row gutters">
      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
        <div class="text-right">
          <button type="button" name="submit" class="btn btn-primary" @click="modifyPwd">提交</button>
        </div>
      </div>
    </div>
    <HintMessage ref="hint" :isError="hintMsg.isError" :hintMsg="hintMsg.text"></HintMessage>
  </div>
</template>

<script>
import HintMessage from "@/components/utils/HintMessage";
import bcrypt from "bcryptjs"

export default {
  name: "AccountForm",
  components: { HintMessage },
  data: function () {
    return {
      // Deep Copy User Object
      userOnSetting: JSON.parse(JSON.stringify(this.$store.getters['user/currentUser'])),
      hintMsg: {
        isError: false,
        text: ""
      },
      rawPwd: "",
      newPwd: ""
    }
  },
  computed: {
    user: function () {
      return this.$store.getters['user/currentUser']
    }
  },
  methods: {
    reset: function () {
      this.userOnSetting = JSON.parse(JSON.stringify(this.user))
    },
    update: function () {
      this.$store.dispatch('user/updateUserInfo', this.userOnSetting)
          .then(() => {
            /*
                Now the user's information is updated,
                it's needed to reset the 'userOnSetting'
             */
            this.userOnSetting = JSON.parse(JSON.stringify(this.user))
            this.hintMsg.isError = false
            this.hintMsg.text = '修改成功！'
            this.$refs.hint.show()
          })
          .catch(err => {
            this.hintMsg.isError = true
            this.hintMsg.text = err
            this.$refs.hint.show()
          })
    },
    modifyPwd: function () {
      /*
          Validate Here !
       */

      // Encrypt Password with Bcrypt
      const salt = bcrypt.genSaltSync(10);
      const rawPwdHash = this.rawPwd //bcrypt.hashSync(this.rawPwd, salt);
      const newPwdHash = bcrypt.hashSync(this.newPwd, salt);
      this.$store.dispatch('user/modifyPwd', { rawPwdHash, newPwdHash })
          .then(() => {
            /*
                If the Password is Modified Successfully,
                the user will be forced to login again
             */
            this.$store.dispatch('user/logout')
            this.$router.push('/Login')
          })
          .catch(err => {
            this.hintMsg.isError = true
            this.hintMsg.text = err
            this.$refs.error.show()
          })
    }
  }
}
</script>

<style scoped>

</style>