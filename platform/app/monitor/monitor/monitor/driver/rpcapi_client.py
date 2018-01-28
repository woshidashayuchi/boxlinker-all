# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/02/08
import json
from common.logs import logging as log
from common.code import request_result
from common.local_cache import LocalCache
from common.parameters import rpc_data
from common.rabbitmq_client import RabbitmqClient

caches = LocalCache(1000)


class KubernetesRpcClient(object):

    def __init__(self):
        self.rbtmq = RabbitmqClient()
        self.queue = 'kubernetes_api'
        self.timeout = 5

    def get_pod_messages(self, context, parameters=None):

        try:
            rpc_body = rpc_data('pods_get', context, parameters)

            ret = self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)

            return ret
        except Exception, e:
            log.error('Rpc client exec error when delete rc and service...,reason=%s' % e)
