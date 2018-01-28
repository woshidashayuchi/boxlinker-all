# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/02/15

import time
import datetime

import pymysql
import pymysql.cursors
import os
from common.logs import logging as log
from conf import conf


class DbOperate(object):

    def __init__(self):
        self.db = conf.db_server01
        self.port = conf.db_port

    def connection(self):
        conn = pymysql.connect(host=self.db,
                               db='servicedata',
                               port=self.port,
                               user='cloudsvc',
                               passwd='cloudsvc',
                               charset='UTF8',
                               cursorclass=pymysql.cursors.DictCursor)
        cur = conn.cursor()
        return conn, cur

    def exeUpdate(self, cur, sql):
        sta = cur.execute(sql)
        return sta

    def exeDelete(self, cur, sql):
        sta = cur.execute(sql)
        return sta

    def exeQuery(self, cur, sql):
        cur.execute(sql)
        return cur

    def connClose(self, conn, cur):
        try:
            cur.close()
            conn.commit()
            conn.close()
        except Exception, e:
            log.error("close the connect to mysql server is error, reason=%s" % e)
            return

    def time_diff(self, update_date):
        dates = time.strptime(str(update_date), "%Y-%m-%d %H:%M:%S")
        date1 = datetime.datetime(dates[0], dates[1], dates[2], dates[3], dates[4], dates[5])
        # 实现年\月\日\时\分\秒差值计算
        time_differ = datetime.datetime.now() - date1
        # datetime.datetime() - datetime.dateytime() 是timedelta的,timedelta可以.days,.seconds
        if time_differ.seconds+time_differ.days*86400 < 60:
            return str(time_differ.seconds)+'秒前'
        elif time_differ.seconds+time_differ.days*86400 < 3600:
            return str(time_differ.seconds/60)+'分钟前'
        elif time_differ.seconds+time_differ.days*86400 < 86400:
            return str(time_differ.seconds/3600)+'小时前'
        elif time_differ.days >= 1 and time_differ.days < 30:
            return str(time_differ.days)+'天前'
        elif time_differ.days >= 30 and time_differ.days < 365:
            return str(time_differ.days/30)+'月前'
        else:
            return str(time_differ.days/365)+'年前'
