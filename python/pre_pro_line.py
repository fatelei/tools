#!/usr/bin/env python
#-*-coding: utf8-*-


"""
process two line data:
data format in file:
xxxx
xxxxx
xxxxxxx
xxxx

it convert to: {filename: {xxxx: [xxxxx], xxxxxx: [xxxx]}
"""


import argparse
import os
import json
import logging

logging.basicConfig(filename="process.log")

def process_core(path):
    """
    处理核心
    """
    filename = ""
    error_line = 0
    lines = []
    try:
        f = file(path, "r")
        filename = f.name
        data = {}
        lines = f.readlines()
        f.close()
        length = len(lines)
        odd = True if length % 2 != 0 else False
        for i in xrange(length):
            tmp = lines[i].replace("\n", "")
            if odd:
                if i == 0:
                    data[tmp] = [lines[i + 1].replace("\n", "")]
                elif i % 2 != 0:
                    if tmp in data:
                        data[tmp].append(lines[i + 1].replace("\n", ""))
                    else:
                        data[tmp] = [lines[i + 1].replace("\n", "")]
            else:
                if i % 2 == 0:
                    if tmp in data:
                        data[tmp].append(lines[i + 1].replace("\n", ""))
                    else:
                        data[tmp] = [lines[i + 1].replace("\n", "")]
        target_filename = "{0}.json".format(filename)
        f = file(target_filename, "w")
        f.write(json.dumps(data))
        f.close()
    except Exception as e:
        logging.warning("filename：%s" % filename)
        logging.warning(e)


def process_dir(dirname, need):
    """
    处理目录
    """
    for root, dirname, files in os.walk(dirname):
        for name in files:
            path = "".join([root, "/", name])
            if need:
                if name.find(need) != -1:
                    process_core(path)
            else:
                process_core(path)


def process_file(filename, need):
    """
    处理文件
    """
    if need:
        if filename.find(need) != -1:
            process_core(filename)
    else:
        process_core(filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="process two line data to json")
    parser.add_argument(
        "-t", dest="target", type=str, help="target to process")
    parser.add_argument(
        "-n", dest="need", type=str, help="need to process file type")
    args = parser.parse_args()
    if args.target:
        try:
            pid = os.fork()
            if pid > 0:
                os._exit(0)
        except OSError as error:
            print "Unable to fork. Error: %d (%s)" % (error.errno, error.strerror)
            os._exit(1)
        if os.path.isdir(args.target):
            process_dir(args.target, args.need)
        elif os.path.isfile(args.target):
            process_file(args.target, args.need)
        else:
            print "can't process unknow type"
