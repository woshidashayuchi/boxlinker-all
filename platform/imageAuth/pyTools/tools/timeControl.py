#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 17/2/13 13:59
"""

import os
import time
import datetime
import random

def get_now_time(seconds=None):  # 输出  2016-09-18 16:35:30  样式的时间格式
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(seconds))

def get_now_time_ss_z():
    # 输出  2016-09-19T02:57:21.766611257Z  样式的时间格式  java 时间格式
    # 1474263549.65
    # 1474253967716
    return time.strftime('%Y-%m-%dT%H:%M:%S.', time.gmtime()) + str(datetime.datetime.now().microsecond) + 'Z'

def get_now_time_ymd(part='-'):  # 采用不同分割符，分割 -, . , other      2016.09.18
    return time.strftime('%Y' + part + '%m' + part + '%d', time.localtime())


def get_timestamp_13():
    now_time = time.time()
    return int(round(now_time * 1000))


def random_str_num(le=16):
    rand = random.uniform(1, 100)
    rand = str(rand).replace('.', '') + str(get_timestamp_13())
    return rand[0:le]


def strtime_to_int(strtime, detailed=True):
    """
    :param strtime: 字符串的数据格式,如  2014-04-16 00:00:00
    :param onlydate: 日期字符串是否是精确时间  含有时分秒
    :return:
    """
    try:
        if detailed:
            time_array = time.strptime(strtime, '%Y-%m-%d %H:%M:%S')  #将其转换为时间数组
        else:
            time_array = time.strptime(strtime, '%Y-%m-%d')  # 将其转换为时间数组

        time_stamp = int(time.mktime(time_array))  # 转换为时间戳:
    except Exception:
        time_stamp = 0
    finally:
        return time_stamp

def int_time_to_str(timeStamp, detailed=True):
    time_array = time.localtime(timeStamp)
    if detailed:
        strtime = time.strftime('%Y-%m-%d %H:%M:%S', time_array)
    else:
        strtime = time.strftime('%Y-%m-%d', time_array)
    return strtime

def time_delta(timeStamp, days=1):
    """
    :param timeStamp: 时间戳格式的时间秒数
    :param days:      增加的天数
    :return:
    """
    timeStamp += 24 * 60 * 60 * days
    return int_time_to_str(timeStamp, detailed=False)


def stos(srctime='31/May/2016:09:41:20', src_format='%d/%b/%Y:%H:%M:%S', dst_format='%Y-%m-%d %H:%M:%S'):
    """
    :param srctime:     原始的时间
    :param src_format:  原始的时间字符串格式
    :param dst_format:  转换成的格式
    :return:
    """
    """
    字符串格式更改
    :return:
    """
    timeArray = time.strptime(srctime, src_format)
    otherStyleTime = time.strftime(dst_format, timeArray)

    return otherStyleTime


# 2016-10-11T16:38:50.144274527+08:00




def ddd(strtime="2016-10-11T16:38:50"):

    # import datetime
    #
    # t_str = '2013-11-30 20:44:07'
    # d = datetime.datetime.strptime(t_str, '%Y-%m-%d %H:%M:%S')
    # print d

    # time_array = datetime.strptime(strtime, '%Y-%m-%dT%H:%M:%S')   # 将其转换为时间数组
    #
    # print time_array
    # time_stamp = int(time.mktime(time_array))  # 转换为时间戳:
    # print time_stamp

    ss = "2016-10-1116:38:50144274527+08:00"
    print ss.rsplit('.')[0].replace('T', ' ')

if __name__ == '__main__':

    print get_timestamp_13()

    print int(time.time())
    print int(time.time()) + 60 * 60 * 24
    print int_time_to_str(int(time.time()))

    print get_now_time()

    print 'sssssssss'

    print int_time_to_str(1490502003.168)
