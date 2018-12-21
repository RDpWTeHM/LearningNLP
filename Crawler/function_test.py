#!/usr/bin/evn python3

"""Crawler/function_test.py

Usage:
  (LearningNLP) Crawler $ python -O function_test.py
"""
import sys
import os
from time import sleep

from threading import Thread

sys.path.append(os.getcwd())

import handler_crawler as hc
import sites.weibo.request as cweibo


def main():
    hc.manage_selenum()

    test_weibo_id = "https://www.weibo.com/58371?topnav=1&wvr=6&topsug=1"
    test_weibo = cweibo.WeiboSpider(test_weibo_id)
    t = Thread(target=test_weibo.run, args=(test_weibo.qdata, ))
    t.setDaemon(True)
    t.start()
    del t

    sleep(50)  # wait test_weibo.run loading browser

    for post in test_weibo.consumer(test_weibo.qdata):
        print(post, file=sys.stderr)
        sleep(1)


if __name__ == '__main__':
    main()
