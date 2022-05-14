from django.urls import include, path
from django.http.response import JsonResponse
from django.http.request import HttpRequest
from workshop.util.interface import *
from workshop.util.opcua import UaClient

client = UaClient()

# Connect ua server
client.connect("opc.tcp://localhost:4840/")


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
    path('GetControlGraph',GetControlGraph),
    path('GetAllExceptionReports',lambda request:myJsonResponse(getAllExceptionReports(request))),
    # path('GetReportDetailHtml',lambda request:getDetailReport(request)),
    path('GetReportDetailHtml', lambda request:myJsonResponse(getDetailReport(request))),

    path('GetAllWorkshopsInfo',lambda request:myJsonResponse(getAllWorkshopInfo(request))),
    path('SubmitWorkshop',lambda request:myJsonResponse(alterWorkshops(request))),
    path('DeleteWorkshop',lambda request:myJsonResponse(deleteWorkshop(request))),

    path('getRelationshipForm',lambda request:myJsonResponse(getRelationshipForm(request))),
    path('getAllWorkshopsId',lambda request:myJsonResponse(getAllWorkshopsId(request))),
    path('submitRelationship',lambda request:myJsonResponse(submitRelationship(request))),

    # New
    path('GetKanbanInfo', lambda request:myJsonResponse(getKanbanInfo(request, client=client))),
    path('testUaConnection', lambda request:myJsonResponse(testUaConnection(request))),
    path('connectUa', lambda request:myJsonResponse(connectUa(request, client=client))),
    path('fetchInformationModel', lambda request:myJsonResponse(getInformationModel(request, client=client))),
    path('deleteReport', lambda request:myJsonResponse(deleteReport(request)))
]

urlpatterns = [
    path('',include(workshop_patterns))
]