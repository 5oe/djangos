# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.join(BASE_DIR, 'pic')


class XiaohuaPipeline(object):
    def process_item(self, item, spider):
        # if spider.name='picture'
        src = item['src']
        alt = item['alt']
        file_name = alt + '.jpg'
        file_path = os.path.join(BASE_DIR, file_name)
        url = 'http://www.521609.com/meinvxiaohua/%s' % src
        response = requests.get(url=url)
        print(src, alt, file_path)
        with open(file_path, 'wb') as f:
            f.write(response.content)
