#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import uuid

from common.logs import logging as log
from common.code import request_result
from ceph.driver import ceph_driver


class CephPoolManager(object):

    def __init__(self):

        self.ceph_driver = ceph_driver.CephDriver()

    def cephpool_create(self, pool_type, pool_name):

        pool_check = self.ceph_driver.pool_check(pool_name)
        if int(pool_check) != 0:
            log.info('存储池%s已存在，无需再次创建' %(pool_name))
            return request_result(301)

        if pool_type == 'hdd':
            pool_create = self.ceph_driver.pool_hdd_create(pool_name)
            if int(pool_create) != 0:
                log.error('机械硬盘池创建失败')
                return request_result(534)

        elif pool_type == 'ssd':
            pool_create = self.ceph_driver.pool_ssd_create(pool_name)
            if int(pool_create) != 0:
                log.error('固态硬盘池创建失败')
                return request_result(534)

        pool_info = self.ceph_driver.pool_info_get()
        pool_info = pool_info.split(" ")

        pool_size = pool_info[0]
        avail = pool_info[1]
        used = pool_info[2]
        used_rate = pool_info[3]

        result = {
                     "pool_type": pool_type,
                     "pool_name": pool_name,
                     "pool_size": pool_size,
                     "avail": avail,
                     "used": used,
                     "used_rate": used_rate
                 }

        return request_result(0, result)

    def cephpool_info(self):

        pool_info = self.ceph_driver.pool_info_get()
        pool_info = pool_info.split(" ")

        pool_size = pool_info[0]
        avail = pool_info[1]
        used = pool_info[2]
        used_rate = pool_info[3]

        result = {
                     "pool_size": pool_size,
                     "avail": avail,
                     "used": used,
                     "used_rate": used_rate
                 }

        return request_result(0, result)
