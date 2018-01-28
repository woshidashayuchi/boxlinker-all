# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/02/07
import rpcapi_define

from common.logs import logging as log
from common.code import request_result
from common.rpc_api import RpcAPI


class RabbitmqResponse(object):

    def __init__(self):
        self.rpc_api = RpcAPI()
        self.rpc_add_resource()

    def rpc_add_resource(self):

        self.rpcapi_define = rpcapi_define.MonitorRpcAPI()

        self.rpc_api.add_resource('mon_get', self.rpcapi_define.monitor_get)

        self.rpc_api.add_resource('broad_get', self.rpcapi_define.broad_get)

    def rpc_exec(self, rpc_body):

        try:
            log.info('rpc_body==%s' % rpc_body)
            return self.rpc_api.rpcapp_run(rpc_body)
        except Exception, e:
            log.error('RPC Server exec error: %s' % e)
            return request_result(599)
