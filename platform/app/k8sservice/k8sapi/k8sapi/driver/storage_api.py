# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

from conf import conf
from common.logs import logging as log
from common.code import request_result
from common.parameters import rpc_data
from common.rabbitmq_client import RabbitmqClient


class StorageRpcApi(object):

    def __init__(self):

        self.rbtmq = RabbitmqClient()
        self.queue = conf.storage_call_queue
        self.timeout = 60

    def disk_create(self, context, parameters=None):

        try:
            rpc_body = rpc_data("stg_ceh_dsk_crt", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)

    def disk_list(self, context, parameters=None):

        try:
            rpc_body = rpc_data("stg_ceh_dsk_lst", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)

    def disk_info(self, context, parameters=None):

        try:
            rpc_body = rpc_data("stg_ceh_dsk_inf", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)

    def disk_update(self, context, parameters=None):

        try:
            rpc_body = rpc_data("stg_ceh_dsk_udt", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)

    def disk_delete(self, context, parameters=None):

        try:
            rpc_body = rpc_data("stg_ceh_dsk_del", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)
