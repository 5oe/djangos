import requests
import hashlib
import re


def get_password(passwd):
    '''这里对密码进行了md5双重加密 veennike 这个值是在main.html_aio_f95e644.js文件找到的 '''
    passwd = hashlib.md5(passwd.encode('utf-8')).hexdigest()
    passwd = 'veenike' + passwd + 'veenike'
    passwd = hashlib.md5(passwd.encode('utf-8')).hexdigest()
    return passwd


def on_ready():
    response = requests.get(
        url='https://passport.lagou.com/login/login.html',
        headers={
            'Referer': 'https://www.lagou.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        }
    )
    X_Anti_Forge_Token = re.findall(r"window.X_Anti_Forge_Token = '(.*?)'", response.text, )[0]
    X_Anti_Forge_Code = re.findall(r"window.X_Anti_Forge_Code = '(.*?)'", response.text, )[0]

    header = {
        'X-Anit-Forge-Code': X_Anti_Forge_Code,
        'X-Anit-Forge-Token': X_Anti_Forge_Token,
        'Referer': 'https://passport.lagou.com/login/login.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    }
    return header, response.cookies.get_dict()

    # https://passport.lagou.com/login/login.json


def login(username, passwd):
    headers, cookies = on_ready()
    login_form = {
        'isValidate': 'true',
        'username': username,
        'password': get_password(passwd),
        'request_form_verifyCode': '',
        'submit': '',
    }
    response = requests.post(
        url='https://passport.lagou.com/login/login.json',
        headers=headers,
        data=login_form,
        cookies=cookies,
    )
    return response


def account_info():
    response = login('13128102401', 'freedom')
    headers, other_cookies = on_ready()
    print(response.text)
    cookies = response.cookies.get_dict()
    r1=requests.get(
        url='https://gate.lagou.com/v1/neirong/account/users/0/',
        headers=headers,
        cookies=cookies
    )
    print(r1.text)
    r2 = requests.get(
        url='https://gate.lagou.com/v1/neirong/account/users/0/',
        headers=headers,
        cookies=r1.cookies.get_dict()
    )
    print(r2.text)

account_info()
