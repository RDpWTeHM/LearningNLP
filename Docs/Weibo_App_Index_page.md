# Index Page of Weibo Application



## *Overview*

[TOC]



## 创建 Index 页面模板

新建 `GUI/web/weibo/templates/weibo/` 文件夹。

创建 `.../templates/weibo/index.html` 文件。

```html
{# web/weibo/templates/weibo/index.html #}
<!DOCTYPE html>
<html lang="en">
<head>
</head>
<body>
    <h1>Weibo IDs list</h1>
</body>
</html>
```

修改 `urls.py` :

```python
@@ -6,7 +6,7 @@ from . import views
 
 
 urlpatterns = [
-    path("", lambda request: HttpResponse("<h1>Hello Weibo App</h1>")),
+    path("", views.index, name="index"),
 
     path("crawler/", views.crawler, name="crawler"),
     path("test_crawler/", views.test_crawler, name="test_crawler"),
```

修改 `views.py`:

```python
from .models import Weibo, Seq2SeqPost

def index(request):
    return render(request, "weibo/index.html",
                  {}, )
```

浏览器刷新 http://localhost:8000/weibo/ 页面查看。

## 使用 bootstrap 以及渲染模板

### 引入 bootstrap 支持

```html
{# web/weibo/templates/weibo/index.html #}
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

	<link rel="stylesheet" media="screen"
		  href="https://cdn.bootcss.com/bootstrap/4.0.0/css/bootstrap.min.css"
    	  integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
		  crossorigin="anonymous">

	<script src="https://cdn.bootcss.com/jquery/3.2.1/jquery.slim.min.js"
	        integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
	        crossorigin="anonymous"></script>
	<script src="https://cdn.bootcss.com/popper.js/1.12.9/umd/popper.min.js"
	        integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q"
	        crossorigin="anonymous"></script>
	<script src="https://cdn.bootcss.com/bootstrap/4.0.0/js/bootstrap.min.js"
	        integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
	        crossorigin="anonymous"></script>

	<title>IDs list on DB | Weibo</title>
</head>
<body>
    [...]
```

上文 source 文件引入参考自 [Bootstrap4中文文档 :link:](https://v4.bootcss.com/)

### django 模板系统

line 20~25

```html
[...]
</head>
<body>
	<div class="container">
	<div class="row">
		<div class="col-md-12 push-md-4">
		<div class="text-center">
		<h1>Weibo IDs list</h1>
		</div></div>
	</div>
	<div class="row">
		<div class="col-md-12 push-md-4">
		<table name="id_list_table" id='id_list_table'
		       class="table table-hover">
		    <thead>
			<tr><th>DB index</th>
				<th>Weibo Name</th><th>Action</th></tr>
			</thead>
			<tbody>
		{% for each_weibo in weibo_all_objects %}
			<tr><th scope="row">[put here]</th>
				<td>{{ each_weibo.weiboID }}</td>
				<td><input type="button" class="btn btn-primary" 
					       name="crawler" value="Crawl"></td></tr>
		{% endfor %}
			</tbody>
		</table>
		</div>
	</div>
</body>
</html>
```

### `views.index` 渲染模板

```python
def index(request):
    return render(request, "weibo/index.html",
                  {'weibo_all_objects': Weibo.objects.all(), }, )
```

> 注意，如果 `Weibo` 数据库表中没有数据，则本处会有异常产生。
>
> 可以使用 `http://localhost:8000/weibo/test_crawler/` 这个 路径跑一下，爬取一次数据。后期修复了这个 bug，已经完善首页和爬取机制后，这个 url 会被删除。
>
> > 如果原本数据库 Weibo 表为空，使用上述路径跑了一下爬虫。则 Weibo表的 name 字段为空。因为目前该方法没有爬取该 ID 对应的微博网名。因此 `webo/` 的 index 页面 name 字段会为空。可以在 `python manage.py shell` 中手动修改。



## Reference

N/A

