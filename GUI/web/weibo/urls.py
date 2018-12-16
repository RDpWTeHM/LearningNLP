from django.urls import path

from django.http import HttpResponse

urlpatterns = [
    path("", lambda request: HttpResponse("<h1>Hello Weibo App</h1>")),
]

