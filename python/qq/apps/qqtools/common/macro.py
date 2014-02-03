#!/usr/bin/python
#-*-coding: utf8-*-

"""
macro
"""


LOGIN_POST_TEMPLATE = {
    "login_url": "http://pt.3g.qq.com/s?aid=nLogin",
    "sidtype": "1",
    "nopre": "0",
    "loginTitle": "login",
    "q_from": "",
    "bid": "0",
    "loginType": "1",
    "qq": "", # qq号
    "pwd": "", # qq密码
    "loginsubmit": "login"
}

CHAT_POST_TEMPLATE = {
    "3gqqsid": "",
    "auto": "1",
    "loginType": "1"  # 1是在线，2是隐身
}

QQ_SEND_MSG_TEMPLATE = {
	"msg": "", # 发送的内容
	"u": "", # 发送的qq号
	"saveURL": "0",
	"do": "send",
	"on": "1",
	"num": "", # 发送的qq号
	"do": "sendsms",
	"aid": u"发送"
}

MOOD_TEMPLATE = {
	"opr_type": "publish_shuoshuo",
	"res_uin": "", # 发布心情的qq号
	"content": "", # 心情内容
	"richval": "", # 富文本内容
	"lat": "0", # 维度
	"lon": "0", # 经度
	"lbsid": "",
	"issyncweibo": "0", # 是否同步到微博
	"format": "json", # 返回数据类型
	"sid": ""
}

HEARTBEAT_INTERVAL = 60

QQ_URL = "http://pt.3g.qq.com/s?aid=nLogin"

QQCHAT_URL = "http://pt.3g.qq.com/s?aid=nLogin3gqq&auto=1&sid={0}"

QQHEARTBEAT_URL = "http://pt.3g.qq.com/s?aid=nLogin3gqqbysid&3gqqsid={0}"

QQCHAT_URLS = ["http://q16.3g.qq.com/g/s?sid={0}",
			   "http://q32.3g.qq.com/g/s?sid={0}"]

QQRECV_MSG_URL = "http://q32.3g.qq.com/g/s?sid={0}&aid=nqqChat&u={1}&g_f=1660"

PUBLISH_MOOD_URL = "http://m.qzone.com/mood/publish_mood"

QQ_LOGOUT_URL = "http://pt.3g.qq.com/s?sid={0}&aid=nLogout"
