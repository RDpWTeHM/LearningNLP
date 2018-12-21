#!/usr/bin/env python
import os
import sys


def learningNLP_customer(argv):
    #
    # package path
    #
    try:
        _cwd = os.getcwd()
        _proj_abs_path = _cwd[0:_cwd.find("GUI")]
        _package_path = os.path.join(_proj_abs_path, "Crawler")
        if _package_path not in sys.path:
            sys.path.append(_package_path)

        #
        # Not: /home/joseph/Devl/LearningNLP/GUI/web/
        #      $ python manage.py runserver
        # But: /<any>/<path>/
        #      $ python /home/joseph/Devl/LearningNLP/GUI/web/manage.py runserver
        #               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #                /\ or use "../../"  relative path
        # will cause issue
    except Exception:
        return  # -[o] fix later by using argv

    #
    # structure
    #
    import handler_crawler as hc  # reference "package path" part
    import threading
    t = threading.Thread(target=hc.manage_selenum)
    t.setDaemon(True)
    t.start()
    del t


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
        learningNLP_customer(sys.argv)

    execute_from_command_line(sys.argv)
