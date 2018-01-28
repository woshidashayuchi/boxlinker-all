#! /usr/bin python
# -*- coding:utf8 -*-
# Date:2016/9/27
# Author:wang-xf

import time
import datetime


def get_now_time_ymd(part='-'):  # 采用不同分割符，分割 -, . , other      2016.09.18
    return time.strftime('%Y' + part + '%m' + part + '%d', time.localtime())


def get_now_time_ss_z():
    # 输出  2016-09-19T02:57:21.766611257Z  样式的时间格式  java 时间格式
    # 1474263549.65
    # 1474253967716
    return time.strftime('%Y-%m-%dT%H:%M:%S.', time.gmtime()) + str(datetime.datetime.now().microsecond) + 'Z'


def get_timestamp_13():
    now_time = time.time()
    return int(round(now_time * 1000))
