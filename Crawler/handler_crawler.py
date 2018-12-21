"""LearningNLP/Crawler/handler_crawler.py

TODO:

"""
import sys
import os

# import time
# from time import sleep
# from time import ctime

from threading import Thread
# import threading
# from queue import Queue

#
# package path
# -[o] update later
#
try:
    _cwd = os.getcwd()
    _proj_abs_path = _cwd[0:_cwd.find("GUI")]
except Exception:
    try:
        _proj_abs_path = _cwd[0:_cwd.find("Crawler")]
    except Exception as err:
        print("append Crawler to sys.path fail", err, file=sys.stderr)
        sys.exit(1)  # fix later by using argv

_package_path = os.path.join(_proj_abs_path, "Crawler")
if _package_path not in sys.path:
    sys.path.append(_package_path)

try:
    import resource_manage  # reference "package path" part
except Exception as err:
    print("import resource_manage Error", err, file=sys.stderr)
    sys.exit(1)

# from selenium.common.exceptions import TimeoutException, NoSuchElementException


#
# manage.py run this as daemon-thread
#
def manage_selenum():
    res = resource_manage.Resource()
    t = Thread(target=res.manage)
    t.setDaemon(True)
    t.start()
    del t
