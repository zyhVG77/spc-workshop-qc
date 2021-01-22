var options = {
	chart: {
		height: 300,
		type: 'line',
		dropShadow: {
			enabled: true,
			opacity: 0.1,
			blur: 5,
			left: -10,
			top: 10
		},
		zoom: {
			enabled: false
		}
	},
	dataLabels: {
		enabled: false
	},
	stroke: {
		curve: 'straight',
		width: 3,
        dashArray: [0, 8, 8, 8]
	},
	series: [{
		name: "单值",
		data: [3.82,4.23, 3.85, 4.32, 4.01,3.41,4.22,4.12]
		}, {
		name: "UCL",
		data: [4.33, 4.33, 4.33, 4.33, 4.33, 4.33, 4.33, 4.33, 4.33]
		}, {
		name: "LCL",
		data: [3.30, 3.30, 3.30, 3.30, 3.30, 3.30, 3.30, 3.30, 3.30]
		}, {
		name: "中心线",
		data: [3.77, 3.77, 3.77, 3.77, 3.77, 3.77, 3.77, 3.77, 3.77]
	}],
	title: {
		text: '齿轮粗糙度',
		align: 'center'
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
	xaxis: {
		categories: ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
	},
	theme: {
		monochrome: {
			enabled: true,
			color: '#1273eb',
			shadeIntensity: 0.1
		},
	},
	fill: {
		type: 'gradient',
		gradient: {
			shade: 'light',
			gradientToColors: ['#007ae1', '#ff3e3e', '#00bb42', '#ffbf05'],
			shadeIntensity: 1,
			type: 'horizontal',
			opacityFrom: 1,
			opacityTo: 1,
			stops: [0, 100, 100, 100, 100]
		},
	},
	markers: {
		size: 0,
		opacity: 0.2,
		colors: ['#007ae1', '#ff3e3e', '#00bb42', '#ffbf05'],
		strokeColor: "#fff",
		strokeWidth: 2,
		hover: {
			size: 7,
		}
	},
}

var chart = new ApexCharts(
	document.querySelector("#basic-line-graph"),
	options
);

chart.render();