from django.urls import path

from django.http import HttpResponse

from . import views


urlpatterns = [
    path("", views.index, name="index"),

    path("crawler/", views.crawler, name="crawler"),
    path("test_crawler/", views.test_crawler, name="test_crawler"),
]
