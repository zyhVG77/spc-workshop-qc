<template>
  <div :class='["modal", "fade", "bd-example-modal-sm", showing ? "show" : ""]'
       tabindex="-1"
       role="dialog"
       :style='showing ? MODAL_STYLE_WHEN_ACTIVE : MODAL_STYLE_WHEN_HIDE'>
    <div class="modal-dialog modal-sm">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ title }}</h5>
          <button type="button" class="close" @click="close">
            <span>×</span>
          </button>
        </div>
        <div class="modal-body">
          {{ text }}
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="reject">否</button>
          <button type="button" class="btn btn-info" @click="resolve">是</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "v-dialog-modal",
  props: ['title', 'text'],
  data: function () {
    return {
      showing: false,
      MODAL_STYLE_WHEN_HIDE: "display: none",
      MODAL_STYLE_WHEN_ACTIVE: "display: block; padding-right: 16px;",
    }
  },
  methods: {
    reject: function () {
      this.$emit('on-cancel')
      this.showing = false
    },
    resolve: function () {
      this.$emit('on-confirm')
      this.showing = false
    },
    close: function () {
      this.$emit('on-close')
      this.showing = false
    },
    show: function () {
      this.showing = true
    }
  }
}
</script>

<style scoped>

</style>