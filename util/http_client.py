# -*- coding: utf-8 -*-
# @Time    : 2017/6/29 10:23
# @Author  : baiyoudong
# @File    : http_client.py
from random import Random

import requests

import header


class HttpClient:
    def __init__(self, proxy_=None, max_retry_=3):
        self.proxy = proxy_
        self.max_retry = max_retry_

    def get_content(self, url):
        content = None
        for i in range(self.max_retry):
            try:
                header.HEADER['User-Agent'] = Random().choice(header.USER_AGENTS)
                if self.proxy:
                    proxy_ip = {'http': 'http://%s' % self.proxy.get_random_http_proxy()}
                    content = requests.get(url=url, headers=header.HEADER, proxies=proxy_ip, timeout=10).text
                else:
                    content = requests.get(url=url, headers=header.HEADER, timeout=10).text
            except Exception, e:
                pass
            else:
                break
        return content

