import requests
import random
import time
import json
from conf import setting
from .log import logger

n = 0


class WebRequest(object):
    def __init__(self):
        self.session = requests.Session()

    def prepare_cookies(self, prepare_url=None):
        prepare_url = 'https://www.lagou.com/' if not prepare_url else prepare_url
        response = self.get(prepare_url)
        return response

    def random_agent(self):
        headers = setting.HEADERS
        headers['User-Agent'] = random.choice(setting.USER_AGENTS)
        return headers

    def get(self, url):
        headers = self.random_agent()
        response = self.session.get(url=url, headers=headers, )
        return response

    def post(self, url, params, form_data, timeOut=5, timeOutRetry=5):
        '''
        post获取响应
        url: 目标链接
        para: 参数
        headers: headers
        cookies: cookies
        proxy: 代理
        timeOut: 请求超时时间
        timeOutRetry: 超时重试次数
        return: 响应
        '''
        global n
        n += 1
        print(n)
        headers = self.random_agent()
        try:
            response = self.session.post(url=url, headers=headers, params=params, data=form_data, timeout=timeOut)
            if response.status_code == 200 or response.status_code == 302:
                d = json.loads(response.text)
                if d['success'] == False:
                    logger.log(status=False, msg='success false,重试次数%s' % timeOutRetry)
                    if timeOutRetry > 0:
                        self.reset()
                        time.sleep(7)
                        return self.post(url, params, form_data, timeOutRetry=timeOutRetry - 1)
                return d

        except Exception as e:
            logger.log(status=False, msg='访问失败,重试次数%s' % timeOutRetry)
            if timeOutRetry > 0:
                return self.post(url, params, form_data, timeOutRetry=timeOutRetry - 1)
            else:
                logger.log(status=False, msg='访问%s测底失败' % url)

    def reset(self):
        self.session = requests.Session()
        self.prepare_cookies()
