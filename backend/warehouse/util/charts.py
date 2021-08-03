from warehouse.models import measure_form_info
from warehouse.util.utils import SCALE, MAXCOLSPAN
from datetime import datetime
import json


def generateXbarRIMREchartsDict(graph):
    progressIndex = graph.progressIndex
    options = {
        'title': [
            {
                'text': graph.measure_plan.product.name + ': ' + graph.control_plan.parameter.name,
                'subtext': 'X bar',
            },
            {
                'subtext': 'R bar',
                'bottom': '49.25%'
            }
        ],
        'legend': {'data': [graph.control_plan.parameter.name, 'Range']},
        'grid': [
            {
                'left': '10%',
                'right': '10%',
                'height': '38%',
            },
            {
                'left': '10%',
                'right': '10%',
                'height': '38%',
                'bottom': '10%'
            }
        ],
        'xAxis': [
            {
                'data': graph.point_ids,
                'gridIndex': 0
            },
            {
                'data': graph.point_ids,
                'gridIndex': 1
            },
        ],
        'yAxis': [
            {
                'name': graph.control_plan.parameter.unit,
                'min': graph.Xmin,
                'max': graph.Xmax,
                'interval': (graph.Xmax - graph.Xmin) / (6 + 2 * SCALE),
                'gridIndex': 0,
                'splitArea': {'show': True}
            },
            {
                'name': 'Range',
                'min': graph.Rmin,
                'max': graph.Rmax,
                'interval': (graph.Rmax - graph.Rmin) / (6 + 2 * SCALE),
                'gridIndex': 1,
                'splitArea': {'show': True}
            }
        ],
        'tooltip': {
            'axisPointer': {'type': 'cross'},
            'trigger': 'axis',
            'formatter': "{b0}"
                         "<br/>{a0}:&nbsp<span style='float:right;'>{c0}</span>"
                         "<br/>{a1}:&nbsp<span style='float:right;'>{c1}</span>"
                         "<br/>" + progressIndex['name'] + ":&nbsp<span style='float:right;'>" + str(
                progressIndex['value']) + '</span>'
        },
        'axisPointer': {'link': {'xAxisIndex': 'all'}},
        'toolbox': {
            'show': True,
            'feature': {
                'dataZoom': {'yAxisIndex': 'none'},
                'restore': {},
                'dataView': {'readOnly': True},
                'saveAsImage': {'type': 'png'}
            }
        },
        'series': [
            {
                'name': graph.control_plan.parameter.name,
                'type': 'line',
                'data': graph.pointx,
                'xAxisIndex': 0,
                'yAxisIndex': 0,
                'itemStyle': {'color': 'rgb(0,0,196)'},
                'markLine': {
                    'symbol': ['none', 'none'],
                    'precision': graph.scale,
                    'data': [
                        {
                            'name': 'UCL',
                            'yAxis': graph.uclx,
                            'lineStyle': {
                                'type': 'solid',
                                'color': 'rgb(255,0,0)'
                            }

                        },
                        {
                            'name': 'CL',
                            'yAxis': graph.clx,
                            'lineStyle': {
                                'type': 'solid',
                                'color': 'rgb(0,196,0)'
                            }
                        },
                        {
                            'name': 'LCL',
                            'yAxis': graph.lclx,
                            'tooltip': {},
                            'lineStyle': {
                                'type': 'solid',
                                'color': 'rgb(255,0,0)'
                            }
                        },
                    ]
                }
            },
            {
                'name': 'Range',
                'type': 'line',
                'data': graph.pointr,
                'xAxisIndex': 1,
                'yAxisIndex': 1,
                'itemStyle': {'color': 'rgb(196,0,0)'},
                'markLine': {
                    'symbol': ['none', 'none'],
                    'precision': graph.scale,
                    'data': [
                        {
                            'name': 'UCL',
                            'yAxis': graph.uclr,
                            'lineStyle': {
                                'type': 'solid',
                                'color': 'rgb(255,0,0)'
                            }

                        },
                        {
                            'name': 'CL',
                            'yAxis': graph.clr,
                            'lineStyle': {
                                'type': 'solid',
                                'color': 'rgb(0,196,0)'
                            }
                        },
                        {
                            'name': 'LCL',
                            'yAxis': graph.lclr,
                            'tooltip': {},
                            'lineStyle': {
                                'type': 'solid',
                                'color': 'rgb(255,0,0)'
                            }
                        },
                    ]
                }
            }
        ]
    }
    dataZoom = [{'xAxisIndex': [0, 1]}]

    uslx = {
        'name': 'USL',
        'yAxis': graph.uslx,
        'tooltip': {},
        'lineStyle': {
            'type': 'solid',
            'color': 'rgb(128,0,0)'
        }
    } if graph.uslx else None
    lslx = {
        'name': 'LSL',
        'yAxis': graph.lslx,
        'tooltip': {},
        'lineStyle': {
            'type': 'solid',
            'color': 'rgb(128,0,0)'
        }
    } if graph.lslx else None

    if graph.size > graph.measure_plan.sample_size:
        options['dataZoom'] = dataZoom
    if uslx:
        options['series'][0]['markLine']['data'].append(uslx)
    if lslx:
        options['series'][0]['markLine']['data'].append(lslx)
    return options


