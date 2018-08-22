import scrapy
from scrapy.http.request import Request
from scrapy import FormRequest


class Login3Spider(scrapy.Spider):
    name = 'login3'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}  # 设置浏览器用户代理

    def start_requests(self):
        """第一次请求一下登录页面，设置开启cookie使其得到cookie，设置回调函数"""
        return [Request('http://dig.chouti.com/', meta={'cookiejar': 1}, callback=self.parse)]

    def parse(self, response):
        # 响应Cookies
        Cookie1 = response.headers.getlist('Set-Cookie')  # 查看一下响应Cookie，也就是第一次访问注册页面时后台写入浏览器的Cookie
        print('后台首次写入的响应Cookies：', Cookie1)
        print(response.meta['cookiejar'])
        data = {  # 设置用户登录信息，对应抓包得到字段
            'phone': '8615284816568',
            'password': '279819',
            'oneMonth': '1'
        }

        print('登录中....!')
        """第二次用表单post请求，携带Cookie、浏览器代理、用户登录信息，进行登录给Cookie授权"""
        # return [FormRequest.from_response(response,
        #                                   url='http://dig.chouti.com/login',  # 真实post地址
        #                                   meta={'cookiejar': 1},
        #                                   headers=self.header,
        #                                   formdata=data,
        #                                   callback=self.next,
        #                                   )]

        yield Request(
            url='http://dig.chouti.com/login',
            method='POST',
            headers=self.header,
            body='phone=8613128102401&password=freedom&oneMonth=1',
            callback=self.next,
            meta={'cookiejar': response.meta['cookiejar']},
        )

    def next(self, response):
        # 请求Cookie
        Cookie2 = response.request.headers.getlist('Cookie')
        print('登录时携带请求的Cookies：', Cookie2)

        jieg = response.body.decode("utf-8")  # 登录后可以查看一下登录响应信息
        print('登录响应结果：', jieg)

        print('正在请需要登录才可以访问的页面....!')

        """登录后请求需要登录才能查看的页面，如个人中心，携带授权后的Cookie请求"""
        yield Request('http://dig.chouti.com/user/link/saved/1', meta={'cookiejar': True}, callback=self.next2)

    def next2(self, response):
        # 请求Cookie
        Cookie3 = response.request.headers.getlist('Cookie')
        print('查看需要登录才可以访问的页面携带Cookies：', Cookie3)
        print(Cookie3,"@@@@@")
        leir = response.xpath('//div[@class="tu"]/a/text()').extract()  # 得到个人中心页面
        print('最终内容!!!!!!!!!!!!', leir)
        leir2 = response.xpath('//div[@class="set-tags"]/a/text()').extract()  # 得到个人中心页面
        print(leir2)
