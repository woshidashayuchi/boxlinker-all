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
        self.queue_c = 'kubernetes_create'
        self.timeout = 5

    def create_services(self, context, parameters=None):
        try:
            rpc_body = rpc_data('kuber_cre', context, parameters)

            return self.rbtmq.rpc_cast_client(self.queue_c, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)
            return request_result(501)

    def show_ns(self, context, parameters=None):
        try:
            rpc_body = rpc_data('ns_show', context, parameters)
            ret = self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)
            log.info('the namespace get result is: %s, type is : %s' % (ret, type(ret)))
            return json.loads(ret)
        except Exception, e:
            log.error('Rpc client exec error when get namespace...,reason=%s' % e)
            return request_result(501)

    def create_ns(self, context, parameters=None):
        try:
            rpc_body = rpc_data('ns_cre', context, parameters)

            ret = self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)

            return ret
        except Exception, e:
            log.error('Rpc client exec error when create namespace...,reason=%s' % e)
            return request_result(501)

    def get_account(self, context, parameters=None):
        try:
            rpc_body = rpc_data('account_get', context, parameters)
            ret = self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)

            return ret
        except Exception, e:
            log.error('Rpc client exec error when get secret msg...,reason=%s' % e)
            return request_result(501)

    def create_secret(self, context, parameters=None):
        try:
            rpc_body = rpc_data('secret_cre', context, parameters)

            ret = self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)
            log.info('secret create result is : %s, type is %s' % (ret, type(ret)))
            return ret
        except Exception, e:
            log.error('Rpc client exec error when create secret...,reason=%s' % e)
            return request_result(501)

    def create_account(self, context, parameters=None):
        try:
            rpc_body = rpc_data('account_cre', context, parameters)

            ret = self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)

            log.info('account create result is : %s, type is %s' % (ret, type(ret)))
            if ret.get('kind') != 'ServiceAccount':
                return False
            return True
        except Exception, e:
            log.error('Rpc client exec error when create account...,reason=%s' % e)

    def delete_service_a_rc(self, context, parameters=None):

        try:
            rpc_body = rpc_data('svc_delete', context, parameters)

            ret = self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)

            return ret
        except Exception, e:
            log.error('Rpc client exec error when delete rc and service...,reason=%s' % e)

    def get_pod_messages(self, context, parameters=None):

        try:
            rpc_body = rpc_data('pods_get', context, parameters)

            ret = self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)

            return ret
        except Exception, e:
            log.error('Rpc client exec error when get pods messages...,reason=%s' % e)

    def update_service(self, context, parameters=None):

        try:
            rpc_body = rpc_data('up_service', context, parameters)

            ret = self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)

            return ret
        except Exception, e:
            log.error('Rpc client exec error when update rc and service...reason=%s' % e)

    def get_one_re(self, context, parameters=None):

        try:
            rpc_body = rpc_data('get_one', context, parameters)

            ret = self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)

            return ret
        except Exception, e:
            log.error('Rpc client exec error when get one resource...reason=%s' % e)

    def create_ingress(self, context, parameters=None):
        try:
            rpc_body = rpc_data('cre_ingress', context, parameters)

            self.rbtmq.rpc_cast_client(self.queue_c, rpc_body)

        except Exception, e:
            log.error('Rpc client exec error when create the default ingress...reason=%s' % e)

    def get_ingress(self, context, parameters=None):
        try:
            rpc_body = rpc_data('g_default_ingress', context, parameters)

            ret = self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)

            return ret
        except Exception, e:
            log.error('Rpc client exec error when get the default ingress message...reason is: %s' % e)

    def update_ingress(self, context, parameters=None):

        try:
            rpc_body = rpc_data('up_ingress', context, parameters)
            ret = self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)

            return ret
        except Exception, e:
            log.error('Rpc client exec error when update the ingress...reason is: %s' % e)


class CertifyRpcClient(object):

    def __init__(self):
        self.rbtmq = RabbitmqClient()
        self.queue = 'kubernetes_api'
        self.timeout = 8

    def create_certify(self, context, parameters=None):
        try:
            rpc_body = rpc_data('secret_cre', context, parameters)

            ret = self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)
            log.info('create the https secret result is: %s' % ret)

            return ret
        except Exception, e:
            log.error('Rpc client exec error when create the certufy secret...reason is: %s' % e)

    def update_certify(self, context, parameters=None):
        try:
            rpc_body = rpc_data('secret_update', context, parameters)

            ret = self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)
            log.info('update the https secret result is: %s' % ret)

            return ret
        except Exception, e:
            log.error('Rpc client exec error when update the certufy secret...reason is: %s' % e)