def generateXbarsEchartsDict(graph):
    progressIndex = graph.progressIndex
    options = {
        'title': [
            {
                'text': graph.measure_plan.product.name + ': ' + graph.control_plan.parameter.name,
                'subtext': 'X bar',
            },
            {
                'subtext': 's bar',
                'bottom': '49.25%'
            }
        ],
        'legend': {'data': [graph.control_plan.parameter.name, 'STDEV']},
        'grid': [
            {
                'left': '10%',
                'right': '10%',
                'height': '38%',
            },
            {
                'left': '10%',
                'right': '10%',
                'height': '38%',
                'bottom': '10%'
            }
        ],
        'xAxis': [
            {
                'data': graph.point_ids,
                'gridIndex': 0
            },
            {
                'data': graph.point_ids,
                'gridIndex': 1
            },
        ],
        'yAxis': [
            {
                'name': graph.control_plan.parameter.unit,
                'min': graph.Xmin,
                'max': graph.Xmax,
                'interval': (graph.Xmax - graph.Xmin) / (6 + 2 * SCALE),
                'gridIndex': 0,
                'splitArea': {'show': True}
            },
            {
                'name': 'Range',
                'min': graph.Smin,
                'max': graph.Smax,
                'interval': (graph.Smax - graph.Smin) / (6 + 2 * SCALE),
                'gridIndex': 1,
                'splitArea': {'show': True}
            }
        ],
        'tooltip': {
            'axisPointer': {'type': 'cross'},
            'trigger': 'axis',
            'formatter': "{b0}"
                         "<br/>{a0}:&nbsp<span style='float:right;'>{c0}</span>"
                         "<br/>{a1}:&nbsp<span style='float:right;'>{c1}</span>"
                         "<br/>" + progressIndex['name'] + ":&nbsp<span style='float:right;'>" + str(
                progressIndex['value']) + '</span>'
        },
        'axisPointer': {'link': {'xAxisIndex': 'all'}},
        'toolbox': {
            'show': True,
            'feature': {
                'dataZoom': {'yAxisIndex': 'none'},
                'restore': {},
                'dataView': {'readOnly': True},
                'saveAsImage': {'type': 'png'}
            }
        },
        'series': [
            {
                'name': graph.control_plan.parameter.name,
                'type': 'line',
                'data': graph.pointx,
                'xAxisIndex': 0,
                'yAxisIndex': 0,
                'itemStyle': {'color': 'rgb(0,0,196)'},
                'markLine': {
                    'symbol': ['none', 'none'],
                    'precision': graph.scale,
                    'data': [
                        {
                            'name': 'UCL',
                            'yAxis': graph.uclx,
                            'lineStyle': {
                                'type': 'solid',
                                'color': 'rgb(255,0,0)'
                            }

                        },
                        {
                            'name': 'CL',
                            'yAxis': graph.clx,
                            'lineStyle': {
                                'type': 'solid',
                                'color': 'rgb(0,196,0)'
                            }
                        },
                        {
                            'name': 'LCL',
                            'yAxis': graph.lclx,
                            'tooltip': {},
                            'lineStyle': {
                                'type': 'solid',
                                'color': 'rgb(255,0,0)'
                            }
                        },
                    ]
                }
            },
            {
                'name': 'STDEV',
                'type': 'line',
                'data': graph.points,
                'xAxisIndex': 1,
                'yAxisIndex': 1,
                'itemStyle': {'color': 'rgb(196,0,0)'},
                'markLine': {
                    'symbol': ['none', 'none'],
                    'precision': int(graph.scale / 2),
                    'data': [
                        {
                            'name': 'UCL',
                            'yAxis': graph.ucls,
                            'lineStyle': {
                                'type': 'solid',
                                'color': 'rgb(255,0,0)'
                            }

                        },
                        {
                            'name': 'CL',
                            'yAxis': graph.cls,
                            'lineStyle': {
                                'type': 'solid',
                                'color': 'rgb(0,196,0)'
                            }
                        },
                        {
                            'name': 'LCL',
                            'yAxis': graph.lcls,
                            'tooltip': {},
                            'lineStyle': {
                                'type': 'solid',
                                'color': 'rgb(255,0,0)'
                            }
                        },
                    ]
                }
            }
        ]
    }
    dataZoom = [{'xAxisIndex': [0, 1]}]

    uslx = {
        'name': 'USL',
        'yAxis': graph.uslx,
        'tooltip': {},
        'lineStyle': {
            'type': 'solid',
            'color': 'rgb(128,0,0)'
        }
    } if graph.uslx else None
    lslx = {
        'name': 'LSL',
        'yAxis': graph.lslx,
        'tooltip': {},
        'lineStyle': {
            'type': 'solid',
            'color': 'rgb(128,0,0)'
        }
    } if graph.lslx else None

    if graph.size > graph.measure_plan.sample_size:
        options['dataZoom'] = dataZoom
    if uslx:
        options['series'][0]['markLine']['data'].append(uslx)
    if lslx:
        options['series'][0]['markLine']['data'].append(lslx)
    return options


