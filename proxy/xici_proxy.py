# -*- coding: utf-8 -*-
# @Time    : 2017/6/26 18:28
# @Author  : baiyoudong
# @File    : xici_proxy.py

import os
import re
import threading
import time
from random import Random

import requests
from BeautifulSoup import BeautifulSoup

from proxy import Proxy
from util import header
from util import rw_lock


class XiCiProxy(Proxy):
    def __init__(self):
        Proxy.__init__(self)
        self.start_url = 'http://api.xicidaili.com/free2016.txt'
        self.http_proxy_list = []
        self.https_proxy_list = []
        self.lock = rw_lock.RWLock()
        self.running = False
        self.random = Random()
        self.update_cycle = 5 * 60  # 20 minutes update ip pool
        self.validate_cycle = 4 * 40
        self.validate_url = 'http://www.baidu.com'
        self.persist_http = 'http_proxy.txt'
        self.persist_https = 'https_proxy.txt'

    def start(self):
        self.running = True
        update_thread = threading.Thread(target=XiCiProxy.update, args=(self,))
        update_thread.start()

        self.load_persist_proxy()

    def update(self):
        while self.running:
            new_http_list = []
            new_https_list = []
            for i in range(1, 10):
                http_list, https_list = self.parse_proxy_list('http://www.xicidaili.com/nn/%d' % i)
                new_http_list.extend(http_list)
                new_https_list.extend(https_list)
                time.sleep(60)

            self.lock.write_acquire()
            if len(new_http_list) > 0:
                self.http_proxy_list = new_http_list
            if len(new_https_list) > 0:
                self.https_proxy_list = new_https_list
            self.lock.write_release()
            self.save_persist_proxy()
            time.sleep(self.update_cycle)

    def save_persist_proxy(self):
        http_fp = open(self.persist_http, 'w')
        https_fp = open(self.persist_https, 'w')
        for proxy in self.http_proxy_list:
            http_fp.write('%s\n' % proxy)
        for proxy in self.https_proxy_list:
            https_fp.write('%s\n' % proxy)
        http_fp.flush()
        https_fp.flush()
        http_fp.close()
        https_fp.close()

    def load_persist_proxy(self):
        try:
            http_fp = open(self.persist_http, 'r')
            https_fp = open(self.persist_https, 'r')
            for line in http_fp:
                self.http_proxy_list.append(line[-1])
            for line in https_fp:
                self.https_proxy_list.append(line[-1])
            http_fp.close()
            https_fp.close()
        except IOError:
            pass

    @staticmethod
    def parse_proxy_list(url):
        temp_filename = '/tmp/temp.html'
        os.system('wget -q --timeout=10 "%s" -O %s' % (url, temp_filename))
        content = open(temp_filename).read()
        soup = BeautifulSoup(content)
        item_list = soup.findAll('tr', {'class': 'odd'})

        http_list = []
        https_list = []
        for item in item_list:
            td_list = item.findAll('td')
            m = re.search('width:(\d+)', str(td_list[6]))
            if not m:
                continue
            if int(m.group(1)) <= 80:
                continue
            ip = td_list[1].getText()
            port = td_list[2].getText()
            http_type = td_list[5].getText()
            if http_type == 'HTTP':
                http_list.append('%s:%s' % (ip, port))
            elif http_type == 'HTTPS':
                https_list.append('%s:%s' % (ip, port))
        return http_list, https_list

    def validate(self, ip):
        header.HEADER['User-Agent'] = self.random.choice(header.USER_AGENTS)
        proxy = {'http': 'http://%s' % ip}
        try:
            content = requests.get(self.validate_url, proxies=proxy, headers=header.HEADER, timeout=20).text
            if not content:
                return False
        except Exception, e:
            return False
        return True

    def get_random_http_proxy(self):
        self.lock.read_acquire()
        proxy = self.random.choice(self.http_proxy_list)
        self.lock.read_release()
        return proxy

    def get_random_https_proxy(self):
        self.lock.read_acquire()
        print self.https_proxy_list
        proxy = self.random.choice(self.https_proxy_list)
        self.lock.read_release()
        return proxy

    def stop(self):
        self.running = False


if __name__ == '__main__':
    cur_proxy = XiCiProxy()
    cur_proxy.start()
    print len(cur_proxy.http_proxy_list)
    print len(cur_proxy.https_proxy_list)
    # print cur_proxy.get_random_http_proxy()
    # print cur_proxy.get_random_https_proxy()
