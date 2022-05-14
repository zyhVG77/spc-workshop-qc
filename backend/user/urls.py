from django.urls import include, path
from django.shortcuts import render
from django.http.response import JsonResponse
from django.http.request import HttpRequest
from user.util.interface import *

class myJsonResponse(JsonResponse):
    pass

user_patterns = [
    path('ConfirmLogin',lambda request:myJsonResponse(confirmLogin(request))),
    path('GetUserInfo',lambda request:myJsonResponse(getUserInfo(request))),
    path('ModifyPassword',lambda request:myJsonResponse(modifyPassword(request))),
    path('UpdateUserInfo',lambda request:myJsonResponse(updateUserInfo(request))),
    path('getUserId', lambda request:myJsonResponse(getUserId(request)))
]

urlpatterns = [
    path('',include(user_patterns))
]