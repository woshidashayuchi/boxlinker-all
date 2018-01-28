# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

from conf import conf
from common.logs import logging as log
from common.code import request_result
from common.parameters import rpc_data
from common.rabbitmq_client import RabbitmqClient


class SecurityRpcApi(object):

    def __init__(self):

        self.rbtmq = RabbitmqClient()
        self.call_queue = conf.security_call_queue
        self.cast_queue = conf.security_cast_queue
        self.timeout = 60

    def operation_create(self, context, parameters=None):

        try:
            rpc_body = rpc_data("sec_opr_rcd_crt", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.call_queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)

    def operation_list(self, context, parameters=None):

        try:
            rpc_body = rpc_data("sec_opr_rcd_lst", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.call_queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)

    def operation_info(self, context, parameters=None):

        try:
            rpc_body = rpc_data("sec_opr_rcd_inf", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.call_queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)

    def operation_update(self, context, parameters=None):

        try:
            rpc_body = rpc_data("sec_opr_rcd_udt", context, parameters)
            return self.rbtmq.rpc_cast_client(
                        self.cast_queue, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)
