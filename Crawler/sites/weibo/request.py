#!/usr/bin/env python3
"""sites/weibo/request.py

N/A
"""
import sys
import os
from functools import wraps

import time

from selenium.common.exceptions import WebDriverException

from selenium.common.exceptions import TimeoutException, NoSuchElementException

from threading import Thread
from queue import Queue
import queue

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


# class WeiboSpider(Thread):
class WeiboSpider():

    def __init__(self, target_id=None):
        self.qdata = Queue()
        self.id = target_id
        # self.l_test_comsumer = None

    def run(self, out_q, weibo_account_id=None):
        if weibo_account_id:
            self.id = weibo_account_id
        elif not self.id:
            raise RuntimeError("Must indicate weibo account id!")

        import resource_manage  # Reference to > "package path" part
        res = resource_manage.Resource()
        if __debug__:
            print("check Singleton> id(res): {}".format(id(res)),
                  file=sys.stderr)
        browser = None
        try:
            browser = res.acquire_browser_handler_by_create()
        except Exception:  # -[o] not decide yet
            browser = res.acquire_browser_handler_from_queue()
        if not browser:
            raise RuntimeError("Can not acquire browser resource")

        browser.get(self.id)
        time.sleep(10)  # -[o] update code later
        while True:
            try:
                data = None

                contents_list = browser.find_elements_by_xpath(
                    "//div[@class='WB_text W_f14']")
                contents = [content.text for content in contents_list]
                for content in contents:
                    # if __debug__:
                    #    print(content, file=sys.stderr)
                    data = content
                    out_q.put(data)

                # scroll down to load more data!
                raise RuntimeError("no more data")
            except RuntimeError as err:
                print("[Debug] WeiboSpider> run> ", err, file=sys.stderr)
                break
            except Exception:  # -[o] pending...
                out_q.put(Exception)
                break
        browser.execute_script("window.stop();")
        res.release_browser_handler(browser)
        del browser

    def consumer(self, in_q):
        while True:
            try:
                data = in_q.get(timeout=3)  # -[o] temp solution
                yield data
            except queue.Empty:
                break
            except Exception as err:
                import traceback; traceback.print_exc();
        return


def main():
    demo()


def demo():
    from selenium import webdriver
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

    url = "https://www.weibo.com/58371?topnav=1&wvr=6&topsug=1"

    def get_browser_handler():
        '''
         start browser
        '''
        capa = DesiredCapabilities().CHROME
        capa["pageLoadStrategy"] = "none"
        from selenium.webdriver.chrome.options import Options
        croptions = Options()
        __string, = ("user-agent=Mozilla/5.0 "
                     "(Windows NT 10.0; Win64; x64) "
                     "AppleWebKit/537.36 (KHTML, like Geoko) "
                     "Chrome/70.0.3538.102 Safari/537.36", )
        croptions.add_argument(__string)

        browser = webdriver.Chrome(
            executable_path="/usr/lib/chromium-browser/chromedriver",
            desired_capabilities=capa,
            chrome_options=croptions, )
        return browser

    browser = get_browser_handler()
    browser.get(url)
    time.sleep(20)

    contents_list = browser.find_elements_by_xpath("//div[@class='WB_text W_f14']")

    contents = [content.text for content in contents_list]
    print(contents)


if __name__ == '__main__':
    main()
