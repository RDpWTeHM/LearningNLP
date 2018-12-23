# Database of Weibo Posts

## *Overview*

[TOC]

## Create ORM model of Post

### Post look like

```
#早鸟分享#【不愿努力的人，才会觉得努力没用】三十而立像个紧箍咒，似乎到了这个年纪就必须完成什么。其实，年龄的增长并不可怕，怕的是你变得不愿改变自己，一味地沉浸在恐慌中。什么都不做，才是真正的来不及。但只要你不退缩，办法总比困难多，往想要的方向去努力，一步一个脚印， ...展开全文c

【#女孩遭猥亵乘客冷眼旁观# 司机拼死抓凶被殴打】12月19日，西安一公交司机周师傅，听见车厢中间有位年轻女乘客大喊“变态！”当时早高峰车厢里挤满了乘客。周师傅拦下该男子，没想到其直接冲着司机的面部就打了过来，车上乘客不仅不帮忙竟然还这样说↓↓事后周师傅回应↓↓O女孩遭猥亵司机拼死抓凶被打 全车乘客冷眼旁观

【心大！爷爷奶奶带3个孙子逛超市，离开时#把孙子忘在购物车里#】18日，浙江杭州，一超市购物车中坐着一名2岁小男孩，在嚎啕大哭。原来，孩子的爷爷奶奶带着3个孙子来买东西，装完东西就带着2个孙子骑电瓶车走了，回家才发现最小的孙子还在购物车里坐着。 L新浪新闻客户端的秒拍视频

#你啥看法#【成都#网红烤兔黑作坊加工后续# 负责人痛哭道歉：做食品做良心】12月20日晚，成都网红店王妈手撕烤兔玉林店加工作坊被爆卫生条件堪忧，加工作坊无证无照，卫生设施设备不完善，堆放原料的篮筐随意放在地上，有些甚至正对下水口。事件被爆后引发热议，并登上了微博热搜。12月21日，王妈手撕 ...展开全文c

```



### Create ORM

#### coding

```python
#### weibo > models.py ####
from django.db import models
from django.utils import timezone

import reprlib

class Weibo(models.Model):
    weiboID = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    
    def __repr__(self):
        return "{!r}".format(self.name)

class Post(models.Model):
    from_id = models.ForeignKey(Weibo, on_delete=models.CASCADE)
    pub_date = models.DateTimeField("date published", default=timezone.now)
    hashtag = models.CharField(max_length=200, default='')
    text = models.TextField()
    
    def __repr__(self):
        return "%s" % reprlib.repr(self.text)
    
class Seq2SeqPost(models.Model):
    from_id = models.ForeignKey(Weibo, on_delete=models.CASCADE)
    pub_date = models.DateTimeField("date published", default=timezone.now)
    hashtag = models.CharField(max_length=200, default='')
    text = models.TextField()

    abstract = models.CharField(max_length=512)

    def __init__(self, *args, **kw):
        super(Seq2SeqPost, self).__init__(*args, **kw)
        self.body = self.text

    def __repr__(self):
        return "%s" % reprlib.repr(self.abstract)
```

1. 请注意 line 31, 32 的 `Seq2SeqPost` 中的 `__init__`，对于重写 `__init__` 一定要调用父类方法，这样才能通过 django 的 ORM (model) 保存数据。

#### migrate

```shell
## 使用一下命令就可以生成 migration/ 文件夹下的 XXXX_initial.py 文件：
$ python manage.py makemigrations weibo
Migrations for 'weibo':
  weibo/migrations/0001_initial.py
    - Create model Post
    - Create model Seq2SeqPost
    - Create model Weibo
    - Add field from_id to seq2seqpost
    - Add field from_id to post

## 使用命令查看迁移命令会执行哪些 SQL 语句：
$ python manage.py sqlmigrate weibo 0001
## 确认之后， 执行以下命令就可以在数据库里创建新定义的模型的数据表：
$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, weibo
Running migrations:
  Applying weibo.0001_initial... OK

```

:point_up_2: Reference: Django Official Website- tutorial 02 



### Usage

#### 先修改一下 timezone

```python
### GUI/web/web/settings.py
[...]

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

[...]
```



#### 在 shell 中测试使用

