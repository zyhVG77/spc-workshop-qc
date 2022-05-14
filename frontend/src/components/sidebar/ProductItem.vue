<template>
  <li class="dropdown">
    <button type="button"
            class="btn dropdown-toggle"
            @click='$emit("changeCurrentProduct", _key)'>
      {{ product.name }}
      <span class="caret"></span>
    </button>
    <ul :class='["dropdown-menu", currentTag === _key ? "show" : ""]' role="menu">
      <li role="presentation" v-for="(para, pk) in product.parameters" :key="pk">
        <a href="javascript:void(0);" class="current-page" @click="seeControlGraph(pk)">{{ para.name }}</a>
      </li>
    </ul>
  </li>
</template>

<script>
export default {
  name: "Product",
  props: ["product", "currentTag", "_key"],
  methods: {
    seeControlGraph: function (paraIndex) {
      this.$emit('changeCurrentProduct', this.currentTag)   // Close Dropdown Tags
      this.$router.push({path: `/home/controlGraph/${this._key}/${paraIndex}`})
    }
  }
}
</script>

<style scoped>

</style>