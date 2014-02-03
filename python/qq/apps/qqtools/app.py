#!/usr/bin/python
#-*-coding: utf8-*-


import argparse
import time
import logging

from qqtools.core.qq import QQ
from qqtools.common.macro import HEARTBEAT_INTERVAL

logging.basicConfig(filename="qq.log", level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


def run():
    parser = argparse.ArgumentParser(description="used for login qq")
    parser.add_argument(
        '-q', dest="qq_no", metavar="qq", type=str, help="qq no")
    parser.add_argument(
        '-p', dest="qq_pwd", metavar="password", type=str, help="qq password")
    parser.add_argument(
        '-u', dest="chat_qq", metavar="chatqq", type=str, help="chat with qq no")
    args = parser.parse_args()
    qq = QQ()
    qq_no = args.qq_no
    qq_pwd = args.qq_pwd
    chat_qq = args.chat_qq
    rst = qq.qq_login(qq_no, qq_pwd)

    if rst: 
        while True:
            try:
                time.sleep(HEARTBEAT_INTERVAL)
                qq.send_qq_heart_beat(qq_no)
                #qq.send_qq_msg(qq_no, chat_qq, "test")
                qq.receive_qq_msg(qq_no, chat_qq)
            except Exception as e:
                logging.warning(e, exc_info=True)
                break


if __name__ == "__main__":
    run()
