#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/8/10 下午5:58
@func: 数据库配置文件
"""

from authServer.conf.conf import DEBUG


import platform


# 业务数据库

sysstr = platform.system()  # Windows测试模式

class hub_db:
    charset = 'utf8'
    port = 3306
    if DEBUG:
        user = 'root'
        pawd = 'root123admin'
        cydb = 'registry'

        if 'Darwin' == sysstr:  # mac
            host = '192.168.1.6'
        elif 'Linux' == sysstr:
            host = 'mysql'
        mysql_engine = 'mysql://' + user + ':' + pawd + '@' + host + ':' + str(port) + '/' + cydb + '?charset=utf8'
    else:
        host = '101.201.53.211'  # 线上
        user = 'root'
        pawd = 'root123admin'
        cydb = 'registry'
        mysql_engine = 'mysql://' + user + ':' + pawd + '@' + host + ':' + str(port) + '/' + cydb + '?charset=utf8'


print hub_db.mysql_engine