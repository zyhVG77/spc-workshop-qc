var options = {
  chart: {
    height: 300,
    type: 'bar',
    stacked: true,
    stackType: '100%',
    toolbar: {
      show: false
    },
    dropShadow: {
      enabled: true,
      opacity: 0.1,
      blur: 5,
      left: -10,
      top: 10
    },
    zoom: {
      enabled: true
    }
  },
  responsive: [{
    breakpoint: 480,
    options: {
      legend: {
        position: 'bottom',
        offsetX: -10,
        offsetY: 0
      }
    }
  }],
  plotOptions: {
    bar: {
      horizontal: false,
    },
  },
  dataLabels: {
    enabled: true
  },
  series: [{
    name: '齿轮A',
    data: [44, 55, 41, 67, 22, 43]
  },{
    name: '轴承B',
    data: [13, 23, 20, 8, 13, 27]
  },{
    name: '热敏电阻C',
    data: [11, 17, 15, 15, 21, 14]
  },{
    name: '活塞D',
    data: [21, 7, 25, 13, 22, 8]
  }],
  xaxis: {
    type: 'datetime',
    categories: ['01/01/2011 GMT', '01/02/2011 GMT', '01/03/2011 GMT', '01/04/2011 GMT', '01/05/2011 GMT', '01/06/2011 GMT'],
  },
  legend: {
    position: 'top',
    offsetY: 10
  },
  fill: {
    opacity: 1
  },
  grid: {
    borderColor: '#ced1e0',
    strokeDashArray: 5,
    xaxis: {
      lines: {
        show: true
      }
    },   
    yaxis: {
      lines: {
        show: false,
      } 
    },
    padding: {
      top: 0,
      right: 0,
      bottom: 0,
      left: 0
    }, 
  },
  colors: ['#007ae1', '#ff3e3e', '#00bb42', '#ffbf05'],
}
var chart = new ApexCharts(
  document.querySelector("#basic-column-stack-graph-fullheight"),
  options
);
chart.render();


var options2 = {
  chart: {
    height: 300,
    type: 'bar',
    stacked: true,
    stackType: '100%',
    toolbar: {
      show: false
    },
    dropShadow: {
      enabled: true,
      opacity: 0.1,
      blur: 5,
      left: -10,
      top: 10
    },
    zoom: {
      enabled: true
    }
  },
  responsive: [{
    breakpoint: 480,
    options: {
      legend: {
        position: 'bottom',
        offsetX: -10,
        offsetY: 0
      }
    }
  }],
  plotOptions: {
    bar: {
      horizontal: false,
    },
  },
  dataLabels: {
    enabled: true
  },
  series: [{
    name: '齿轮A',
    data: [43, 22, 41, 67, 55, 44]
  },{
    name: '轴承B',
    data: [13, 20, 13, 23, 8, 27]
  },{
    name: '热敏电阻C',
    data: [11, 21, 15, 17, 15, 14]
  },{
    name: '活塞D',
    data: [21, 25, 22, 7, 13, 8]
  }],
  xaxis: {
    type: 'datetime',
    categories: ['01/01/2011 GMT', '01/02/2011 GMT', '01/03/2011 GMT', '01/04/2011 GMT', '01/05/2011 GMT', '01/06/2011 GMT'],
  },
  legend: {
    position: 'top',
    offsetY: 10
  },
  fill: {
    opacity: 1
  },
  grid: {
    borderColor: '#ced1e0',
    strokeDashArray: 5,
    xaxis: {
      lines: {
        show: true
      }
    },
    yaxis: {
      lines: {
        show: false,
      }
    },
    padding: {
      top: 0,
      right: 0,
      bottom: 0,
      left: 0
    },
  },
  colors: ['#007ae1', '#ff3e3e', '#00bb42', '#ffbf05'],
}
var chart_2 = new ApexCharts(
    document.querySelector("#basic-column-stack-graph-fullheight-2"),
    options2
);
chart_2.render();
