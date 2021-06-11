<template>
  <div class="main-container">
    <div class="page-header">
      <ol class="breadcrumb">
        <li class="breadcrumb-item">账户设置</li>
      </ol>
    </div>

    <div class="row gutters">
      <div class="col-xl-3 col-lg-3 col-md-12 col-sm-12 col-12">
        <div class="card h-100">
          <div class="card-body">
            <div class="account-settings">
              <UserDetail></UserDetail>
              <div class="about">
                <h5>About</h5>
                <p>用户</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-xl-9 col-lg-9 col-md-12 col-sm-12 col-12">
        <div class="card h-100">
          <AccountForm></AccountForm>
        </div>
      </div>
    </div>
    <!-- Row end -->
  </div>
  <!-- Main container end -->
</template>

<script>
import UserDetail from "@/components/workshop/UserDetail";
import AccountForm from "@/components/workshop/AccountForm";
export default {
name: "AccountSettings",
  components: { AccountForm, UserDetail }
}
</script>

<style scoped>

</style>