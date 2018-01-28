# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/03/01
from common.rabbitmq_client import RabbitmqClient
from common.logs import logging as log
from common.code import request_result
from common.local_cache import LocalCache
from common.parameters import rpc_data

caches = LocalCache(1000)


class MonitorRpcClient(object):

    def __init__(self):
        self.rbtmq = RabbitmqClient()
        self.queue = 'monitorcall_monitor'
        self.queue1 = 'monitorcall_broad'
        self.timeout = 8

    def monitor_message_get(self, context, parameters=None):
        log.info('in rpc api data is:%s' % context)
        try:
            rpc_body = rpc_data('mon_get', context, parameters)

            return self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)
            return request_result(701)

    def broad_message_get(self, context, parameters=None):
        log.info('in broad monitor data is: %s' % context)

        try:
            rpc_body = rpc_data('broad_get', context, parameters)

            return self.rbtmq.rpc_call_client(self.queue1, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)
            return request_result(701)
