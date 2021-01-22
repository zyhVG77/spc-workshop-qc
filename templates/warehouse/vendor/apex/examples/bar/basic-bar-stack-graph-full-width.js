var options = {
	chart: {
		height: 300,
		type: 'bar',
		stacked: true,
		stackType: '100%',
		toolbar: {
      show: false,
    },
    dropShadow: {
			enabled: true,
			opacity: 0.1,
			blur: 5,
			left: -10,
			top: 10
		},
	},
	plotOptions: {
		bar: {
			horizontal: true,
		},
	},
	stroke: {
		show: false,
	},
	series: [{
		name: '无损耗',
		data: [44, 55, 41, 37, 43, 43, 21]
	},{
		name: '微小损耗',
		data: [100, 94, 94, 88, 101, 104, 120]
	},{
		name: '轻度损耗',
		data: [70, 71, 65, 80, 94, 100, 54]
	},{
		name: '中度损耗',
		data: [25, 12, 19, 32, 25, 24, 10]
	},{
		name: '严重损耗',
		data: [9, 7, 5, 8, 6, 9, 4]
	}],
	xaxis: {
		categories: ["差速器盘角齿", "滤清器", "密封垫", "离合器盘", "刹车盘", "半轴螺栓", "凸轮轴"],
	},
	tooltip: {
		y: {
			formatter: function(val) {
				return val;
			}
		}
	},
	fill: {
		opacity: 1
	},
	legend: {
		position: 'bottom',
		horizontalAlign: 'center',
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
	colors: ['#00bb42', '#007ae1', "#6633FF", '#ff3e3e', '#990000'],
}

var chart = new ApexCharts(
	document.querySelector("#basic-bar-stack-graph-full-width"),
	options
);

chart.render();
