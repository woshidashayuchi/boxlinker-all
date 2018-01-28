# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 17/4/14 上午11:16

from common.logs import logging as log
from common.code import request_result
from common.local_cache import LocalCache
from common.parameters import rpc_data
from common.rabbitmq_client import RabbitmqClient
from conf import conf


caches = LocalCache(1000)


class AlarmRpcClient(object):
    def __init__(self):
        self.rbtmq = RabbitmqClient()
        self.queue = conf.alarm_queue
        self.timeout = 8

    def create_service_alarm(self, context, parameters=None):
        try:
            rpc_body = rpc_data("alarm_cre", context, parameters)
            return self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)
            return request_result(598)

    def query_alarm(self, context, parameters=None):
        try:
            rpc_body = rpc_data("alarm_que", context, parameters)
            return self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)
            return request_result(598)

    def update_alarm(self, context, parameters=None):
        try:
            rpc_body = rpc_data('alarm_update', context, parameters)
            return self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason is: %s' % e)
            return request_result(598)

    def delete_alarm_svc(self, context, parameters=None):
        try:
            rpc_body = rpc_data('del_service_alarm', context, parameters)
            return self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason is: %s' % e)
            return request_result(598)

    def update_service_alarm(self, context, parameters=None):

        try:
            rpc_body = rpc_data('up_service_alarm', context, parameters)
            return self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason is: %s' % e)
            return request_result(598)

    def create_alarm(self, context, parameters=None):
        try:
            rpc_body = rpc_data('only_create_alarm', context, parameters)
            return self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason is: %s' % e)
            return request_result(598)

    def only_query_alarm(self, context, parameters=None):
        try:
            rpc_body = rpc_data('only_list_alarm', context, parameters)
            return self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason is: %s' % e)
            return request_result(598)

    def only_detail_alarm(self, context, parameters=None):
        try:
            rpc_body = rpc_data('only_detail_alarm', context, parameters)
            return self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason is: %s' % e)
            return request_result(598)

    def only_delete_alarm(self, context, parameters=None):
        try:
            rpc_body = rpc_data('only_del_alarm', context, parameters)

            return self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason is: %s' % e)
            return request_result(598)

    def only_update_alarm(self, context, parameters=None):
        log.info('222222222222-----')
        try:
            rpc_body = rpc_data('only_update_alarm', context, parameters)
            return self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason is: %s' % e)
            return request_result(598)

