# Start

[TOC]



## command history

### Structure and django setup

```shell
$ mkvirtualenv LearningNLP
(LearningNLP) $ pip -V
...python 3.x.x ....
(LearningNLP) $ python -V
python 3.x.x ....
(LearningNLP) $ pip install django
...
(LearningNLP) $ pip install selenium
...
(LearningNLP) $ mkdir GUI
(LearningNLP) $ mkdir Docs
(LearningNLP) $ cd GUI
(LearningNLP) GUI $ django-admin startproject web
(LearningNLP) GUI $ vim web/web/settings.py
#### set all domian allow  ####
(LearningNLP) GUI $ cd web
(LearningNLP) web $ python manage.py runserver 0.0.0.0:8099
...
Quit the server with CONTROL-C.
^C(LearningNLP) web $
(LearningNLP) web $ cd ../../
(LearningNLP) $ pip freeze > requirements.txt
(LearningNLP) $ ### commit here ###
```



### Crawler Develop

```shell
(LearningNLP) $ mkdir Crawler
(LearningNLP) $ cd Crawler
(LearningNLP) Crawler $ mkdir sites
(LearningNLP) Crawler $ mkdir concurrency
(LearningNLP) Crawler $ touch concurrency/threads.py
(LearningNLP) Crawler $ 
(LearningNLP) Crawler $ mkdir -p sites/weibo
(LearningNLP) Crawler $ touch sites/weibo/parse.py
(LearningNLP) Crawler $ touch sites/weibo/request.py
(LearningNLP) Crawler $ 
(LearningNLP) Crawler $ touch crawler.py
(LearningNLP) Crawler $ 
### coding crawler.py ###
(LearningNLP) Crawler $ python ./crawler.py
[2018-12-11 22:49:01,372]INFO     ## worker-Wiadeul ## command: debug_producer; data: 1.
[2018-12-11 22:49:01,373]ERROR    ## worker-Wiadeul ## debug producer with data: 1
[2018-12-11 22:49:06,377]INFO     ## worker-Wiadeul ## command: debug_producer; data: 2.
[2018-12-11 22:49:06,378]ERROR    ## worker-Wiadeul ## debug producer with data: 2
^C[2018-12-11 22:49:07,351]INFO     ## worker-Wiadeul ## command: stop; data: None.
[2018-12-11 22:49:07,352]WARNING  ## worker-Wiadeul ## STOP!
[2018-12-11 22:49:07,353]INFO     main thread quit!
(LearningNLP) Crawler $ 
(LearningNLP) Crawler $ ### git commit here ###
```





