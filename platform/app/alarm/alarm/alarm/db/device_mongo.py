# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 17/5/19 下午2:28
import sys
p_path = sys.path[0] + '/../..'
p_path1 = sys.path[0] + '/..'
sys.path.insert(1, p_path)
sys.path.append(p_path1)
import pymongo
import datetime
from conf import conf
from common.logs import logging as log


class DeviceMongo(object):
    def __init__(self):
        self.mongo_host = conf.mongo_host

    def connect(self):
        # 创建连接
        conn = pymongo.MongoClient(self.mongo_host)
        # 连接数据库
        db = conn.wxf_test
        # 操作的表
        posts = db.record1

        return posts

    def post(self, dict_data):
        # 插入记录(每条记录的插入时间都不一样)
        posts = self.connect()

        ret = posts.insert(dict_data)
        log.info('---------------%s' % ret)

if __name__ == '__main__':
    for i in range(10):
        device_mongo = DeviceMongo()
        new_data = {"cpu_used": 20, "memory_used": 32, 'date': datetime.datetime.now()}
        device_mongo.post(new_data)