def generatePNpCUEchartsDict(graph):
    from database.util.graphCheck import pChart, npChart, cChart, uChart
    if type(graph) == pChart:
        subText = 'p Chart'
    elif type(graph) == npChart:
        subText = 'np Chart'
    elif type(graph) == cChart:
        subText = 'c Chart'
    elif type(graph) == uChart:
        subText = 'u Chart'
    else:
        assert False
    options = {
        'title': {
            'text': graph.measure_plan.product.name + ': ' + graph.control_plan.parameter.name,
            'subtext': subText,
        },
        'grid': {
            'left': '10%',
            'right': '10%',
        },
        'xAxis': {'data': graph.point_ids},
        'yAxis': {
            'name': graph.control_plan.parameter.unit,
            'min': graph.min,
            'max': graph.max,
            'interval': (graph.max - graph.min) / (6 + 2 * SCALE),
            'splitArea': {'show': True}
        },
        'tooltip': {'axisPointer': {'type': 'cross'}, },
        'toolbox': {
            'show': True,
            'feature': {
                'dataZoom': {'yAxisIndex': 'none'},
                'restore': {},
                'dataView': {'readOnly': True},
                'saveAsImage': {'type': 'png'}
            }
        },
        'series': [
            {
                'name': graph.control_plan.parameter.name,
                'type': 'line',
                'data': graph.point,
                'itemStyle': {'color': 'rgb(0,0,196)'},
                'markLine': {
                    'symbol': ['none', 'none'],
                    'precision': graph.scale,
                    'data': [
                        {
                            'name': 'UCL',
                            'yAxis': graph.ucl,
                            'lineStyle': {
                                'type': 'solid',
                                'color': 'rgb(255,0,0)'
                            }

                        },
                        {
                            'name': 'CL',
                            'yAxis': graph.cl,
                            'lineStyle': {
                                'type': 'solid',
                                'color': 'rgb(0,196,0)'
                            }
                        },
                        {
                            'name': 'LCL',
                            'yAxis': graph.lcl,
                            'tooltip': {},
                            'lineStyle': {
                                'type': 'solid',
                                'color': 'rgb(255,0,0)'
                            }
                        },
                    ]
                }
            }
        ]
    }
    dataZoom = [{'xAxisIndex': [0, 1]}]

    usl = {
        'name': 'USL',
        'yAxis': graph.usl,
        'tooltip': {},
        'lineStyle': {
            'type': 'solid',
            'color': 'rgb(128,0,0)'
        }
    } if graph.uslx else None
    lsl = {
        'name': 'LSL',
        'yAxis': graph.lsl,
        'tooltip': {},
        'lineStyle': {
            'type': 'solid',
            'color': 'rgb(128,0,0)'
        }
    } if graph.lslx else None

    if graph.size > graph.measure_plan.sample_size:
        options['dataZoom'] = dataZoom
    if usl:
        options['series'][0]['markLine']['data'].append(usl)
    if lsl:
        options['series'][0]['markLine']['data'].append(lsl)
    return options


