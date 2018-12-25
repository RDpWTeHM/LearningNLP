# Improve Function



[TOC]



## One by One display Detail

Develop this function for improve `get_seq2seqpost()` function(API)

### Get one Seq2Seq Post API

Get one Seq2Seq Post by API: `weibo/<weiboID>/get/seq2seqpost/<index>/`

```
API:   weibo/<weiboID>/get/seq2seqpost/<index>/
       ~~~~~~~~~~~~~   ~~  ~~~~~~~~~~
model:      ^ Weibo    ^action   ^ Seq2SeqPost
```

**Expect response json:**

```json
{
    "weiboID_of_from_id": '58371',
    "pub_date": '2018-12-25 06:51:19.818500+00:00',
    "hashtag": "早鸟分享",
    "text": "①活出自己：不要想着变成别人，etc...",
    "abstract": "18个建议提升人格魅力"
}
```

> where: value of "pub_data" is `datetime` cover to string.

#### Test Case(unit test)

该测试需要的 packages/modules:

```python
from django.test import TestCase

# Create your tests here.
import sys
from django.utils import timezone
import copy
from .models import Weibo, Seq2SeqPost
```

为测试类准备用于保存到数据库中的数据：

```python
class APIGetSeq2seqpostTest(TestCase):
    weibo_data4test = {"weiboID": '58371', "name": "新浪新闻客户端"}
    seq2seqpost_data4test_nohashtag = {}
    seq2seqpost_data4test = {
        "weiboID_of_from_id": '58371',
        "pub_date": timezone.now(),
        "hashtag": "早鸟分享",
        "text": "①活出自己：不要想着变成别人，做好自己，自信是魅力的根本；" +
                "②果断：行动力让人尊敬；③豁达：洒脱和宽容让你更阳光；" +
                "④不抱怨：絮絮叨叨诉说不幸，只会让别人看轻你；" +
                "⑤不讨好：总有人不喜欢你，做该做的事，只要无愧于心。愿这些小改变，让你更有魅力！ ...展开全文c",
        "abstract": "18个建议提升人格魅力",
    }
```

该单元测试具体代码：

```python
    def test_correctness(self):
        '''正确性测试

        使用预期的 API 和正确的预期输入，
        判断是否可以得到正确的结果。
        '''
        # create/save data in DB
        Weibo.objects.create(**self.weibo_data4test)
        _data_for_creat_on_DB_as_kwargs = copy.deepcopy(self.seq2seqpost_data4test)
        foreignKey_weiboID = _data_for_creat_on_DB_as_kwargs.pop("weiboID_of_from_id")
        _ = Seq2SeqPost.objects.filter(from_id=Weibo.objects.get(weiboID=foreignKey_weiboID))
        if _:  # in test case, DB should be clean.
            pass  # backend code maybe like: _.update(**_data_for_creat_on_DB_as_kwargs)
        else:
            _ = Seq2SeqPost.objects.create(
                from_id=Weibo.objects.get(weiboID=foreignKey_weiboID),
                **_data_for_creat_on_DB_as_kwargs)
            print("{!r}".format(_), file=sys.stderr)

        # request data
        response = self.client.get("/weibo/%d/get/seq2seqpost/%d/" % (
            Weibo.objects.get(weiboID=foreignKey_weiboID).id, 1))
        assert response.status_code == 200  # correctness test, expect 200.

        # cover python instance to string
        data = dict(zip(
            copy.deepcopy([_key for _key in self.seq2seqpost_data4test.keys()]),
            copy.deepcopy([str(self.seq2seqpost_data4test[_]) for _ in self.seq2seqpost_data4test.keys()]),
        ))
        data['body'] = data['text']

        self.assertDictEqual(json.loads(response.content), data)
```

run test:

```shell
Usage:
    GUI/web $ python manage.py test weibo
    # or test specified
    GUI/web $ python manage.py test weibo.APIGetSeq2seqpostTest
```

test result currently:

```shell
$ python manage.py test weibo
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
'18个建议提升人格魅力'
F
======================================================================
FAIL: test_correctness (weibo.tests.APIGetSeq2seqpostTest)
正确性测试
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/joseph/Jos/GitHub/LearningNLP/GUI/web/weibo/tests.py", \
line 54, in test_correctness
    assert response.status_code == 200  # correctness test, expect 200.
AssertionError

----------------------------------------------------------------------
Ran 1 test in 0.013s

FAILED (failures=1)
Destroying test database for alias 'default'...

```



#### Develop

##### parse API (url)

`urls.py` :

```python
    #
    # API
    #
    path("get/Seq2SeqPost/", views.get_Seq2SeqPost, name="get_Seq2SeqPost"),
    path("<int:pk>/get/seq2seqpost/<int:index>/",
         views.get_seq2seqpost, name="get_seq2seqpost"),
```

Note: change last "get/seq2seqpost/" url =to=> "/get/Seq2SeqPost/",

Change `views.py` too.



`views.py` achieve this function:

```python
def get_seq2seqpost(request, pk, index):
    """ 'weibo/<weiboID>/get/seq2seqpost/<index>/'
        -[o] response by json later
    """
    return HttpResponse("weibo pk: %d, seq2seqpost index: %d" % (pk, index))

```

