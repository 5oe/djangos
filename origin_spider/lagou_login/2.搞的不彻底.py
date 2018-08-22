#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import requests

# ############### 1. 查看登录页面 ###############
r1 = requests.get(
    url='https://passport.lagou.com/login/login.html',
    headers={
        'Host': 'passport.lagou.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
)
X_Anti_Forge_Token = re.findall(r"window.X_Anti_Forge_Token = '(.*?)'", r1.text, re.S)[0]
X_Anti_Forge_Code = re.findall(r"window.X_Anti_Forge_Code = '(.*?)'", r1.text, re.S)[0]

# ############### 2. 用户名密码登录 ###############
r2 = requests.post(
    url='https://passport.lagou.com/login/login.json',
    headers={
        'Host': 'passport.lagou.com',
        'Referer': 'https://passport.lagou.com/login/login.html',
        'X-Anit-Forge-Code': X_Anti_Forge_Code,
        'X-Anit-Forge-Token': X_Anti_Forge_Token,
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    },
    data={
        'isValidate': True,
        'username': '13128102401',
        'password': 'e77720f7f898e3a732fdd8dd7bc19efb',
        'request_form_verifyCode': '',
        'submit': '',

    },
    cookies=r1.cookies.get_dict()
)
print(r2.text)
# ############### 3. 查看个人页面 ###############
cook = '_ga=GA1.2.135832056.1528466842; user_trace_token=20180608220702-3762d959-6b25-11e8-9431-5254005c3644; LGUID=20180608220702-3762def7-6b25-11e8-9431-5254005c3644; index_location_city=%E5%B9%BF%E5%B7%9E; JSESSIONID=ABAAABAABEEAAJAE207C0B51AFA21D3C6CD94BDC312D2F2; _gid=GA1.2.591136767.1532187920; X_HTTP_TOKEN=b790fc438ac6f79a160ed3706a14b9ff; ab_test_random_num=0; hasDeliver=0; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; LG_LOGIN_USER_ID=21182c50fd3dc7367d2798df31dee6e0a87ac128d826a69649d2686ba37d95d3; _putrc=0C98BECFA9C01FF5123F89F2B170EADC; login=true; unick=%E8%B5%B5%E5%AD%90%E6%87%BF; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1531637607,1532187920,1532189820,1532190882; LGSID=20180722082408-8cb92dd4-8d45-11e8-9ee6-5254005c3644; gate_login_token=ab8d0595bf01bc3ab4fcfa3dff0c699df4064b52539743d4b6231f42782889d2; SEARCH_ID=32a61a736e4a4f09b16573433c71c097; TG-TRACK-CODE=jobs_again; fromsite="localhost:63342"; utm_source=""; _gat=1; LGRID=20180722090836-c315040a-8d4b-11e8-a280-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1532221718'
mycook_dict = {}
string_list = cook.split(';')
for string in string_list:
    k, v = string.split('=', 1)
    mycook_dict[k] = v

cookie_dict = dict(r2.cookies.get_dict(), **(r1.cookies.get_dict()))

r3 = requests.get(
    url='https://www.lagou.com/jobs/3944019.html',
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'X-L-REQ-HEADER': "{deviceType:1}",
        'Origin': 'https://account.lagou.com',
        'Host': 'www.lagou.com',
        'Referer': 'https://www.lagou.com/',
        'Upgrade-Insecure-Requests': '1',

    },
    cookies=cookie_dict,
    params={
        'source': 'viewrec',
        'i': 'position_rec-3',
    }
)

with open('a.html', 'w') as f:
    f.write(r3.text)
print(cookie_dict)
print('*' * 200)
print(mycook_dict)
