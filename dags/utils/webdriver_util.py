# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Erik Rivera

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
from inspect import stack
from os.path import join
from time import time

import requests

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait


class ElementCSSSelector:
    def __init__(self, d):
        self.d = d

    def get(self, selector):
        return self.d.find_element_by_css_selector(selector)

    def get_and_clear(self, selector):
        elem = self.get(selector)
        elem.clear()
        return elem


class Waiter:
    """
    A wrapper around WebDriverWait. It prints messages before the call and take
    a screenshot afterward. It also adds a few convenient functions.
    """

    def __init__(self, d, screenshot_dir, default_timeout):
        self.d = d
        self.shot_id = 0
        self.shot_dir = screenshot_dir
        self.default_timeout = default_timeout

        if not os.path.isdir(self.shot_dir):
            os.makedirs(self.shot_dir)

    def until(self, method, message='', timeout=-1, caller_frame=2):
        if timeout < 0:
            timeout = self.default_timeout
        self._wrapper(method, message, timeout, caller_frame,
                      lambda mthd, msg: WebDriverWait(self.d, timeout).until(mthd, msg))

    def until_display(self, selector, timeout=-1):
        """
        For some reason EC.visibility_of throws exceptions. Hence this method.
        """
        self.until(ec_element_to_be_displayed(selector), timeout=timeout, caller_frame=3)

    def _wrapper(self, method, message, timeout, caller_frame, func):
        caller = stack()[caller_frame][3]
        print("Waiting in {}(), timeout {} secs...".format(caller, timeout))
        start = time()
        try:
            func(method, message)
            print("Spent {0:.3f} secs".format(time() - start))
            self.shoot(caller)
        except TimeoutException as e:
            print('timeout-exception')
            self.shoot('timeout-exception')
            raise e

    def shoot(self, base_file_name):
        """
        Save a screenshot at {screenshot_out_dir}/N-{base_file_name}.png,
        where N is an incrementing integer ID.
        """
        path = join(self.shot_dir, '{}-{}.png'.format(self.shot_id,
                                                      base_file_name))
        print("Screenshot saved at {}".format(path))
        self.d.save_screenshot(path)
        self.shot_id += 1


def ec_element_to_be_displayed(selector):
    def ec(d):
        return ElementCSSSelector(d).get(selector).value_of_css_property('display') != 'none'
    return ec


def init(default_timeout=10, folder='/tmp/'):

    # download_path = os.path.join(os.getcwd(), 'download')
    download_path = os.path.join('/sel', 'download')
    folder = os.path.join('/sel')
    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    fp.set_preference("browser.download.panel.shown", False)
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk",
                      "text/csv, application/vnd.ms-excel, application/octet-stream, application/pdf, application/xls, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    fp.set_preference("browser.download.dir", download_path)
    driver = webdriver.Firefox(firefox_profile=fp)
    waiter = Waiter(driver, folder, default_timeout)
    selector = ElementCSSSelector(driver)
    return driver, waiter, selector, download_path


def wait_and_get(driver, url):
    """
    Wait until the given URL is accessible (returns 2xx or 3xx),
    and then call driver.get(url)
    """
    print("Waiting for {} readiness...".format(url))
    while True:
        # noinspection PyBroadException
        try:
            r = requests.get(url, timeout=3)
            r.raise_for_status()
            break
        except Exception as e:
            print(str(e))
            print("Contina esperando...")

    print("Interactuando con {}...".format(url))
    driver.get(url)
