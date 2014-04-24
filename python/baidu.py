#!/usr/bin/python
#-*-coding: utf8-*-

import requests
import time
import pprint
import urllib

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36'
}


def get_baidu_cookie():
    resp = requests.get(
        'https://passport.baidu.com/v2/?login&u=', headers=headers)
    cookie = resp.headers['set-cookie'].split(';')[0]
    return cookie


def get_baidu_token():
    params = {
        'tpl': 'pp',
        'apiver': 'v3',
        'tt': int(time.time() * 1000),
        'class': 'login',
        'loginType': 'basicLogin',
        'callback': 'bd__cbs__tnhtnb'
    }

    query_str = urllib.urlencode(params)

    url = 'https://passport.baidu.com/v2/api/?getapi&' + query_str

    resp = requests.get(url, headers=headers)
    data = resp.text.replace('bd__cbs__tnhtnb', '')[1:-1]
    data = eval(data)
    token = data['data']['token']
    return token


def baidu_login():
    cookie = get_baidu_cookie()
    headers['cookie'] = cookie

    now = int(time.time() * 1000)
    url = 'http://wappass.baidu.com/wp/api/login?v=' + str(now)

    token = get_baidu_token()

    body = {
        'charset': 'UTF-8',
        'token': token,
        'tpl': 'pp',
        'apiver': 'v3',
        'tt': now,
        'safeflg': 0,
        'u': 'http://passport.baidu.com',
        'isPhone': True,
        'quick_user': 0,
        'loginType': 'basicLogin',
        'logLoginType': 'wap_loginTouch',
        'loginmerge': True,
        'username': 'fate_lei',
        'password': 'fate123'
    }

    resp = requests.post(
        'http://wappass.baidu.com/wp/api/login?v=1398174334508', headers=headers, data=body)

    pp = pprint.PrettyPrinter()
    pp.pprint(resp.json())


if __name__ == "__main__":
    baidu_login()
