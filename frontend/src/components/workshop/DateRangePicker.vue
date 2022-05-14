<template>
  <v-date-picker v-model="range" :model-config="modelConfig" is-range>
    <template v-slot="{ inputValue, inputEvents }">
      <div class="flex justify-center items-center">
        <label>开始日期：</label>
        <input
            :value="inputValue.start"
            v-on="inputEvents.start"
            class="border px-2 py-1 w-25 rounded focus:outline-none focus:border-indigo-300"
        />
        <svg
            class="w-4 h-4 mx-2"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
        >
          <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M14 5l7 7m0 0l-7 7m7-7H3"
          />
        </svg>
        <label>结束日期：</label>
        <input
            :value="inputValue.end"
            v-on="inputEvents.end"
            class="border px-2 py-1 w-25 rounded focus:outline-none focus:border-indigo-300"
        />
        <button type="button" class="btn btn-primary" @click="submitDateRange">确定</button>
        <button type="button" class="btn btn-danger" v-show="!dynamic" @click="toDynamicControl">返回</button>
      </div>
    </template>
  </v-date-picker>
</template>

<script>
export default {
  name: "DateRangePicker",
  props: ['dynamic'],
  data() {
    return {
      range: {
        start: new Date(),
        end: new Date()
      },
      modelConfig: {
        start: {
          type: 'string',
          mask: 'YYYY-MM-DD'
        },
        end: {
          type: 'string',
          mask: 'YYYY-MM-DD'
        },
      }
    };
  },
  watch: {
    range: function (newVal) {
      this.$emit('change', newVal)
    }
  },
  methods: {
    submitDateRange: function () {
      this.$emit('submit-date-range', this.range)
    },
    toDynamicControl: function () {
      this.$emit('to-dynamic-control')
    }
  }
}
</script>

<style scoped>
svg {
  width: 1rem;
  height: 1rem
}
</style>
