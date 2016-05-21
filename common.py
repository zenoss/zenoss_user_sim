import time
from collections import defaultdict

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class assertPage(object):
    def __init__(self, title):
        self.title = title

    def __call__(self, f):
        def wrapper(*args, **kwargs):
            assert self.title in args[0].title, \
                '{}() is called on the wrong page, {}.'.format(
                    f.__name__, self.title)
            return f(*args, **kwargs)

        return wrapper

class assertPageAfter(object):
    def __init__(self, title):
        self.title = title

    def __call__(self, f):
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)
            assert self.title in args[0].title, \
                'calling {}() moved to the wrong page, {}.'.format(
                    f.__name__, args[0].title)
            return result
        return wrapper

def find(d, selector):
    return d.find_element_by_css_selector(selector)

def findMany(d, selector):
    return d.find_elements_by_css_selector(selector)

def findIn(el, selector):
    return el.find_element_by_css_selector(selector)

def merge(d1, d2):
    """Merge two dictionaries. The latter argument overwrites the former."""
    result = d1.copy()
    result.update(d2)
    return result

class Result(object):
    def __init__(self, name):
        self.name = name
        self.success = True
        self.stat = {}
        self.data = {}

    def putStat(self, k, v):
        k = '.'.join([self.name, k])
        self.stat[k] = v

    def putData(self, k, v):
        k = '.'.join([self.name, k])
        self.data[k] = v

class WorkflowResult(Result):
    def __init__(self, name):
        Result.__init__(self, name)
        self.failedTask = None

    def putTaskResult(self, result):
        if not result.success:
            self.failedTask = result.name
        self.success *= result.success
        self.stat.update(result.stat)
        self.data.update(result.data)


