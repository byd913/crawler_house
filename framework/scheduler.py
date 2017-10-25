# -*- coding: utf-8 -*-
# @Time    : 2017/6/29 10:00
# @Author  : baiyoudong
# @File    : scheduler.py
import logging
import os
from logging.handlers import TimedRotatingFileHandler
import time

import sys

from watcher import Watcher
from crawler import se_rent_crawler
from proxy import xici_proxy


def init_log():
    """
    initial logging module
    :rtype: None
    """
    if not os.path.exists('log'):
        os.makedirs('log')

    server_log = logging.getLogger('server')
    rotating_handler = TimedRotatingFileHandler(filename='log/mission.log', when='midnight')
    formatter = logging.Formatter(
        '%(levelname)s\t%(asctime)s\t[%(thread)d]\t[%(filename)s:%(lineno)d]\t%(message)s')
    rotating_handler.setFormatter(formatter)
    rotating_handler.suffix = 'log.%Y-%m-%d-%H'
    server_log.addHandler(rotating_handler)

    stdout_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(levelname)s\t%(asctime)s\t[%(thread)d]\t[%(filename)s:%(lineno)d]\t%(message)s')
    stdout_handler.setFormatter(formatter)
    server_log.addHandler(stdout_handler)

    server_log.setLevel(logging.INFO)


init_log()

if __name__ == '__main__':
    watcher = Watcher()

    proxy = xici_proxy.XiCiProxy()
    proxy.start()

    while True:
        crawler = se_rent_crawler.SERentCrawler('北京', proxy)
        crawler.start()
        time.sleep(60)
