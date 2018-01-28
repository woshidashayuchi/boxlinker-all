# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 17/3/28 下午5:13

from common.logs import logging as log
from common.rabbitmq_client import RabbitmqClient
from common.local_cache import LocalCache
from conf import conf
from common.code import request_result
caches = LocalCache(1000)


class RollingUpdate(object):

    def __init__(self):
        self.rbtmq = RabbitmqClient()
        self.queue = conf.rolling_up
        self.timeout = 5

    def rolling_update(self, context):
        try:
            log.info('to rolling update, the data is: %s' % context)
            self.rbtmq.rpc_cast_client(self.queue, context)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)
            return request_result(598)
