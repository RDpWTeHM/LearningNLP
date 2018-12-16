#!/usr/bin/env python
import os
import sys


def learningNLP_customer():
    import threading
    t = threading.Thread(target=manage_selenum)
    t.setDaemon(True)
    t.start()
    del t


def manage_selenum():
    from time import sleep
    from time import ctime
    while True:
        print("{} manage_selenum".format(ctime()), file=sys.stderr)
        sleep(5)


def Is_child_processing():
    import re
    re_result = re.findall(
        "{}".format(os.getpid()),
        os.popen("ps -ejf | grep {} | grep -v \"grep\"".format(os.getpid())).read()
        )
    ret = True if len(re_result) == 1 else False
    return ret


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

    if Is_child_processing():
        learningNLP_customer()

    execute_from_command_line(sys.argv)
