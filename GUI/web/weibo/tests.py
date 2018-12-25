"""GUI/web/weibo/tests.py
Usage:
    GUI/web $ python manage.py test weibo
    # or test specified
    ~~GUI/web $ python manage.py test weibo.APIGetSeq2seqpostTest~~
"""

from django.test import TestCase

# Create your tests here.
import sys
# from datetime import datetime
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
                "④不抱怨：絮絮叨叨诉说不幸，只会让别人看轻你；" +
                "⑤不讨好：总有人不喜欢你，做该做的事，只要无愧于心。愿这些小改变，让你更有魅力！ ...展开全文c",
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
        if _:
            '''in test case, DB should be clean.
            '''
            pass  # update
        else:
            test_data = Seq2SeqPost.objects.create(
                from_id=Weibo.objects.get(weiboID=foreignKey_weiboID),
                **_test_data)
            print("{!r}".format(test_data), file=sys.stderr)

        # request data
        response = self.client.get("/weibo/%d/get/seq2seqpost/%d/" % (
            Weibo.objects.get(weiboID=foreignKey_weiboID).id, 1))
        assert response.status_code == 200  # correctness test, expect 200.

        self.assertDictEqual(response.json(), self.seq2seqpost_data4test)
