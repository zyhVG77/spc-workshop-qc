var options = {
	chart: {
		width: 400,
		type: 'pie',
	},
	labels: ['油泵', '化油器', '皮带', '刹车蹄', '平衡块'],
	series: [20, 20, 20, 20, 20],
	responsive: [{
		breakpoint: 480,
		options: {
			chart: {
				width: 200
			},
			legend: {
				position: 'bottom'
			}
		}
	}],
	stroke: {
		width: 0,
	},
	colors: ['#007ae1', '#ff3e3e', '#00bb42', '#ffbf05'],
}
new ApexCharts(
	document.querySelector("#basic-pie-graph"),
	options
).render();

var options1 = {
	chart: {
		width: 400,
		type: 'pie',
	},
	labels: ['发动机配件', '传动系配件', '制动系配件', '转向系配件', '行走系配件'],
	series: [40, 10, 35, 5, 10],
	responsive: [{
		breakpoint: 480,
		options: {
			chart: {
				width: 200
			},
			legend: {
				position: 'bottom'
			}
		}
	}],
	stroke: {
		width: 0,
	},
	colors: ['#007ae1', '#ff3e3e', '#00bb42', '#ffbf05'],
};

new ApexCharts(
	document.querySelector("#basic-pie-graph1"),
	options1
).render();

var options2 = {
	chart: {
		width: 400,
		type: 'pie',
	},
	labels: ['高流通产品', '短期贮存', '中期贮存', '长期贮存'],
	series: [40, 20, 20, 20],
	responsive: [{
		breakpoint: 480,
		options: {
			chart: {
				width: 200
			},
			legend: {
				position: 'bottom'
			}
		}
	}],
	stroke: {
		width: 0,
	},
	colors: ['#007ae1', '#ff3e3e', '#00bb42', '#ffbf05'],
};

new ApexCharts(
	document.querySelector("#basic-pie-graph2"),
	options2
).render();