#!/usr/bin/python
#-*-coding: utf8-*-

import requests
import json
import logging
import random

from lxml import etree
from lxml.html import fromstring
from copy import deepcopy
from urlparse import urlparse
from requests.exceptions import ConnectionError, Timeout

from qqtools.common.macro import QQ_URL, LOGIN_POST_TEMPLATE, QQCHAT_URL, CHAT_POST_TEMPLATE,\
    QQHEARTBEAT_URL, QQCHAT_URLS, QQ_SEND_MSG_TEMPLATE, MOOD_TEMPLATE, PUBLISH_MOOD_URL,\
    QQRECV_MSG_URL, QQ_LOGOUT_URL


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

    def parse_recv_msg(self, html):
        """
        解析收到的qq消息
        """
        dom = fromstring(html)
        recv_msgs = dom.xpath('//p[@class="ft-s ft-cl2"]')
        for recv in recv_msgs:
            msg = recv.text.replace('\r\n', '').replace('&nbsp;', ' ')
            for brother in recv.itersiblings():
                msg += ':' + brother.text
            logging.info(msg)

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
        try:
            resp = requests.post(login_url, headers=self.headers, data=post_data)
        except ConnectionError as e:
            resp = requests.post(login_url, headers=self.headers, data=post_data)
        except Timeout as e:
            resp = requests.post(login_url, headers=self.headers, data=post_data)

        if resp.status_code == 200:
            sid = self.get_qq_sid(resp)
            self.clients[qq_no] = sid
            rst = self.qqchat_login(qq_no)
            if rst:
                return True
            else:
                return False
        else:
            return False

    def qqchat_login(self, qq_no):
        qqsid = self.clients[qq_no]
        chat_url = QQCHAT_URL.format(qqsid)
        resp = requests.get(chat_url)
        chat_login_url = self.parse_chat_url(resp.text)
        post_data = deepcopy(CHAT_POST_TEMPLATE)
        post_data['3gqqsid'] = qqsid
        try:
            resp = requests.post(chat_url, headers=self.headers, data=post_data)
        except ConnectionError as e:
            resp = requests.post(chat_url, headers=self.headers, data=post_data)
        except Timeout as e:
            resp = requests.post(chat_url, headers=self.headers, data=post_data)
        status_code = resp.status_code
        if status_code == 200:
            logging.info("chatlogin ok")
            return True
        else:
            logging.warning(resp.text)
            return False

    def send_qq_heart_beat(self, qq_no):
        """
        发送心跳保持在线
        """
        sid = self.clients[qq_no]
        refresh_url = QQHEARTBEAT_URL.format(sid)
        try:
            resp = requests.get(refresh_url)
        except ConnectionError as e:
            resp = requests.get(refresh_url)
        except Timeout as e:
            resp = requests.get(refresh_url)
        if resp.status_code != 200:
            logging.warning(resp.text)

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
            logging.info("send msg ok")
        else:
            logging.warning(resp.text)

    def receive_qq_msg(self, qq_no, recv_qq_no):
        """
        接收qq消息
        """
        sid = self.clients[qq_no]
        recv_url = QQRECV_MSG_URL.format(sid, recv_qq_no)
        resp = requests.get(recv_url, headers=self.headers)
        self.parse_recv_msg(resp.text)

    def publish_qq_mood(self, qq_no, content):
        """
        发送qq心情
        """
        post_data = deepcopy(MOOD_TEMPLATE)
        post_data["res_uin"] = qq_no
        post_data["content"] = content
        post_data["sid"] = self.clients[qq_no]
        resp = requests.post(
            PUBLISH_MOOD_URL, headers=self.headers, data=post_data)
        if resp.status_code == 200:
            logging.info("publish qq mood ok")
        else:
            logging.warning(resp.text)

    def qq_logout(self, qq_no):
        """
        qq注销
        """
        sid = self.clients[qq_no]
        logout_url = QQ_LOGOUT_URL.format(sid)
        resp = requests.get(logout_url)
        loggging.info(resp.status_code)


if __name__ == "__main__":
    qq = QQ()
    qq.qq_login('xx', 'xx')
    qq.publish_qq_mood('xx')
