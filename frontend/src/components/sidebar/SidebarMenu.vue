<template>
  <div class="sidebar-content sidebar-menu">
    <ul>
      <li :class='["sidebar-dropdown", currentActiveTag === "controlGraph" ? "active" : ""]'
          v-show="currentSubSys === 'workshop'">
        <a href="javascript:void(0);" @click="closeOrOpenProductTag">
          <i class="icon-home2"></i>
          <span class="menu-text">零件</span>
        </a>
        <div class="sidebar-submenu">
          <ul>
            <ProductItem v-for="(product, k) in products"
                     :product="product"
                     :key="k"
                     :currentTag="currentProductTag"
                     :_key="k"
                     @changeCurrentProduct="changeCurrentProduct($event)">
            </ProductItem>
          </ul>
        </div>
      </li>

      <li :class='currentActiveTag === item.id ? "active" : ""' v-for="(item, k) in menuItems" :key="k">
        <router-link :to="item.path">
          <i :class="item.iconClass"></i>
          <span class="menu-text">{{ item.name }}</span>
        </router-link>
      </li>

      <li v-show='this.$store.getters["user/currentUser"].role === "admin"'>
        <a href="javascript: void(0);" @click="changeSubSystem">
          <i class="icon-corner-down-right"></i>
          <span class="menu-text">
            进入{{ currentSubSys==='workshop'?"仓储":"车间"}}管理
          </span>
        </a>
      </li>

    </ul>
  </div>
</template>

<script>
import ProductItem from "@/components/sidebar/ProductItem";

export default {
  name: "SidebarMenu",
  components: { ProductItem },
  data: function () {
    return {
      currentActiveTag: "NULL",
      currentProductTag: -1,
    }
  },
  computed: {
    products: function () {
      return this.$store.getters['products/allProducts']
    },
    currentSubSys: function () {
      return this.$store.getters['subsystem_state/current_sub_sys']
    },
    menuItems: function () {
      let menuItems = []
      this.$store.getters['permission/routes'].forEach(route => {
        let path = route.path
        if (route.children) {
          route.children.forEach(child => {
            let nPath = path + '/' + child.path
            if (child.meta && child.meta.isSidebarItem) {
              // If current subsystem is workshop
              // then do not show the sidebar items of warehouse subsystem
              if (child.meta.subsystem
                  && this.$store.getters['subsystem_state/current_sub_sys']!==child.meta.subsystem) {
                // Go to next loop
                return;
              }

              let pattern = /\/home\/(.+?)\//

              pattern.exec(nPath + '/')
              let id = RegExp.$1
              menuItems.push({
                path: nPath,
                name: child.meta.sidebarInfo.name,
                iconClass: child.meta.sidebarInfo.iconClass,
                id
              })
            }
          })
        }
      })
      return menuItems
    }
  },
  watch: {
    '$route': 'activateTag'
  },
  methods: {
    closeOrOpenProductTag: function () {
      this.currentActiveTag = (this.currentActiveTag === "controlGraph") ? "NULL" : "controlGraph"
      this.currentProductTag = -1
    },
    changeCurrentProduct: function (nTag) {
      if (nTag === this.currentProductTag)
        this.currentProductTag = -1
      else
        this.currentProductTag = nTag
    },
    activateTag: function () {
      let pattern = /\/home\/(.+?)\//

      pattern.exec(this.$route.path + '/')
      this.currentActiveTag = RegExp.$1
      console.log(this.currentActiveTag)
    },
    changeSubSystem: function () {
      this.$store.dispatch("subsystem_state/changeSubSys")
          .then(to => {
            if (to === 'workshop')
              this.$router.push('/home/controlGraph/0/0')
            else
              this.$router.push('/home/kanban')
          })
          .catch(() => {})
      // Refresh router-view
      // this.$router.push('/home')
    }
  },
  mounted() {
    // If current subsystem is workshop
    // Gotta fetch all the products first
    if (this.$store.getters['subsystem_state/current_sub_sys'] === 'workshop') {
      this.$store.dispatch('products/getAllProducts')
          .then(products => {
            if (products.length > 0 && products[0].parameters.length > 0) {
              this.$router.push('/home/controlGraph/0/0')
            }
          })
    }
  }
}
</script>

<style scoped>

</style>