def generateReportDict(graph):
    from database.util.graphCheck import Xbar_R, Xbar_s, I_MR, pChart, npChart, cChart, uChart
    class myLines():
        def __init__(self):
            self.title = None
            self.head = None
            self.data = None

    len_points = len(graph.point_ids)
    chart_colspan = len_points + 1 if len_points <= MAXCOLSPAN else MAXCOLSPAN + 1
    chart_linenums = int(len_points / MAXCOLSPAN) + 1

    has_ppk = True

    control_point_table = []
    for linenum in range(chart_linenums):
        lines = myLines()
        lines.title = '控制点数据表' if linenum == 0 else ' '
        lines.head = ['控制点各属性 \ 子组编号' if linenum == 0 and colnum == 0 else
                      graph.point_ids[(chart_colspan - 1) * linenum + colnum - 1]
                      if colnum != 0 and (chart_colspan - 1) * linenum + colnum - 1 < len_points
                      else ' ' for colnum in range(chart_colspan)]
        if type(graph) == Xbar_s:
            lines.data = [
                [
                    'X' if colnum == 0 else
                    graph.pointx[(chart_colspan - 1) * linenum + colnum - 1]
                    if (chart_colspan - 1) * linenum + colnum - 1<len_points else ' '
                    for colnum in range(chart_colspan)
                ],
                [
                    's' if colnum == 0 else
                    graph.points[(chart_colspan - 1) * linenum + colnum - 1]
                    if(chart_colspan - 1) * linenum + colnum - 1 < len_points else ' '
                    for colnum in range(chart_colspan)
                ]
            ]

        elif type(graph) == Xbar_R or type(graph) == I_MR:
            lines.data = [
                [
                    'X' if colnum == 0 else
                    graph.pointx[(chart_colspan - 1) * linenum + colnum - 1]
                    if 0 <= (chart_colspan - 1) * linenum + colnum - 1 < len_points else ' '
                    for colnum in range(chart_colspan)
                ],
                [
                    'R' if colnum == 0 else
                    graph.pointr[(chart_colspan - 1) * linenum + colnum - 1]
                    if 0 <= (chart_colspan - 1) * linenum + colnum - 1 < len_points else ' '
                    for colnum in range(chart_colspan)
                ]
            ]

        else:  # type(graph) = p,np,c,u
            has_ppk = False
            lines.data = [
                [

                    graph.point[(chart_colspan - 1) * linenum + colnum - 1]
                    if 0 <= (chart_colspan - 1) * linenum + colnum - 1 < len_points else
                    {pChart: 'p', npChart: 'np', cChart: 'c', uChart: 'u'}[type(graph)]
                    if colnum == 0 else ''
                    for colnum in range(chart_colspan)
                ]
            ]

        control_point_table.append(lines)

    original_point_table = []
    original_point_datas = []
    maxScale = 0
    for original_point in graph._original_points:
        measure_form_id = original_point.measure_form.uid
        measure_form = measure_form_info.objects.get(uid=measure_form_id)
        parameter_data = measure_form.parameter_datas.filter(parameter=graph.control_plan.parameter).order_by('sample_id')
        parameter_data = [round(data.value,graph.scale) for data in parameter_data]
        original_point_datas.append(parameter_data)
        maxScale = maxScale if len(parameter_data) <= maxScale else len(parameter_data)

    for linenum in range(chart_linenums):
        lines = myLines()
        lines.title = '原始属性表' if linenum == 0 else ' '
        lines.head = ['组内样本编号 \ 子组编号' if linenum == 0 and colnum == 0 else
                      graph.point_ids[(chart_colspan - 1) * linenum + colnum - 1]
                      if colnum != 0 and (chart_colspan - 1) * linenum + colnum - 1 < len_points
                      else ' ' for colnum in range(chart_colspan)]
        lines.data = [
            [
                samplenum+1 if colnum == 0 else
                original_point_datas[(chart_colspan - 1) * linenum + colnum - 1][samplenum]
                if (chart_colspan - 1) * linenum + colnum - 1 < len_points and
                len(original_point_datas[(chart_colspan - 1) * linenum + colnum - 1]) > samplenum
                else ' ' for colnum in range(chart_colspan)
            ]
            for samplenum in range(maxScale)
        ]
        original_point_table.append(lines)

    echartsDict = graph.generateEchartsDict()
    echartsDict.pop('title')
    echartsDict.pop('legend')
    echartsDict.pop('tooltip')
    echartsDict.pop('axisPointer')
    echartsDict.pop('toolbox')
    echartsDict['animation'] = False
    if 'dataZoom' in echartsDict:
        echartsDict.pop('dataZoom')

    abnormalities = graph.getAbnormality()



    context = {
        'product_id': graph.measure_plan.product.uid,
        'product_name': graph.measure_plan.product.name,
        'product_type': graph.measure_plan.product.type,
        'parameter_id': graph.control_plan.parameter.parameter_id,
        'parameter_name': graph.control_plan.parameter.name,
        'parameter_unit': graph.control_plan.parameter.unit,
        'measure_plan_id': graph.measure_plan.uid,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'time': datetime.now().strftime('%X'),
        'chart_colspan': chart_colspan,
        'control_point_table': control_point_table,
        'original_point_table':original_point_table,
        'option': json.dumps(echartsDict),
        'abnormailty_count':len(abnormalities),
        'has_ppk':has_ppk,
        'cpk':graph.CPK if has_ppk else None,
        'ppk':graph.PPK if has_ppk else None,
        'abnormalities':abnormalities
    }

    return context
