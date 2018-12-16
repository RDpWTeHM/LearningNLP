from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def crawler(request):
    return HttpResponse("<h1>you are in weibo -> crawler</h1>")
