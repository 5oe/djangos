# -*- coding: utf-8 -*-
import scrapy
from scrapy import  cmdline
from scrapy import conf
from scrapy.conf import settings
import os
from scrapy.http.request import Request

class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['douban.com']
    start_urls = ['http://douban.com/']

    def start_requests(self):
        import os
        print(os.environ.get('SCRAPY_PROJECT'), '***')
        yield Request(url='http://douban.com/')

    def parse(self, response):
        print('*****')
