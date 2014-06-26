#!/usr/bin/python
#-*-coding: utf8-*-

import requests
import time
import pprint
import urllib
import argparse
import os
import datetime

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


def baidu_login(username="test", password="test123"):
    if "cookie" in headers:
        headers.pop('cookie')
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
        'isPhone': False,
        'quick_user': 0,
        'loginType': 'basicLogin',
        'logLoginType': 'wap_loginTouch',
        'loginmerge': True,
        'username': username,
        'password': password
    }

    resp = requests.post(
        'http://wappass.baidu.com/wp/api/login?v=1398174334508', headers=headers, data=body)
   
    result = resp.json()
    print result
    if result['errInfo']['no'] == u'0':
        return True
    else:
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", metavar="users", dest="user_file", type=str)
    parser.add_argument("-u", metavar="username", dest="username", type=str)
    parser.add_argument("-p", metavar="password", dest="password", type=str)    
    parser.add_argument("-o", metavar="result", dest="result", type=str)
    args = parser.parse_args()

    if not args.user_file and not args.username and not args.password:
        parser.print_usage()
    else:
        
        users = []
        results = []
        count = 0


        if args.result:
            record = True
        else:
            record = False

        if args.user_file:
            if os.path.isfile(args.user_file):
                with open(args.user_file, "rb") as f:
                    lines = f.readlines()
                    func1 = lambda x: x.replace("\r\n", "")
                    func = lambda x: x.split(' ')
                    users = map(func, map(func1, lines))

        else:
           if args.username and args.password:
               result = baidu_login(username=args.username,
                           password=args.password)
               if result:
                   results.append(u'%s %s 成功\n' % (args.username, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                   count += 1
               else:
                   results.append(u'%s %s 失败\n' % (args.username, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        for user in users:
            result = baidu_login(username=user[0], password=user[1])
            if result:
                results.append(u'%s %s 成功\n' % (user[0], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                count += 1
            else:
                results.append(u'%s %s 失败\n' % (user[0], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            time.sleep(10)

        if record:
           with open(args.result, 'wb') as f:
               f.write('用户数: %d\n' % len(users))
               for result in results:
                   f.write(result.encode('utf8'))
               f.write('成功/失败: %d/%d' % (count, (len(users) - count)))


