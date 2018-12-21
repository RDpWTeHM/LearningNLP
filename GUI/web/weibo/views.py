from django.shortcuts import render

# Create your views here.
import sys
import os
from time import sleep
from django.http import HttpResponse


def crawler(request):
    return HttpResponse("<h1>you are in weibo -> crawler</h1>")


def test_crawler(request):
    from threading import Thread
    import sites.weibo.request as cweibo  # Reference to > "package path" part
    test_weibo_id = "https://www.weibo.com/58371?topnav=1&wvr=6&topsug=1"
    test_weibo = cweibo.WeiboSpider(test_weibo_id)
    t = Thread(target=test_weibo.run, args=(test_weibo.qdata, ))
    t.setDaemon(True)
    t.start()
    del t

    sleep(80)

    for post in test_weibo.consumer(test_weibo.qdata):
        # storage data to DB
        print(post, file=sys.stderr)
        sleep(1)

    return HttpResponse("Success")
