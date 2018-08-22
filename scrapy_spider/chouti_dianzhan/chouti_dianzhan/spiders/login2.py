import json
import scrapy
from scrapy.http.cookies import CookieJar
from scrapy.http.request import Request
from scrapy.selector import HtmlXPathSelector
from scrapy import FormRequest


class LoginSpider(scrapy.Spider):
    name = 'login2'
    allowed_domains = ['chouti.com']
    # start_urls = ['https://dig.chouti.com/', ]

    login_cookies = {}
    # cook_jar = None

    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

    # get请求获取必要的cookies,为post请求做准备
    # 将获取的cookie作为参数,发送登录的post请求
    def start_requests(self):
        yield Request(
            url='https://dig.chouti.com/',
            method='GET',
            headers=self.headers,
            callback=self.parse,
            meta={'cookiejar': 1}
        )

    def parse(self, response):
        # cook_jar = CookieJar()
        # cook_jar.extract_cookies(response, response.request)
        # self.cook_jar = cook_jar

        cookies_list = response.headers.getlist('Set-Cookie')
        for cookie in cookies_list[0].decode('utf8').split(';'):
            k, v = cookie.split('=', 1)
            self.login_cookies[k] = v

        print(self.login_cookies)
        # yield Request(
        #     url='http://dig.chouti.com/login',
        #     method='POST',
        #     headers=self.headers,
        #     body='phone=8613128102401&password=freedom&oneMonth=1',
        #     callback=self.to_index,
        #     # meta={'cookiejar': response.meta['cookiejar']},
        #     cookies=self.login_cookies
        # )

        data = {
            'phone': '8613128102401',
            'password': 'freedom',
            'oneMonth': '1'
        }

        return [FormRequest.from_response(response,
                                          url='http://dig.chouti.com/login',  # 真实post地址
                                          meta={'cookiejar': 1},
                                          headers=self.headers,
                                          formdata=data,
                                          callback=self.to_index,
                                          )]

    def to_index(self, response):
        # 验证登录是否成功
        print(response.text)
        d = json.loads(response.text)
        # {'result': {'code': '9999', 'message': '', 'data': {'complateReg': '0', 'destJid': 'cdu_52915644228'}}}
        if d['result']['code'] != '9999':
            raise Exception('获取cookie失败')
        print('*' * 200)
        Cookie2 = response.request.headers.getlist('Cookie')
        print('登录时携带请求的Cookies：', Cookie2)
        yield Request(
            url='http://dig.chouti.com/',
            method='GET',
            headers=self.headers,
            meta={'cookiejar': response.meta['cookiejar']},
            callback=self.upvote,
            # cookies=self.login_cookies,
        )

    def upvote(self, response):
        # 点赞
        print('！' * 200)
        hxs = HtmlXPathSelector(response)
        news_list = hxs.select('//div[@class="content-list"]//div[@class="item"]')
        for news in news_list:
            news_id = news.xpath('.//div[@class="part2"]/@share-linkid').extract_first()
            url = 'https://dig.chouti.com/link/vote?linksId=%s' % news_id
            yield Request(
                url=url,
                method='POST',
                headers=self.headers,
                # meta={'cookiejar': response.meta['cookiejar']},
                callback=self.upvote_result,
                cookies=self.login_cookies,
            )

    def upvote_result(self, response):
        print(3)
        print(response.text)