```python
$ python manage.py shell
>>> from weibo.models import Weibo, Seq2SeqPost
>>> Weibo.objects.all()
<QuerySet []>
>>> weibo_id = Weibo(weiboID="58371", name="新浪新闻客户端")
>>> weibo_id.save()
>>> weibo_id.id
1
>>> weibo_id.name
'新浪新闻客户端'
>>> weibo_id.weiboID
'58371'
>>> Weibo.objects.all()
<QuerySet ['58371']>
>>>
>>> from django.utils import timezone
>>> from datetime import datetime
>>> import pytz
>>>
>>> del weibo_id
>>> weibo_id = Weibo.objects.get(pk=1)
>>> weibo
'新浪新闻客户端'
>>> weibo.name
'新浪新闻客户端'
>>> 
>>> weibo_id.seq2seqpost_set.all()
<QuerySet []>
# Create seq2seqpost:
>>> weibo_id.seq2seqpost_set.create(
        pub_date=datetime(2018, 12, 20, 10, 46, 0,
                          tzinfo=pytz.timezone('Asia/Shanghai')),
        # hashtag = ,
        text = "12月19日，西安一公交司机周师傅，听见车厢中间有位年轻女乘客大喊“变态！”当时早高峰车厢里挤满了乘客。周师傅拦下该男子，没想到其直接冲着司机的面部就打了过来，车上乘客不仅不帮忙竟然还这样说↓↓事后周师傅回应↓↓O女孩遭猥亵司机拼死抓凶被打 全车乘客冷眼旁观",
        abstract = "#女孩遭猥亵乘客冷眼旁观# 司机拼死抓凶被殴打", )
'#女孩遭猥亵乘客冷眼旁观# 司机拼死抓凶被殴打'
>>> weibo_id.seq2seqpost_set.all()
<QuerySet ['#女孩遭猥亵乘客冷眼旁观# 司机拼死抓凶被殴打']>
>>> seq2seq_test = Seq2SeqPost.objects.get(pk=1)                          
>>> seq2seq_test                                                         
'#女孩遭猥亵乘客冷眼旁观# 司机拼死抓凶被殴打'
>>> seq2seq_test.abstract                                                
'#女孩遭猥亵乘客冷眼旁观# 司机拼死抓凶被殴打'
>>> seq2seq_test.text                                                    
'12月19日，西安一公交司机周师傅，听见车厢中间有位年轻女乘客大喊“变态！”当时早高峰车厢里挤满了乘客。周师傅拦下该男子，没想到其直接冲着司机的面部就打了过来，车上乘客不仅不帮忙竟然还这样说↓↓事后周师傅回应↓↓O女孩遭猥亵司机拼死抓凶被打 全车乘客冷眼旁观'
>>> seq2seq_test.pub_date                                                
datetime.datetime(2018, 12, 20, 2, 40, tzinfo=<UTC>)
>>> seq2seq_test.from_id
'新浪新闻客户端'
>>>
```

:point_up_2: Reference: Django Official Website- tutorial 02 



#### 第一次爬取入库

原型的 `test_crawler` url 路径处理：

```python
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
        sleep(0.3)

    return HttpResponse("Success")
```

将 line 14 替换成如下 line 2 ~ 29 逻辑即可：

```python
    for post in test_weibo.consumer(test_weibo.qdata):
        weibo_id = '58371'
        weibo_id = Weibo.objects.get(weiboID=weibo_id)
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
                data_dict["from_id"] = weibo_id
                # data_dict["pub_date"]  # not achive yet, use default.
                data_dict["hashtag"] = result[0][0]
                data_dict["text"] = result[0][2]
                data_dict["abstract"] = result[0][1]
        else:
            data_dict["from_id"] = weibo_id
            data_dict["text"] = result[0][1]
            data_dict["abstract"] = result[0][0]
        seq2seqpost = Seq2SeqPost()
        for key in data_dict.keys():
            setattr(seq2seqpost, key, data_dict[key])
        seq2seqpost.save()
```

**注意，我们已经在 `python manage.py shell` 创建过“该” Weibo 表 的 weibo_ID 过了。**

如果没有创建该 id，是会报错的！

#### 测试爬取入库

**直接启动 django server 之后，在浏览器输入 `localhost:8000/weibo/test_crawler/` 即可。**



