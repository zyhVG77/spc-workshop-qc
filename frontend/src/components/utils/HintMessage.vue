<template>
  <div :class='["alert", isError ? "alert-danger" : "alert-success"]' v-show="showHint">{{ hintMsg }}</div>
</template>

<script>
export default {
  name: "HintMessage",
  data: function () {
    return {
      showHint: false,
      showTime: 1500
    }
  },
  props: ["isError", "hintMsg"],
  methods: {
    show: function () {
      const _this = this;
      _this.showHint = true;
      setTimeout(function () {
        _this.showHint = false;
      }, _this.showTime);
    }
  }
}
</script>

<style scoped>

</style>