# -*- coding: utf-8 -*-
# @Time    : 2017/6/29 20:35
# @Author  : baiyoudong
# @File    : se_es_crawler.py
import logging
import re

from BeautifulSoup import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

from model.rent_house import RentHouse
from model.rent_house import Session
from util import http_client


class SEESCrawler:
    def __init__(self, city_, proxy_=None):
        self.executor = ThreadPoolExecutor()
        self.city = city_
        self.proxy = proxy_
        self.client = http_client.HttpClient(self.proxy, 6)

    def start(self):
        logging.getLogger('server').info('start crawling...')
        for page in range(71):
            page_url = 'http://bj.58.com/ershoufang/0/pn%d/' % page
            self.parse_list_page(page_url)
            # self.executor.submit(SECrawler.parse_list_page, self, page_url)

        logging.getLogger('server').info('crawl finish')

    def parse_list_page(self, page_url):
        content = self.client.get_content(page_url)
        if not content:
            return

        soup = BeautifulSoup(content)
        # next_page_url = None
        # next_page_list = soup.findAll('a', {'class': 'next'})
        # for page in next_page_list:
        #     next_page_url = page.get('href')
        #     break

        house_list = soup.findAll('div', {'class': 'list-info'})
        for house in house_list:
            house_url = house.h2.a.get('href')
            self.executor.submit(SEESCrawler.parse_house_page, self, house_url)

    def parse_house_page(self, house_url):
        content = self.client.get_content(house_url)
        if not content:
            return

        soup = BeautifulSoup(content)
        rent_house = RentHouse()
        rent_house.title = soup.html.head.title.string.strip()
        rent_house.source = 1  # 1:58
        rent_house.url = house_url
        rent_house.city = self.city

        price_list = soup.findAll('div', {'class': 'house-pay-way f16'})
        rent_house.price = int(price_list[0].findAll('b', {'class': 'f36'})[0].string)

        info_list = soup.find('ul', {'class': 'f14'}).findAll('li')
        for info in info_list:
            if str(info).find('租赁方式') != -1:
                rent_house.rent_type = info.findAll('span')[1].string
            elif str(info).find('房屋类型') != -1:
                rent_house.house_type = info.findAll('span')[1].string
            elif str(info).find('所在小区') != -1:
                rent_house.house_name = info.findAll('span')[1].a.string
        time_pattern = '\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
        rent_house.update_time = re.search(time_pattern,
                                           str(soup.find('p', {'class': 'house-update-info c_888 f12'}))).group(0)
        rent_house.description = '.'.join(soup.find('ul', {'class': 'introduce-item'}).findAll(text=True)).replace(
            '&nbsp', '')

        # db_session = Session()
        # try:
        #     db_session.add(rent_house)
        #     db_session.flush()
        #     db_session.commit()
        # except Exception, e:
        #     pass
        # else:
        #     logging.getLogger('server').info('finish [%s]' % rent_house.url)
        # finally:
        #     db_session.close()

if __name__ == '__main__':
    crawler = SEESCrawler('北京')
    crawler.parse_list_page('http://bj.58.com/ershoufang/pn5')
