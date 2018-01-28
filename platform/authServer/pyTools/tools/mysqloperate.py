#!/usr/bin/env /usr/bin/python2.6
# coding: UTF-8
# build by lzp for mysql
# 数据库操作接口
# 20150809

import sys
import logging

hava_pymysql = True
hava_MySQLdb = True
MYQSL = None

try:
    import pymysql

    MYQSL = pymysql
except ImportError:
    hava_pymysql = False
    print "import pymysql ImportError"

if hava_pymysql:
    pass
else:
    try:
        import MySQLdb

        MYQSL = MySQLdb
    except ImportError:
        hava_MySQLdb = False
        print "import MySQLdb ImportError"

if hava_MySQLdb is False and hava_pymysql is False:
    exit(-1)


DEBUG = True
def PrintDbg(arg, debug=DEBUG):
    if debug == True:
        print(arg)


class mysqlOperation():
    def __init__(self, host, user, passwd, port, db, charset="utf8", debug=DEBUG, log='mysql.log'):
        """
        :param host:
        :param user:
        :param passwd:
        :param port:
        :param db:
        :param charset:
        :param debug:   调试输出
        :return:
        """
        self.HOST = host
        self.USER = user
        self.PWD = passwd
        self.PORT = port
        self.DB = db
        self.CS = charset
        self.debug = debug

        try:
            self.connHandle = MYQSL.connect(host=self.HOST, user=self.USER, passwd=self.PWD, port=self.PORT,
                                              charset=self.CS, db=self.DB)

            self.curHandle = self.connHandle.cursor()
            #self.connHandle.select_db(self.DB)
        except Exception as msg:
            for val in msg.args:
                PrintDbg(val, self.debug)


    def __del__(self):
        try:
            self.curHandle.close()
            self.connHandle.close()
        except Exception as msg:
            PrintDbg('mysqlOperation __del__ error', self.debug)
            for val in msg.args:
                PrintDbg(val, self.debug)


    def doDelete(self, sql, args=None):
        """
        add lzp 20160531 删除数据记录
        :param sql:
        :param args:
        :return:成功返回True,失败返回False
        """
        ret = True
        try:
            self.curHandle.execute(sql, args=args)
            self.connHandle.commit()
        except Exception:
            ret = False
            self.connHandle.rollback()
        finally:
            return ret





    def doExecute(self, sql, args=None ):
        """
        建表、执行sql语句
        :param sql:
        :return:
        """
        ret = True
        try:
            self.curHandle.execute(sql, args=args)
            results = self.curHandle.fetchall()
        except Exception as msg:
            #self.connHandle.rollback()
            ret = False
            for val in msg.args:
                PrintDbg(val, self.debug)
        finally:
            return ret


    def Execute(self, sql, args=None):
        """
        建表、执行sql语句
        :param sql:
        """
        ret = True
        try:
            self.curHandle.execute(sql, args=args)
        except Exception as msg:
            ret = False
            self.connHandle.rollback()
            for val in msg.args:
                PrintDbg(val, self.debug)
        finally:
            return ret

    def create_tb(self, sql):
        """
        :param sql:  建表
        """
        ret = True
        try:
            self.curHandle.execute(sql)
        except Exception as msg:
            ret = False
            for val in msg.args:
                PrintDbg(val, self.debug)
        finally:
            return ret


    def selectBySql(self, sql, args=None, retbool=False):
        """
        add lzp 20160219
        :param sql:  sql 语句
        :param args: 参数字典
        :param retbool: 模式  默认retbool=False 返回查找到的所有信息
                             retbool=True 返回是否存在要查找的值, 返回True存在, False不存在
        """
        try:
            self.curHandle.execute(sql, args)
            results = self.curHandle.fetchall()

            if retbool is False:
                return results
            elif retbool and len(results):
                return True
            else:
                return False

        except Exception as msg:
            for val in msg.args:
                PrintDbg(val, self.debug)
            return False

    def InsertOrUpdateBySql(self, sql, args=None):
        """
        add lzp 20160219
        :param sql:  插入sql语句
        :param args: 需要格式化的字典数据
        :return:
        """

        ret = True
        try:
            # self.curHandle.execute("set names UTF-8")
            self.curHandle.execute(sql, args)
            self.connHandle.commit()
        except Exception as msg:
            self.connHandle.rollback()
            ret = False
            for val in msg.args:
                PrintDbg(val, self.debug)
        finally:
            return ret


    def InsertOrUpdateMan(self, sql, args):
        """
        add lzp 20160219
        :param sql:  插入sql语句
        :param args: 需要格式化的字典数据
        :return:
        """

        ret = True
        try:
            # self.curHandle.execute("set names UTF-8")
            #self.curHandle.execute(sql, args)
            self.curHandle.executemany(sql, args)
            self.connHandle.commit()
        except Exception as msg:
            self.connHandle.rollback()
            ret = False
            PrintDbg("InsertOrUpdateMan is error", self.debug)
            for val in msg.args:
                PrintDbg(val, self.debug)
        finally:
            return ret
