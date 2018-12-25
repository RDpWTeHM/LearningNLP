# Improve Function



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
    "weiboID_of_from_id": 58371,
    "pub_date": 2018-12-25 10:9:23,
    "hashtag": "早鸟分享",
    "text": "①活出自己：不要想着变成别人，etc...",
    "abstract": "18个建议提升人格魅力"
}
```



#### Test Case(unit test)

```python
from django.test import TestCase

# Create your tests here.
import sys
from django.utils import timezone
import copy
from .models import Weibo, Seq2SeqPost

class APIGetSeq2seqpostTest(TestCase):
    weibo_data4test = {"weiboID": 58371, "name": "新浪新闻客户端"}
    seq2seqpost_data4test_nohashtag = {}
    seq2seqpost_data4test = {
        "weiboID_of_from_id": 58371,
        "pub_date": timezone.now(),
        "hashtag": "早鸟分享",
        "text": "①活出自己：不要想着变成别人，做好自己，自信是魅力的根本；" +
                "②果断：行动力让人尊敬；③豁达：洒脱和宽容让你更阳光；" +
                "④不抱怨：小改变，...展开全文c",
        "abstract": "18个建议提升人格魅力",
    }

    def test_correctness(self):
        '''正确性测试

        使用预期的 API 和正确的预期输入，
        判断是否可以得到正确的结果。
        '''
        Weibo.objects.create(**self.weibo_data4test)
        _test_data = copy.deepcopy(self.seq2seqpost_data4test)
        foreignKey_weiboID = _test_data.pop("weiboID_of_from_id")
        _ = Seq2SeqPost.objects.filter(from_id=Weibo.objects.get(weiboID=foreignKey_weiboID))
        if _:  # in test case, DB should be clean.
            pass  # backend code maybe like: _.update(**_test_data)
        else:
            test_data = Seq2SeqPost.objects.create(
                from_id=Weibo.objects.get(weiboID=foreignKey_weiboID),
                **_test_data)
            print("[Debug] {!r}".format(test_data), file=sys.stderr)

        # request data
        response = self.client.get("/weibo/%d/get/seq2seqpost/%d/")
        assert response.status_code == 200  # correctness test, expect 200.
        # assert Test Cause pass?
        self.assertDictEqual(response.json(), self.seq2seqpost_data4test)
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







## real  `[Crawl]`  button function

