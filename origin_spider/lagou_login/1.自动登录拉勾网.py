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
        'password': 'freedom',
        'request_form_verifyCode': '',
        'submit': '',

    },
    cookies=r1.cookies.get_dict()
)

# ############### 3. 查看个人页面 ###############
r5 = requests.get(
    url='https://www.lagou.com/resume/myresume.html',
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'

    },
    cookies=r1.cookies.get_dict()
)

print(r5.cookies.get_dict())
print(r5.text)
