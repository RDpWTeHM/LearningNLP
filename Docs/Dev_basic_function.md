# Develop Basic Function



## django server Customization

### 从 `manage.py` 入手

#### 分析

django server 启动了两个 processing，一个是总管理，子进程在开发过程中，代码有更新即重启该子进程。

```shell
(LearningNLP) web $ python manage.py runserver
...
Ctrl+Z
(LearningNLP) web $ ps -ejf | grep manage.py
## UID     PID  PPID  PGID   SID  C STIME TTY          TIME CMD ##
joseph    9678  6200  9678  6200 11 23:55 pts/1    00:00:01 \
python ./manage.py runserver 0.0.0.0:8000
joseph    9680  9678  9678  6200 18 23:55 pts/1    00:00:01 \
<.virtualenvs>/<path>/<to>/python ./manage.py runserver 0.0.0.0:8000
## 上面的长行已经手动换行过了 ##
(LearningNLP) web $ 
```

子进程的 PID 在 `ps -ejf` 的结果中只会存在一个，如 9680。

而父进程的 PID 会存在两个，如 9678。

#### Code

以加入一个 daemon 线程为例：

>  daemon 线程意味着主线程和所有非 daemon 线程退出，则该线程也随之关闭，从而关闭进程；
>
> 同时这意味着，非 daemon 线程在 主线程退出后，程序也不会退出，直到所有的非 daemon 进程退出后，进程才关闭。
>
>  
>
> 另，该 daemon 线程加在子进程中，因为是子进程未来将要使用该线程中的资源。

判断当前进程是否为子进程：

```python
def Is_child_processing():
    import re
    re_result = re.findall(
        "{}".format(os.getpid()),
        os.popen("ps -ejf | grep {} | grep -v \"grep\"".format(os.getpid())).read()
        )
    ret = True if len(re_result) == 1 else False
    return ret
```



一个死循环运行打印消息的函数（大多数情况下，线程即函数）：

```python
def manage_selenum():
    from time import sleep
    from time import ctime
    while True:
        print("{} manage_selenum".format(ctime()), file=sys.stderr)
        sleep(5)
```



以线程形式启动该函数的代码：

```python
def learningNLP_customer():
    import threading
    t = threading.Thread(target=manage_selenum)
    t.setDaemon(True)  # 确保目前按 Ctrl+C 能够使程序退出
    t.start()
    del t
```



加入该线程到子进程中：

```python
#### GUI/web/manage.py
[...]

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    if Is_child_processing(): learningNLP_customer()

    execute_from_command_line(sys.argv)
```

在 `if __name__ == '__main__':` 下增加了如上 line 15 的代码。

#### 运行效果

```shell
(LearningNLP) web $ ./manage.py runserver 0.0.0.0:8000
Sun Dec 16 17:25:35 2018 manage_selenum
Performing system checks...

System check identified no issues (0 silenced).
[...]
December 16, 2018 - 17:25:36
Django version 2.1.4, using settings 'web.settings'
Starting development server at http://0.0.0.0:8067/
Quit the server with CONTROL-C.
Sun Dec 16 17:25:40 2018 manage_selenum
Sun Dec 16 17:25:45 2018 manage_selenum
^C(LearningNLP) web $ 
```



