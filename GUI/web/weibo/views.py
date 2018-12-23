from django.shortcuts import render

# Create your views here.
import sys
import os
from time import sleep
from django.http import HttpResponse

from .models import Weibo, Seq2SeqPost


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

    sleep(50)

    for post in test_weibo.consumer(test_weibo.qdata):
        weibo_id = '58371'
        try:
            weibo_id = Weibo.objects.get(weiboID=weibo_id)
        except Weibo.DoesNotExist:
            weibo_id = Weibo.objects.create(weiboID=weibo_id)
        import re

        data_dict = {}
        noHashTag_rule = re.compile("^【(.*)】(.*)$")
        result = re.findall(noHashTag_rule, str(post))
        if not result:
            hashTag_rule = re.compile('^#(.*)#【(.*)】(.*)$')
            result = re.findall(hashTag_rule, str(post))

            if not result:
                # logging here
                print("unknow format post:\n\t", str(post), file=sys.stderr)
                continue
            else:
                print("[Debug]", file=sys.stderr)
                print("\t result ==>>>", result, file=sys.stderr)
                data_dict["from_id"] = weibo_id
                # data_dict["pub_date"]  # not achive yet, use default.
                data_dict["hashtag"] = result[0][0]
                data_dict["text"] = result[0][2]
                data_dict["abstract"] = result[0][1]
                print("[Debug] data_dict", data_dict, file=sys.stderr)
        else:
            data_dict["from_id"] = weibo_id
            data_dict["text"] = result[0][1]
            data_dict["abstract"] = result[0][0]
        try:
            _ = Seq2SeqPost.objects.filter(abstract=data_dict["abstract"])
            if not _:
                del _; raise Seq2SeqPost.DoesNotExist
        except Seq2SeqPost.DoesNotExist:
            seq2seqpost = Seq2SeqPost()
            for key in data_dict.keys():
                setattr(seq2seqpost, key, data_dict[key])
            seq2seqpost.save()
        else:
            continue

        # print(post, file=sys.stderr)
        # sleep(0.3)

    return HttpResponse("Success")
