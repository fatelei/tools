#!/usr/bin/env python
#-*-coding:utf8-*-

# a simple web crawler use python requests

import cookielib
import urllib2
import urllib
import json
import logging
import datetime
import argparse
import re

# url to crawler
settings = {
    "login_url": "https://www.appannie.com/account/login/",
    "target_url": "http://www.appannie.com/app/ios/kingsoft-office-free-seamlessly-compatible-with-word-ppt/ranking/history/chart_data/?d=iphone&c=143465&f=ranks&s={0}&e={1}&_c=1"
}

# custom headers
headers = [
    ('Host', 'www.appannie.com'),
    ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.172 Safari/537.22'),
    ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
    ('Origin', 'https://www.appannie.com'),
    ('Referer', 'https://www.appannie.com/account/login/'),
    ('Connection', 'keep-alive')
]

# add proxy
config = {'host': 'songfei.org', 'port': 31287}

# user login info
user_info = {
    "username": "fatelei@gmail.com",
    "password": "fate1234",
    "next": "/",
    "remember_user": "on"
}


def start_crawler(start, end):
    # start login
    try:
        cj = cookielib.CookieJar()
        proxy_handler = urllib2.ProxyHandler(
            proxies={'http': '%s:%s' % (config['host'], config['port']), 'https': '%s:%s' % (config['host'], config['port'])})
        opener = urllib2.build_opener(
            proxy_handler, urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = headers
        data = urllib.urlencode(user_info)
        req = opener.open(settings["login_url"], data=data)
        if req.code == 200:
            target_url = settings["target_url"].format(start, end)
            req = opener.open(target_url)
            data = req.read()
            try:
                f = file("rst.json", "w")
                f.write(data)
                f.close()
                data = json.loads(data)
                for d in data:
                    print "key: %s" % d["label"]

                    for l in d["data"]:
                        print "time: %s -> download: %d -> event: %s" % (datetime.datetime.fromtimestamp(l[0] / 1000).strftime("%Y-%m-%d %H-%M-%S"),
                                                                         l[1], l[2].replace("\n", "") if l[2] else l[2])

            except Exception as e:
                logging.warning(e)
        else:
            logging.warning("login failed")
    except Exception as e:
        logging.warning(e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="a simple crawler")
    parser.add_argument("-s", dest="s", type=str, help="start date")
    parser.add_argument("-e", dest="e", type=str, help="end date")
    args = parser.parse_args()
    if args.e or args.s:
        p = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        if p.search(args.e) and p.search(args.s):
            start, end = args.s, args.e
    else:
        start = end = datetime.datetime.now().strftime("%Y-%m-%d")
    start_crawler(start, end)
