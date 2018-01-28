# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

from conf import conf
from common.logs import logging as log
from common.code import request_result
from common.parameters import rpc_data
from common.rabbitmq_client import RabbitmqClient


class LogRpcApi(object):

    def __init__(self):

        self.rbtmq = RabbitmqClient()
        self.queue = conf.log_call_queue
        self.timeout = 60

    def label_log(self, context, parameters=None):

        try:
            rpc_body = rpc_data("log_lab_log_get", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.queue, self.timeout, rpc_body)
        except Exception, e:
            return request_result(598)

    def pod_log_list(self, context, parameters=None):

        try:
            rpc_body = rpc_data("log_pol_log_lst", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.queue, self.timeout, rpc_body)
        except Exception, e:
            return request_result(598)
