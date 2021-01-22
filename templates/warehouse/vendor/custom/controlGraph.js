

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
		data: [75.58, 81.11, 78.48, 86.42, 74.19, 83.19, 71.43,89.03, 77.43]
		}, {
		name: "UCL",
		data: [90, 90, 90, 90, 90, 90, 90, 90, 90]
		}, {
		name: "LCL",
		data: [70, 70, 70, 70, 70, 70, 70, 70, 70]
		}, {
		name: "中心线",
		data: [80.37, 80.37, 80.37, 80.37, 80.37, 80.37, 80.37, 80.37, 80.37]
	}],
	title: {
		text: '齿轮X03外径',
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



$(document).ready(function() {
	// $('#controlGraph').hide();
});


$('#drawControlGraph').click(function() {
	// $('#controlGraph').show();
	chart.render();
});