#!/usr/bin/python
#-*-coding: utf8-*-


import argparse

from qqtools.core.qq import QQ

def run():
    parser = argparse.ArgumentParser(description="used for login qq")
    parser.add_argument('-q', dest="qq_no", metavar="qq", type=str, help="qq no")
    parser.add_argument('-p', dest="qq_pwd", metavar="password", type=str, help="qq password")
    args = parser.parse_args()
    qq = QQ()
    qq_no = args.qq_no
    qq_pwd = args.qq_pwd
    print qq_no, qq_pwd
    qq.qq_login(qq_no, qq_pwd)

if __name__ == "__main__":
    run()


