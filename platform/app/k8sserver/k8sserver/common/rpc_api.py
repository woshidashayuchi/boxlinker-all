# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

from common.logs import logging as log
from common.code import request_result


class RpcAPI(object):

    def __init__(self):

        self.app_resources = {}

    def add_resource(self, api, resource):

        self.app_resources[api] = resource

    def rpcapp_run(self, dict_data):

        try:
            api = dict_data['api']
            context = dict_data['context']
            parameters = dict_data['parameters']
        except Exception, e:
            log.error('parameters error: %s' % e)
            return request_result(101)

        try:
            log.info('执行结果:%s'% self.app_resources[api])
            log.info('context:%s' % context)
            log.info('parameters:%s' % parameters)
            return self.app_resources[api](context, parameters)
        except Exception, e:
            log.error('RPC API routing error: %s' % e)
            return request_result(102)
