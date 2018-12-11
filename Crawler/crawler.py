#!/usr/bin/env python3

"""crawler.py
Author: Joseph Lin
E-mail: joseph.lin@aliyun.com
Social:
  https://github.com/RDpWTeHM
  https://blog.csdn.net/qq_29757283

Usage: $ python ./crawler.py

TODO:
  N/A

Note:
  N/A
"""
import os
import sys
import time

import logging

import signal
import atexit

import traceback

try:
    from selenium import webdriver
except ImportError as exc:
    raise ImportError(
        "Couldn't import selenium. Are you sure it's installed and "
        "available on your PYTHONPATH environment variable? Did you "
        "forget to activate a virtual environment?"
    ) from exc
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.common.exceptions import WebDriverException

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


# import threading
from threading import Thread
import queue


Q_TODO = queue.Queue()


def request_work(command, data=None):
    Q_TODO.put((command, data))


def producer():
    _debug_times = 0
    while True:
        time.sleep(5)
        _debug_times += 1
        request_work("debug_producer", data=_debug_times)


def worker(thr_name):
    while True:
        command, data = Q_TODO.get()  # block method
        logging.info("## worker-{} ## command: {}; data: {}.".format(thr_name, command, data))
        if command == 'stop':
            logging.warning("## worker-{} ## STOP!".format(thr_name))
            break
        elif command == "debug_producer":
            logging.error("## worker-{} ## debug producer with data: {}".format(thr_name, data))
        else:
            logging.warning("## worker-{} ## unsupport command!".format(thr_name))


def main():
    thrs = []

    t = Thread(target=producer,
               args=(), )
    t.setDaemon(True)
    t.start()
    del t

    t = Thread(target=worker,
               args=("Wiadeul", ), )
    t.setDaemon(False)
    thrs.append(t)
    del t

    for thr in thrs:
        thr.start()

    ''' main thread can't quit earlier
      due to register SIGTERM function is work on main thread
    '''
    for thr in thrs:
        thr.join()

    logging.info("main thread quit!")


if __name__ == "__main__":
    #
    # logging
    #
    logging.basicConfig(
        # filename=N/A,
        level=logging.INFO,
        # level=logging.WARNING,
        format='[%(asctime)s]%(levelname)-9s%(message)s',
    )

    def sigterm_handler(signo, frame):
        request_work("stop")

    signal.signal(signal.SIGTERM, sigterm_handler)
    signal.signal(signal.SIGINT, sigterm_handler)

    main()