然后启动 `python manage.py shell` 来查看数据是否正确地保存到数据中：

```python
>>> from weibo.models import Weibo, Seq2SeqPost
>>> Seq2SeqPost.objects.all()
<QuerySet ['#女孩遭猥亵乘客冷眼旁观# 司机拼死抓凶被殴打', \
'跟风？高校出通知#用华为手机可免费上网#一个月', \
'#女孩遭猥亵乘客冷眼旁观# 司机拼死抓凶被殴打', \
'心大！爷爷奶奶带3个孙子...开时#把孙子忘在购物车里#', \
[...]
'#后妈开水烫伤男童下体#后续：下身烫伤耳朵化脓', \
'女孩遭猥亵司机拼死抓凶被打 全车乘客冷眼旁观', \
'重庆一男子存1.2吨硬币，银行20名员工一周才能清点完', \
'贵阳30岁民警抓涉毒嫌犯...通报现场同事痛哭：不能接受']>
#### 上面输出为了友好阅读经过了手动修改（换行和省略） ###
>>> for eachpost in Seq2SeqPost.objects.all():
        print("====" + "{!r}".format(eachpost.from_id) + "====")
        print("\t", eachpost.pub_date)
        print("\t", eachpost.hashtag)
        print("\t[", eachpost.abstract, "]")
        print("\t", eachpost.body)
===='新浪新闻客户端'====
	 2018-12-20 02:40:00+00:00
	 
	[ #女孩遭猥亵乘客冷眼旁观# 司机拼死抓凶被殴打 ]
	 12月19日，西安一公交司机周师傅，听见车厢中间有位年轻女乘客大喊“变态！”当时早高峰车厢里挤满了乘客。周师傅拦下该男子，没想到其直接冲着司机的面部就打了过来，车上乘客不仅不帮忙竟然还这样说↓↓事后周师傅回应↓↓O女孩遭猥亵司机拼死抓凶被打 全车乘客冷眼旁观
===='新浪新闻客户端'====
	 2018-12-22 12:24:29.421650+00:00
	 
	[ 跟风？高校出通知#用华为手机可免费上网#一个月 ]
	 12月18日，河南郑州某学校发布一则通知：凡使用华为系列手机的同学，凭手机到值班室登记，免费使用校园网一个月对此学生表示：不觉得是炒作，营销推广学生得到实惠挺好的。#你啥看法# L新浪新闻客户端的秒拍视频
===='新浪新闻客户端'====
	 2018-12-22 12:24:29.835419+00:00
	 
	[ #女孩遭猥亵乘客冷眼旁观# 司机拼死抓凶被殴打 ]
	 12月19日，西安270路公交线路司机周师傅，听见车厢中间有位20多岁的女乘客大喊“变态！”当时早高峰车厢里挤满了乘客。周师傅拦下该男子，没想到变态男多次殴打周师傅的头部，但周师傅一直紧紧地拽住他，直到警方赶到现场。然而全车人冷眼旁观没有人起 ...展开全文c
===='新浪新闻客户端'====
	 2018-12-22 12:24:30.257949+00:00
	 
	[ 心大！爷爷奶奶带3个孙子逛超市，离开时#把孙子忘在购物车里# ]
	 18日，浙江杭州，一超市购物车中坐着一名2岁小男孩，在嚎啕大哭。原来，孩子的爷爷奶奶带着3个孙子来买东西，装完东西就带着2个孙子骑电瓶车走了，回家才发现最小的孙子还在购物车里坐着。 L新浪新闻客户端的秒拍视频
===='新浪新闻客户端'====
     [...省略剩下部分...]
```



## 深入定制 model 类

注意到上面有一处重复 :point_right: "#女孩遭猥亵乘客冷眼旁观# 司机拼死抓凶被殴打"。

**先针对爬取过程中的修改，**

对于爬取下来的数据，先判断数据库中是否已经存在再保存：

```python
try:
	_ = Seq2SeqPost.objects.filter(abstract=data_dict["abstract"])
    if not _:
        del _
        raise Seq2SeqPost.DoesNotExist
except Seq2SeqPost.DoesNotExist:
    seq2seqpost = Seq2SeqPost()
    for key in data_dict.keys():
        setattr(seq2seqpost, key, data_dict[key])
        seq2seqpost.save()
else:
    continue

```

