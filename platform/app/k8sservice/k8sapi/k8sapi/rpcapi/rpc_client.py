# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/02/06

import time

from common.logs import logging as log
from common.code import request_result
from common.local_cache import LocalCache
from common.parameters import rpc_data
from common.rabbitmq_client import RabbitmqClient
from conf import conf


caches = LocalCache(1000)


class KubernetesRpcClient(object):

    def __init__(self):
        self.rbtmq = RabbitmqClient()
        self.queue = conf.call_queue
        self.timeout = 60

    def create_services(self, context, parameters=None):
        try:
            rpc_body = rpc_data("svc_cre", context, parameters)
            log.info('rpc client to server data is : %s' % rpc_body)
            return self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)
            return request_result(598)

    def query_service(self, context, parameters=None):

        try:
            rpc_body = rpc_data("svc_query", context, parameters)

            return self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)
            return request_result(598)

    def detail_service(self, context, parameters=None):

        try:
            rpc_body = rpc_data("svc_detail", context, parameters)

            return self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)
            return request_result(598)

    def delete_service(self, context, parameters=None):

        try:
            rpc_body = rpc_data("svc_delete", context, parameters)

            return self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)
            return request_result(598)

    def update_service(self, context, parameters=None):

        try:
            rpc_body = rpc_data('svc_update', context, parameters)

            return self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)
            return request_result(598)

    def pod_msg(self, context, parameters=None):

        try:
            rpc_body = rpc_data('pod_msg', context, parameters)

            return self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)
            return request_result(598)

    def service_name_get(self, context, parameters=None):
        try:
            rpc_body = rpc_data('name_check', context, parameters)
            return self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('check the name if used or not error, reason is: %s' % e)
            return request_result(598)


class CertifyRpcClient(object):
    def __init__(self):
        self.rbtmq = RabbitmqClient()
        self.queue = conf.call_queue
        self.timeout = 60

    def create_certify(self, context, parameters=None):
        try:
            rpc_body = rpc_data("certify_cre", context, parameters)
            return self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)
            return request_result(598)

    def query_certify(self, context, parameters=None):
        try:
            rpc_body = rpc_data("certify_query", context, parameters)
            return self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)
            return request_result(598)

    def update_certify(self, context, parameters=None):
        try:
            rpc_body = rpc_data("certify_update", context, parameters)
            return self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)
            return request_result(598)


class AdminServiceRpcClient(object):
    def __init__(self):
        self.rbtmq = RabbitmqClient()
        self.queue = conf.call_queue
        self.timeout = 60

    def get_all_services(self, context, parameters=None):
        try:
            rpc_body = rpc_data("admin_services_get", context, parameters)
            return self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)
            return request_result(598)
