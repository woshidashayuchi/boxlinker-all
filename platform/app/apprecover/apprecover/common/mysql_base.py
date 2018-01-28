# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

from conf import conf

from common.logs import logging as log
from common.single import Singleton
from common.DBUtils.PooledDB import PooledDB

try:
    import MySQLdb
except ImportError, e:
    log.error('MySQLdb import error: %s' % (e))
    raise


class MysqlInit(object):

    __metaclass__ = Singleton

    def __init__(self):

        try:
            self.pool = PooledDB(MySQLdb, 4,
                                 host=conf.db_server01, port=conf.db_port,
                                 user=conf.db_user, passwd=conf.db_passwd,
                                 db=conf.database, charset='utf8')
        except Exception, e:
            log.error('db_server01(%s) connection error: reason= %s'
                      % (conf.db_server01, e))
            try:
                self.pool = PooledDB(MySQLdb, 4,
                                     host=conf.db_server02, port=conf.db_port,
                                     user=conf.db_user, passwd=conf.db_passwd,
                                     db=conf.database, charset='utf8')
            except Exception, e:
                log.error('db_server02(%s) connection error: reason=%s'
                          % (conf.db_server02, e))
                raise

    def get_cursor(self):

        try:
            self.conn = self.pool.connection()
            self.cursor = self.conn.cursor()
            self.cursor.execute('SET NAMES utf8')
            # self.cursor.execute('SET CHARACTER SET utf8')
            # self.cursor.execute('SET character_set_connection=utf8')
        except Exception, e:
            log.error('Get MySQL cursor error: reason=%s' % (e))
            self.cursor.close()
            self.conn.close()
            raise

    def exec_select_sql(self, sql):

        self.get_cursor()
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            self.cursor.close()
            self.conn.close()
            log.debug('exec sql success, sql=%s' % (sql))
            return result
        except Exception, e:
            log.error('exec sql error, sql=%s, reason=%s' % (sql, e))
            raise

    def exec_update_sql(self, *sql):

        self.get_cursor()
        try:
            for v_sql in sql:
                self.cursor.execute(v_sql)

            self.conn.commit()
            self.cursor.close()
            self.conn.close()
            log.debug('exec sql success, sql=%s' % (str(sql)))
            return
        except Exception, e:
            try:
                for v_sql in sql:
                    self.cursor.execute(v_sql)

                self.conn.commit()
                self.cursor.close()
                self.conn.close()
                log.debug('exec sql success, sql=%s' % (str(sql)))
                return
            except Exception, e:
                log.error('exec sql error, sql=%s, reason=%s'
                          % (str(sql), e))
                self.cursor.close()
                self.conn.close()
                raise