line 2 设计详情 :point_right: [为什么使用 `.filter` 而非 `.get`](#为什么使用 `.filter` 而非 `.get`)

**清洗数据 - 删除数据库中重复的数据**

> 对于摘要相同，内容不同 > 内容更新这种情况先忽略(不爬取)。

在当前数据库已经有数据重复的情况下，需要对 `Seq2SeqPost` 类指定它的“比较”方式，让它知道什么样的两个数据是“相等”的，为 `Seq2SeqPost` 类添加如下方法：

```python
class Seq2SeqPost(models.Model):
    [...]

    def __eq__(self, other):
        if not isinstance(other, Seq2SeqPost):
            return NotImplemented
        return str(self.from_id) == str(other.from_id) and \
               self.abstract == other.abstract
```

注意到使用了 `str(self.frome_id)` 这意味着需要为 `Weibo` 类重写 `__str__` 方法：

```python
class Weibo(models.Model):
    [...]

    def __str__(self):
        return self.name
```

在 `python manage.py shell` 中测试：

```python
>>> from weibo.models import Seq2SeqPost, Weibo
>>> 
>>> all_ = Seq2SeqPost.objects.all()
>>> all_[0]
'#女孩遭猥亵乘客冷眼旁观# 司机拼死抓凶被殴打'
>>> all_[0] == all_[1]
False
>>> for each in all_:
        print(all_[0]==each)

True
False
True
False
[...]
False
>>> print("{!r}".format(all_[0])); print("{!r}".format(all_[2]))
'#女孩遭猥亵乘客冷眼旁观# 司机拼死抓凶被殴打'
'#女孩遭猥亵乘客冷眼旁观# 司机拼死抓凶被殴打'

>>> ### 删除数据库中的特定项（重复的项）
>>> obj = all_[2]
>>> obj
'#女孩遭猥亵乘客冷眼旁观# 司机拼死抓凶被殴打'

>>> obj.delete()
(1, {'weibo.Seq2SeqPost': 1})

>>> all_ = Seq2SeqPost.objects.all()
>>> for each in all_:
        for each in all_:

'#女孩遭猥亵乘客冷眼旁观# 司机拼死抓凶被殴打'
'跟风？高校出通知#用华为手机可免费上网#一个月'
'心大！爷爷奶奶带3个孙子...开时#把孙子忘在购物车里#'
'成都#网红烤兔黑作坊加工...责人痛哭道歉：做食品做良心'
[...]
>>> exit
```







## Reference

N/A



### 为什么使用 `.filter` 而非 `.get`

`.get(abstract=data_dict["abstract"])` 如果数据库中已经存在多个相同的 abstract，那么会抛出异常。这样就需要处理两个异常：

```python
>>> _obj = Seq2SeqPost.objects.get(abstract="成都#网红烤兔黑作坊加工后续# 负
...: 责人痛哭道歉：做食品做良心")
---------------------------------------------------------------------------
MultipleObjectsReturned                   Traceback (most recent call last)
<ipython-input-12-cb0a9faaf2e9> in <module>
----> 1 _obj = Seq2SeqPost.objects.get(abstract="成都#网红烤兔黑作坊加工后续# 负责人痛哭道歉：做食品做良心")
[...]
MultipleObjectsReturned: get() returned more than one Seq2SeqPost -- it returned 2!

>>>
```

使用 `.filter` 如果不存在，则返回空的 QuerySet 实例

```python
>>> _ = Seq2SeqPost.objects.filter(abstract="NOT Exist")                    

>>> _                                                                       
<QuerySet []>

>>> if _: print("don't print me")                                           

>>> if not _: print("print me")                                             
print me

```

做了一下判断是否为空，然后做 raise 异常处理：

```python
    if not _:
        del _; raise Seq2SeqPost.DoesNotExist
```

这样就可以捕获这个表示当前数据库中不存在该 post 数据的异常了：

```python
>>> try: 
...:     _ = Seq2SeqPost.objects.filter(abstract="abstract") 
...:     if not _:
...:         del _; raise Seq2SeqPost.DoesNotExist
...: except Seq2SeqPost.DoesNotExist: 
...:     print("do save") 
...:                                                                         
do save

>>> 
```

=== END





