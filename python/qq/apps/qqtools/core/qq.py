#!/usr/bin/python
#-*-coding: utf8-*-

import requests
import json
import logging
import signal
import random

from lxml import etree
from copy import deepcopy
from urlparse import urlparse

from qqtools.common.macro import QQ_URL, LOGIN_POST_TEMPLATE, QQCHAT_URL, CHAT_POST_TEMPLATE,\
    QQHEARTBEAT_URL, QQCHAT_URLS, QQ_SEND_MSG_TEMPLATE, MOOD_TEMPLATE, PUBLISH_MOOD_URL


def heart_beat(signum, frame):
    """
    发送心跳保持在线
    """
    for k, v in self.clients.iteritems():
        refresh_url = QQHEARTBEAT_URL.format(v)
        resp = requests.get(refresh_url)


class QQ(object):

    def __init__(self):
        self.headers = {
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"
        }
        self.clients = {}

    def parse_login_url(self, xml):
        """
        获取登录地址
        """
        root = etree.fromstring(xml.encode('utf8'))
        goes = root.xpath('//go[@method="post"]')
        sids = root.xpath('//postfield[@name="sid"]')
        login_url = ""
        for go in goes:
            tmp_val = go.values()
            if len(tmp_val) > 0:
                if "handleLogin" in tmp_val[0]:
                    login_url = tmp_val[0]
                    break

        sid = sids[0].values()
        url = '{0}&{1}={2}'.format(login_url, sid[0], sid[1])
        return url

    def parse_chat_url(self, xml):
        """
        获得聊天地址
        """
        root = etree.fromstring(xml.encode('utf8'))
        goes = root.xpath('//go[@method="post"]')

        # 在线地址
        return goes[0].values()[0]

        # 隐身地址
        # return goes[1].values()[1]

    def get_qq_sid(self, resp):
        """
        获取sid
        """
        query = urlparse(resp.url).query
        func = lambda x: x.split('=')
        rst = map(func, query.split('&'))
        return rst[0][1]

    def qq_login(self, qq_no, qq_pwd):
        """
        登录qq
        """
        resp = requests.get(QQ_URL)
        login_url = self.parse_login_url(resp.text)
        post_data = deepcopy(LOGIN_POST_TEMPLATE)
        post_data['qq'] = qq_no
        post_data['pwd'] = qq_pwd
        resp = requests.post(login_url, headers=self.headers, data=post_data)
        sid = self.get_qq_sid(resp)
        self.clients[qq_no] = sid
        self.qqchat_login(qq_no)

    def qqchat_login(self, qq_no):
        qqsid = self.clients[qq_no]
        chat_url = QQCHAT_URL.format(qqsid)
        resp = requests.get(chat_url)
        chat_login_url = self.parse_chat_url(resp.text)
        post_data = deepcopy(CHAT_POST_TEMPLATE)
        post_data['3gqqsid'] = qqsid
        resp = requests.post(chat_url, headers=self.headers, data=post_data)
        status_code = resp.status_code
        if status_code == 200:
            print "chatlogin ok"
        else:
            print resp.text
        #signal.signal(signal.SIGALRM, heart_beat)
        #signal.setitimer(signal.ITIMER_REAL, 40)

    def send_qq_msg(self, qq_no, send_qq_no, content):
        """
        发送qq消息
        """
        index = random.randint(0, 1)
        sid = self.clients[qq_no]
        chat_url = QQCHAT_URLS[index].format(sid)
        post_data = deepcopy(QQ_SEND_MSG_TEMPLATE)
        post_data["msg"] = content
        post_data["u"] = send_qq_no
        post_data["num"] = send_qq_no
        resp = requests.post(chat_url, headers=self.headers, data=post_data)
        status_code = resp.status_code
        if status_code == 200:
            print "send ok"
        else:
            print resp.text

    def publish_qq_mood(self, qq_no):
        """
        发送qq心情
        """
        post_data = deepcopy(MOOD_TEMPLATE)
        post_data["res_uin"] = qq_no
        post_data["content"] = u"燕玲，好喜欢你!"
        post_data["sid"] = self.clients[qq_no]
        resp = requests.post(
            PUBLISH_MOOD_URL, headers=self.headers, data=post_data)
        if resp.status_code == 200:
            print "publish ok"
        else:
            print resp.text

if __name__ == "__main__":
    qq = QQ()
    qq.qq_login('1443343615', 'k7yeqs&fate')
    qq.publish_qq_mood('1443343615')
