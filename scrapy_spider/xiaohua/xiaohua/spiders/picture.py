# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector, HtmlXPathSelector
from scrapy.http import Request
import hashlib
from xiaohua.items import *


class PictureSpider(scrapy.Spider):
    name = 'picture'
    allowed_domains = ['521609.com']
    start_urls = ['http://www.521609.com/meinvxiaohua/']
    url_set = set()

    def parse(self, response):
        # 下载所有图片
        li_obj = Selector(response=response).xpath('//div[@class="index_img list_center"]/ul/li')
        for li in li_obj:
            alt = li.xpath('.//img/@alt').extract_first()
            src = li.xpath('.//img/@src').extract_first()
            yield XiaohuaItem(alt=alt, src=src)

        # 获取页码
        page_obj = Selector(response=response).xpath('//div[@class="listpage"]//a')
        for page in page_obj:
            url = page.xpath('./@href').extract_first()
            s = self.md5(url)
            if s in self.url_set:
                pass
            else:
                self.url_set.add(s)
                url = 'http://www.521609.com/meinvxiaohua/%s' % url
                yield Request(url=url, callback=self.parse)

    def md5(self, url):
        m = hashlib.md5()
        m.update(url.encode('utf8'))
        return m.hexdigest()
