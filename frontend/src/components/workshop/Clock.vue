<template>
  <div id="clock">
    <div class="date">{{ date }}</div>
    <div class="time">{{ time }}</div>
  </div>
</template>

<script>
export default {
  name: "Clock",
  data: function () {
    return {
      time: '',
      date: ''
    }
  },
  mounted() {
    function zeroPadding(num, digit) {
      var zero = '';
      for(var i = 0; i < digit; i++) {
        zero += '0';
      }
      return (zero + num).slice(-digit);
    }

    var week = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'];
    // var timerID = setInterval(updateTime, 1000);
    setInterval(() => {
      var cd = new Date();
      this.time = zeroPadding(cd.getHours(), 2) + ':' + zeroPadding(cd.getMinutes(), 2) + ':' + zeroPadding(cd.getSeconds(), 2);
      this.date = zeroPadding(cd.getFullYear(), 4) + '-' + zeroPadding(cd.getMonth() + 1, 2) + '-' + zeroPadding(cd.getDate(), 2) + ' ' + week[cd.getDay()];
    }, 1000);

    var cd = new Date();
    this.time = zeroPadding(cd.getHours(), 2) + ':' + zeroPadding(cd.getMinutes(), 2) + ':' + zeroPadding(cd.getSeconds(), 2);
    this.date = zeroPadding(cd.getFullYear(), 4) + '-' + zeroPadding(cd.getMonth() + 1, 2) + '-' + zeroPadding(cd.getDate(), 2) + ' ' + week[cd.getDay()];
  }
}
</script>

<style lang="scss" scoped>
#clock {
  font-family: 'Share Tech Mono', monospace;
  color: #000000;
  // position: absolute;
  text-align: center;
  // transform: translate(-50%, -50%);
  // text-shadow: 0 0 5px rgb(169, 159, 159),  0 0 5px rgba(255, 255, 255, 0);
  .time {
    letter-spacing: 0.05em;
    font-size: 1.3em;
  }
  .date {
    font-size: 1em;
  }
}
</style>
