from django.shortcuts import render

# Create your views here.
import sys
import os
from time import sleep
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.http import Http404
from django.http import JsonResponse

from .models import Weibo, Seq2SeqPost
import re
import copy


def index(request):
    return render(request, "weibo/index.html",
                  {'weibo_all_objects': Weibo.objects.all(), },
                  )


def add(request):
    if request.method == 'POST':
        data = request.POST.get("new_crawl_target", None)
        result = re.findall("^id: (.*) & name: (.*)$", data)
        if not request:
            return HttpResponse("wrong format")
        else:
            weiboID = result[0][0]
            weibo_name = result[0][1]
            try:
                Weibo.objects.create(weiboID=weiboID, name=weibo_name)
                new_target = Weibo.objects.get(weiboID=weiboID)
                return redirect("/" + "weibo" + "/")
                #                      ~~~~~     ~~~~
                #                       ^ sync     ^ index page
                #                   with app_name
            except Exception as err:
                print("Exception: ", err, file=sys.stderr)
                raise


class CrawlResponse404(Exception):
    pass


def do_crawl(weiboID):
    from threading import Thread
    import sites.weibo.request as cweibo  # Reference to > "package path" part
    weibo_crawl = cweibo.WeiboSpider("https://www.weibo.com/%s" % weiboID)
    t = Thread(target=weibo_crawl.run, args=(weibo_crawl.qdata, ))
    t.setDaemon(True)
    t.start()
    del t

    sleep(30)
    weibo_obj = None
    for post in weibo_crawl.consumer(weibo_crawl.qdata):
        try:
            weibo_obj = Weibo.objects.get(weiboID=weiboID)
        except Weibo.DoesNotExist:
            raise CrawlResponse404("WeiboID: %s does not exist" % weiboID)

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
                # print("[Debug]", file=sys.stderr)
                # print("\t result ==>>>", result, file=sys.stderr)
                # data_dict["pub_date"]  # not achive yet, use default.
                data_dict["hashtag"] = result[0][0]
                data_dict["text"] = result[0][2]
                data_dict["abstract"] = result[0][1]
                # print("[Debug] data_dict", data_dict, file=sys.stderr)
        else:
            data_dict["text"] = result[0][1]
            data_dict["abstract"] = result[0][0]
        data_dict["from_id"] = weibo_obj

        if not Seq2SeqPost.objects.filter(abstract=data_dict["abstract"]):
            seq2seqpost = Seq2SeqPost()
            for key in data_dict.keys():
                setattr(seq2seqpost, key, data_dict[key])
            seq2seqpost.save()
        else:
            continue
    if weibo_obj:
        return "%d" % weibo_obj.pk
    else:
        raise CrawlResponse404("server busy")  # raise Http404 should be work!


def crawler(request):
    '''do crawler
      receive crawler weibo id name name

      do crawl, storage crawl to DB

      response 'status', 'crawl number of posts', 'this times start id on DB';
    '''
    if request.method == 'GET':
        try:
            _name = request.GET["name"]
        except Exception as e:
            print("TODO: more specify", e, file=sys.stderr)
            import traceback; traceback.print_exc();
            raise Http404("need specify name")
        else:
            try:
                print("crawler name: ", _name, file=sys.stderr)
                _target = Weibo.objects.get(name=_name)
                return HttpResponse(do_crawl(_target.weiboID))
            except Weibo.DoesNotExist:
                raise Http404(
                    "dose not exist this weibo name in DB, "
                    "please add it on Index page, then request again")
            except CrawlResponse404 as err:
                raise Http404("{}".format(err))
            except Exception as err:
                import traceback; traceback.print_exc();
                raise Http404("{}".format(err))


def crawl_and_display(request, pk):
    # ~~                                                     Browser
    #  ^------------------------------ return HTML ---------->  #
    #                                                          /|
    # views. <--- "weibo/crawler/"  <--- Ajax request  ------#  |
    # crawler()                                              *  /
    # run          API                                       * /
    # in           "weibo/get_seq2seqpost/"  <-- Ajax request -
    # backend!     to get "new" post one by one(and display) *  \
    #                |                                       *   |
    # views.          `--- response seq2seqpost by json -------> #
    # crawler()                                              *
    # finish work, ----- and response! --------------------> #
    #                                          got "weibo/crawler/" response,
    #                                          set MAX length to stop
    #                                          request "weibo/get_seq2seqpost/"
    #
    # mainly logical on crawl_and_display.html with crawler()
    #
    return render(request, "weibo/crawl_and_display.html",
                  {"Weibo_by_pk": get_object_or_404(Weibo, pk=pk)})


def get_Seq2SeqPost(request):
    if request.method == "GET":
        try:
            _weiboID = request.GET["weiboID"]
            _index = request.GET["index"]

            _obj = Weibo.objects.get(weiboID=_weiboID).seq2seqpost_set.all()[int(_index)]
            return HttpResponse(
                "<h1>" + _obj.abstract + "</h1>" +
                "<p><i>" + _obj.hashtag + "</i></p>" +
                "<p>" + _obj.text + "</p>"
            )
        except TypeError:  # "_index" must be integer
            raise
        except IndexError:
            raise
        except Weibo.DoesNotExist:
            return HttpResponse("dose not exist")
        except Seq2SeqPost.DoesNotExist:
            raise


def get_seq2seqpost(request, pk, index):
    """ 'weibo/<weiboID>/get/seq2seqpost/<index>/'
      Response by json!
    """
    if request.method == "GET":
        try:
            seq2seqpost_obj = get_object_or_404(Weibo, pk=pk).seq2seqpost_set.get(pk=index)

            fix_data = {"eliminate": ["_state", 'from_id_id', "id", ],  # don't include those data
                        "extra": ["weiboID_of_from_id", ],  # extra data
                        }
            data = dict(zip(  # cover object to string
                copy.deepcopy([_key for _key in seq2seqpost_obj.__dict__.keys()]),
                copy.deepcopy([str(getattr(seq2seqpost_obj, _)) for _ in seq2seqpost_obj.__dict__.keys()]),
            ))
            # do the action of fix
            for __k in fix_data["eliminate"]: data.pop(__k)
            for __k in fix_data["extra"]:
                if __k == "weiboID_of_from_id":
                    data[__k] = seq2seqpost_obj.from_id.weiboID
                # elif ...: <= example for expand

            # print(data, file=sys.stderr)
            return JsonResponse(data)
        except Seq2SeqPost.DoesNotExist:
            return Http404("index Seq2SeqPost Dose not exist")
    else:
        return HttpResponse("wrong request, please use GET")
    return HttpResponse("weibo pk: %d, seq2seqpost index: %d" % (pk, index))


def detail(request, pk):
    """-[o] update this and *.html that
      display one by one by Ajax.
    """
    weibo_obj = get_object_or_404(Weibo, pk=pk)
    try:
        return render(request, "weibo/detail.html",
                      {"weibo_obj": weibo_obj})
    except Exception:
        raise


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
