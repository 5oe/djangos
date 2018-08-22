# # -*- coding: utf-8 -*-
# import scrapy
#
# from scrapy.spiders import CrawlSpider, Rule
#
#
# class ImdbSpider(scrapy.Spider):
#     name = 'imdb'
#     allowed_domains = ['imdb.cn']
#     start_urls = ['http://www.imdb.cn/nowplaying/1']
#
#     #   一般爬虫的逻辑是：给定起始页面，发起访问，分析页面包含的所有其他链接，
#     # 然后将这些链接放入队列，再逐次访问这些队列，直至边界条件结束。
#     # 为了针对列表页+详情页这种模式，需要对链接抽取（link extractor）的逻辑进行限定。
#     # 好在scrapy已经提供，关键是你知道这个接口，并灵活运用
#     def parse(self, response):
#         pass
#
#     def start_requests(self):
#         pass
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from moive_evaluate.items import MoiveEvaluateItem


# 这个Rule啊其实就是为了爬取全站内容的写法，首先我们继承的就不是scrapy.spider类了，而是继承CrawlSpider这个类，看源码就回明白CrawlSpider这个类也是继承scrapy.spider类。
#
# 　　具体参数：
#
# 　　allow：这里用的是re过滤，我们其实就是start_urls加上我们这个匹配到的具体链接下的内容。 　  LinkExtractor：故名思议就是链接的筛选器，首先筛选出来我们需要爬取的链接。
#
# 　　deny：这个参数跟上面的参数刚好想反，定义我们不想爬取的链接。
#
# 　　follow：默认是false，爬取和start_url符合的url。如果是True的话，就是爬取页面内容所有的以start_urls开头的url。
#
# 　　restrict_xpaths：使用xpath表达式，和allow共同作用过滤链接。还有一个类似的restrict_css
#
# 　　callback：定义我们拿到可以爬取到的url后，要执行的方法，并传入每个链接的response内容（也就是网页内容）
#
# 　　注意：rule无论有无callback，都由同一个_parse_response函数处理，只不过他会判断是否有follow和callback



# 显示可用的模板              scrapy genspider -l
# 利用crawlspider创建的框架  scrapy genspider -t crawl weisun sohu.com
# 开始爬取                   scrapy crawl weisun --nolog

class WeisunSpider(CrawlSpider):
    name = 'sohu'
    allowed_domains = ['sohu.com']
    start_urls = ['http://sohu.com/']

    rules = (
        # 新闻网页的url地址类似于：
        # “http://news.sohu.com/20160926/n469167364.shtml”
        # 所以可以得到提取的正则表达式为'.*?/n.*?shtml’
        Rule(LinkExtractor(allow=('.*?/n.*?shtml'), allow_domains=('sohu.com')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = MoiveEvaluateItem()
        # i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # 根据Xpath表达式提取新闻网页中的标题
        i["name"] = response.xpath("/html/head/title/text()").extract()
        # 根据Xpath表达式提取当前新闻网页的链接
        i["link"] = response.xpath("//link[@rel='canonical']/@href").extract()
        yield i


n = 0


class imdbSpider(CrawlSpider):
    name = 'imdb'
    allowed_domains = ['imdb.cn']
    start_urls = ('http://www.imdb.cn/nowplaying/%s' % i for i in range(1, 14624))
    rules = (
        Rule(LinkExtractor(allow=r"/title/tt\d+$"), callback="parse_imdb", follow=True),
    )

    def parse_imdb(self, response):
        global n
        n += 1
        print(n)
        item = MoiveEvaluateItem()
        item['link'] = response.url
        item['name'] = response.xpath('//div[@class="hdd"]/h3/text()').re('([\u4e00-\u9fa5]+|a-zA-Z+)(.*)')
        print(item['name'])


# from scrapy.http.request import Request
#
# n = 0
#
#
# class ImdbSpider(CrawlSpider):
#     name = 'imdb'
#     allowed_domains = ['imdb.cn']
#     rules = (
#         Rule(LinkExtractor(allow=r"/title/tt\d+$"), callback="parse_imdb", follow=True),
#     )
#
#     def start_requests(self):
#         for i in range(1, 14616):
#             url = "http://www.imdb.cn/nowplaying/" + str(i)
#             yield Request(url=url, callback=self.parse_imdb)
#
#     def parse_imdb(self, response):
#         global n
#         n += 1
#         print(n)
#         item = MoiveEvaluateItem()
#         item['link'] = response.url
#         item['name'] = "".join(response.xpath('//*[@class="fk-3"]/div[@class="hdd"]/h3/text()').extract())
#         for k, v in item.items():
#             print(k, v)
#         pass


