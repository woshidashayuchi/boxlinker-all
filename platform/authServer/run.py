#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/8/26 下午6:01
"""
import time
from authServer.index import run_server

if __name__ == '__main__':

    while True:
        try:
            run_server()
        except Exception as msg:
            print 'is error begin'
            print msg.message
            print msg.args
            print 'is error end'
            time.sleep(10)