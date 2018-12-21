from django.urls import path

from django.http import HttpResponse

from . import views


urlpatterns = [
    path("", lambda request: HttpResponse("<h1>Hello Weibo App</h1>")),

    path("crawler/", views.crawler, name="crawler"),
    path("test_crawler/", views.test_crawler, name="test_crawler"),
]
