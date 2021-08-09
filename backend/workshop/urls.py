from django.urls import include, path
from django.shortcuts import render
from workshop.util.graphCheck import getGraph
from django.http.response import JsonResponse
from django.http.request import HttpRequest
from workshop.util.interface import *

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

workshop_patterns = [
    path('GetAllProducts',lambda request:myJsonResponse(getProducts(request))),
    path('SubmitProduct',lambda request:myJsonResponse(alterProducts(request))),
    path('DeleteProduct',lambda request:myJsonResponse(deleteProduct(request))),
    path('GetControlGraph',GetControlGraph),#todo : modify to this => ,lambda request:myJsonResponse(getControlGraph(request))),
    path('GetAllExceptionReports',lambda request:myJsonResponse(getAllExceptionReports(request))),
    # path('GetReportDetailHtml',lambda request:getDetailReport(request)), # todo: not Json Response
    path('GetReportDetailHtml', lambda request:myJsonResponse(getDetailReport(request))),  # todo: not Json Response

    path('GetAllWorkshopsInfo',lambda request:myJsonResponse(getAllWorkshopInfo(request))),
    path('SubmitWorkshop',lambda request:myJsonResponse(alterWorkshops(request))),
    path('DeleteWorkshop',lambda request:myJsonResponse(deleteWorkshop(request))),

    path('getRelationshipForm',lambda request:myJsonResponse(getRelationshipForm(request))),
    path('getUserId',lambda request:myJsonResponse(getUserId(request))),
    path('getAllWorkshopsId',lambda request:myJsonResponse(getAllWorkshopsId(request))),
    path('submitRelationship',lambda request:myJsonResponse(submitRelationship(request)))
]

urlpatterns = [
    path('test',get_graph),
    path('',include(workshop_patterns))
]