:point_up: this functional just for first assert in TestCase cloud pass due to it just for `# correctness test, expect 200.`

*Check first assert whether pass or not:*

```shell
$ python manage.py test weibo
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
'18个建议提升人格魅力'
E
======================================================================
ERROR: test_correctness (weibo.tests.APIGetSeq2seqpostTest)
正确性测试
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/joseph/Jos/GitHub/LearningNLP/GUI/web/weibo/tests.py", \
line 57, in test_correctness
    self.assertDictEqual(response.json(), self.seq2seqpost_data4test)
  File "/home/joseph/.virtualenvs/fuuuckNetEaseMusic/lib/python3.6/\
site-packages/django/test/client.py", line 650, in _parse_json
    .format(response.get('Content-Type'))
ValueError: Content-Type header is "text/html; charset=utf-8", \
not "application/json"

----------------------------------------------------------------------
Ran 1 test in 0.040s

FAILED (errors=1)
Destroying test database for alias 'default'...
```

now, it failure at right place.

server could parse this API-url correctly.

##### response json data

```python
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

            return JsonResponse(data)
        except Seq2SeqPost.DoesNotExist:
            return Http404("index Seq2SeqPost Dose not exist")
    else:
        return HttpResponse("wrong request, please use GET")
    return HttpResponse("weibo pk: %d, seq2seqpost index: %d" % (pk, index))
```

修改 `views.py` 中对应 function 之后的测试结果：

```shell
$ python manage.py test weibo
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
'18个建议提升人格魅力'
.
----------------------------------------------------------------------
Ran 1 test in 0.014s

OK
Destroying test database for alias 'default'...
```

--- 测试通过！



#### Note

这个 test case - function 不仅仅测试了一个功能，

1. 解析 url -- 如果不能解析（API 无效）则该测试用例不会通过
2. DB 保存数据 -- 如果没有对应“正确”的 models，则 function 的开头构造数据即失败
3. 



## real  `[Crawl]`  button function

```
crawl_and_display()       crawler()
~~~~~~~~~~~~~~~~~~~       ~~~~~~~~~
    /\                        /\
    ||                        ||
  mainly HTML(Ajax)        do the crawl act!
```

### crawl and pre-display

#### 重构 HTML 模板

##### boostrapbase 模板

```HTML
{# weibo/templates/weibo/bootstrapbase.html #}
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <link rel="stylesheet" media="screen"
        href="https://cdn.bootcss.com/bootstrap/4.0.0/css/bootstrap.min.css"
     [...]
    <script src="https://cdn.bootcss.com/bootstrap/4.0.0/js/bootstrap.min.js"
            integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
            crossorigin="anonymous"></script>

    <title>{% block title_text %}{% endblock %}</title>

{% block js_in_head %}  
{% endblock js_in_head %}

  </head>
  <body>
    {% block body %}
    {% endblock %}
  </body>
</html>
```

##### index 页面继承 bootstrap 模板

```html
{# web/weibo/templates/weibo/index.html #}
{% extends 'weibo/bootstrapbase.html' %}

	{% block title_text %}IDs list on DB | Weibo {% endblock %}

{% block js_in_head %}  
{% endblock js_in_head %}

{% block body %}
	<div class="container">
	<div class="row">
		<div class="col-md-12 push-md-4 jumbotron">
		<div class="text-center">
		<h1>Weibo IDs list</h1>
		</div>
		<br/>

		<form method="POST" action="{% url 'weibo:add' %}">
[...]
[...]
		</table>
		<script>
			function crawler(_name){
				alert("Crawl " + _name);
				window.open("{% url 'weibo:crawler' %}?name=" + _name);
			}
		</script>
		</div>
	</div>
{% endblock body %}
```



#### crawl and pre-display 页面

##### django url 路由

```python
app_name = 'weibo'
urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.add, name="add"),

    path("crawler/", views.crawler, name="crawler"),

    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/crawl_and_display/",
         views.crawl_and_display, name="crawl_and_display"),

    #
    # API
    [...]
]
```

##### Simple Response function on `views.py`

```python
def crawl_and_display(request, pk):
    return HttpResponse(
        "<h1>you are at weibo/%d/crawl_and_display/</h1>" % pk)
```

##### update weibo index `href`

```html
[...]
            <tbody>
		{% for each_weibo in weibo_all_objects %}
			<tr><th scope="row">{{ each_weibo.id }}</th>
				<td><a href="{% url 'weibo:detail' each_weibo.id %}"
					   class="">
				{{ each_weibo.name }}</a>
				</td>
				<td><input type="button" class="btn btn-primary" 
					       name="crawler" id="crawler" value="Crawl"
					       onclick="crawler({{ each_weibo.pk }})"></td>
					       {# onclick="window.open('{% url 'weibo:crawl_and_display' each_weibo.pk %}')"></td> #}
			</tr>
		{% endfor %}
			</tbody>
		</table>
		<script>
			function crawler(_pk){
				var _url = `/weibo/${_pk}/crawl_and_display/`
				window.open(_url);
			}
		</script>
		</div>
```

> 对 line 11 使用 `{# #}` 注释后，line 12 去掉注释，该种方法也有效。



##### -[o] create the HTML





## Reference

N/A