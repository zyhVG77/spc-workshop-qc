from workshop.models import *
from user.util.utils import *

UNK = 'UNK' # 接口函数默认值
# TOKENTIMEOUT = 600 # 用户token生存时间
# WIDTH = 11 # 数据库uid宽度(不可更改)
SCALE = 1 # ecnarts数据图纵轴缩放程度
MAXCOLSPAN = 10 # 详细分析报告中，一行最多能容纳的子组个数
TEMPLATENAME = 'Report.html' # 渲染异常分析报告模板文件名 templates/Report.html
CELLSPERPAGE = 100 # 展示储位时每页的储位个数
# DEBUG = True # 后端程序运行时是否允许输出信息
SPC_parameters = { # SPC控制图常数表
    'XR':{
        'minSize': 2,
        'maxSize': 25,
        'A2':[None ,None ,1.880,1.023,0.729,0.577,0.483,0.419,0.373,0.337,
              0.308,0.285,0.266,0.249,0.235,0.223,0.212,0.203,0.194,0.187,
              0.180,0.173,0.167,0.162,0.157,0.153],
        'd2':[None ,None ,1.128,1.693,2.059,2.326,2.534,2.704,2.847,2.970,
              3.078,3.173,3.258,3.336,3.407,3.472,3.532,3.588,3.640,3.689,
              3.735,3.778,3.819,3.858,3.895,3.931],
        'D3':[None ,None ,0    ,0    ,0    ,0    ,0    ,0.076,0.136,0.184,
              0.223,0.256,.0283,0.307,0.328,0.347,0.363,0.378,0.391,0.403,
              0.415,0.425,0.434,0.443,0.451,0.459],
        'D4':[None ,None ,3.267,2.574,2.282,2.114,2.004,1.924,1.864,1.816,
              1.777,1.744,1.717,1.693,1.672,1.653,1.637,1.622,1.608,1.597,
              1.585,1.575,1.566,1.557,1.548,1.541]
    },
    'XS':{
        'minSize':2,
        'maxSize':25,
        'A3':[None ,None ,2.659,1.954,1.628,1.427,1.287,1.182,1.099,1.032,
              0.975,0.927,0.886,0.850,0.817,0.789,0.763,0.739,0.718,0.698,
              0.680,0.663,0.647,0.633,0.619,0.606],
        'c4':[None  ,None  ,0.7979,0.8862,0.9213,0.9400,0.9515,0.9594,0.9650,0.9693,
              0.9727,0.9754,0.9776,0.9794,0.9810,0.9823,0.9835,0.9845,0.9854,0.9862,
              0.9869,0.9876,0.9882,0.9887,0.9892,0.9896],
        'B3':[None ,None ,0    ,0    ,0    ,0    ,0.030,0.118,0.185,0.239,
              0.284,0.321,0.354,0.382,0.406,0.428,0.448,0.466,0.482,0.497,
              0.510,0.523,0.534,0.545,0.555,0.565],
        'B4':[None ,None ,3.267,2.568,2.266,2.089,1.970,1.882,1.815,1.761,
              1.716,1.679,1.646,1.618,1.594,1.572,1.552,1.534,1.518,1.503,
              1.490,1.477,1.466,1.455,1.445,1.435]
    },
    'IMR':{
        'minSize':2,
        'maxSize':10,
        'E2':[None ,None ,2.660,1.772,1.457,1.290,1.184,1.109,1.054,1.010,0.975],
        'd2':[None ,None ,1.128,1.693,2.059,2.326,2.534,2.704,2.847,2.970,3.078],
        'D3':[None ,None ,0    ,0    ,0    ,0    ,0    ,0.076,0.136,0.184,0.223],
        'D4':[None ,None ,3.267,2.574,2.282,2.114,2.004,1.924,1.864,1.816,1.777]
    }
}

if DEBUG:
    print('\nConfigs')
    print('---------------------------------------')
    print('DEBUG: ',DEBUG)
    print('TEMPLATENAME: ',TEMPLATENAME)
    print('MAXCOLSPAN: ',MAXCOLSPAN)
    print('SCALE: ',SCALE)
    print('WIDTH: ',WIDTH)
    print('TOKENTIMEOUT: ',TOKENTIMEOUT)
    print('UNK: ',UNK)

# def idIter(start=0):
#     id = start
#     while True:
#         yield str(id).rjust(WIDTH, '0')
#         id += 1

try:
    if DEBUG:
        print('\nWorkshop idIterators')
        print('---------------------------------------')
    product_uid = product_info.objects.last()
    par_uid = parameter_info.objects.last()
    control_plan_uid = control_plan_info.objects.last()
    measure_plan_uid = measure_plan_info.objects.last()
    measure_form_uid = measure_form_info.objects.last()
    parameter_data_uid = parameter_data_info.objects.last()
    control_point_uid = control_point_info.objects.last()
    abnormality_uid = abnormality_info.objects.last()
except:
    product_uid = par_uid = control_plan_uid = measure_plan_uid = measure_form_uid = \
    parameter_data_uid = control_point_uid = abnormality_uid = None
    if DEBUG:
        print('Initiallize idIterators failed')

product_uid = int(product_uid.uid if product_uid else -1) + 1
par_uid = int(par_uid.uid if par_uid else -1) + 1
control_plan_uid = int(control_plan_uid.uid if control_plan_uid else -1) + 1
measure_plan_uid = int(measure_plan_uid.uid if measure_plan_uid else -1) + 1
measure_form_uid = int(measure_form_uid.uid if measure_form_uid else -1) + 1
parameter_data_uid = int(parameter_data_uid.uid if parameter_data_uid else -1) + 1
control_point_uid = int(control_point_uid.uid if control_point_uid else -1) + 1
abnormality_uid = int(abnormality_uid.uid if abnormality_uid else -1) + 1

if DEBUG:
    print('product_uid: ',product_uid)
    print('uesr_uid: ',user_uid)
    print('par_uid: ',par_uid)
    print('control_plan_uid: ',control_plan_uid)
    print('measure_plan_uid: ',measure_plan_uid)
    print('measure_form_uid: ',measure_form_uid)
    print('parameter_data_uid: ',parameter_data_uid)
    print('control_point_uid: ',control_point_uid)
    print('abnormality_uid: ',abnormality_uid)

user_uid = idIter(user_uid)
product_uid = idIter(product_uid)
par_uid = idIter(par_uid)
control_plan_uid = idIter(control_plan_uid)
measure_plan_uid = idIter(measure_plan_uid)
measure_form_uid = idIter(measure_form_uid)
parameter_data_uid = idIter(parameter_data_uid)
control_point_uid = idIter(control_point_uid)
abnormality_uid = idIter(abnormality_uid)