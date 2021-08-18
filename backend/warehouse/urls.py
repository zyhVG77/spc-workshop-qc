from django.urls import include, path
from django.shortcuts import render
from workshop.util.graphCheck import getGraph
from django.http.response import JsonResponse
from django.http.request import HttpRequest
from warehouse.util.interface import *

def get_graph(request): # 这个用于测试, 无实际意义
    data = getGraph('00000000003','00000000003')
    content = data.generateReportDict()
    return render(request, 'Report.html', content)

def test(request:HttpRequest):
    print(request.body.decode())
    print("ok")
    return None

def GetControlGraph(request):
    result = getControlGraph(request)
    if isinstance(result,dict):
        return myJsonResponse(result)
    else:
        return result

class myJsonResponse(JsonResponse):
    pass

# user_patterns = [
#     path('ConfirmLogin',lambda request:myJsonResponse(confirmLogin(request))),
#     path('GetUserInfo',lambda request:myJsonResponse(getUserInfo(request))),
#     path('ModifyPassword',lambda x:None),
#     path('UpdateUserInfo',lambda request:myJsonResponse(updateUserInfo(request)))
# ]

warehouse_patterns = [
    path('GetStorageCells', lambda request: myJsonResponse(getStorageCells(request))),
    path('GetWarehouseInfo', lambda request: myJsonResponse(getWarehouseInfo(request))), # todo: url in documentation is wrong
    path('GetNumberOfStorageCells', lambda request: myJsonResponse(getNumberOfStorageCells(request))),
    path('GetStorageCellDetail', lambda request: myJsonResponse(getStorageCellDetail(request))),

    path('SubmitMeasurePlan', lambda request: myJsonResponse(submitMeasurePlan(request))),
    path('GetMeasurePlans', lambda request: myJsonResponse(getMeasurePlans(request))),
    path('DeleteMeasurePlan', lambda request: myJsonResponse(deleteMeasurePlan)),

    path('GetAllProducts',lambda request:myJsonResponse(getProducts(request))),
    path('SubmitProduct',lambda request:myJsonResponse(alterProducts(request))),
    path('DeleteProduct',lambda request:myJsonResponse(deleteProduct(request))),
    path('getControlGraph',GetControlGraph),#todo : modify to this => ,lambda request:myJsonResponse(getControlGraph(request))),
    path('GetAllExceptionReports',lambda request:myJsonResponse(getAllExceptionReports(request))),
    # path('GetReportDetailHtml',lambda request:getDetailReport(request)), # todo: not Json Response

    path('GetReportDetailHtml', lambda request:myJsonResponse(getDetailReport(request))),  # todo: not Json Response

    path('submitPutInForm',lambda request:myJsonResponse(submitPutInForm(request))),
    path('submitTakeOutForm',lambda request:myJsonResponse(submitTakeoutForm(request))),

    path('GetWarehouseBasicInfo',lambda request:myJsonResponse(getWarehouseBasicInfo(request))),
    path('GetWarehouseAffairs',lambda request:myJsonResponse(getWarehouseAffairs(request))),
    path('GetTodayStatistics',lambda request:myJsonResponse(getTodayStatistics(request))),
    path('GetFullYearStatistics',lambda request:myJsonResponse(getFullYearStatistics(request)))
]

urlpatterns = [
    path('test',get_graph),
    path('', include(warehouse_patterns))
]