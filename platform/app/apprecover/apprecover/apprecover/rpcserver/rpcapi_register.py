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

        self.rpcapi_define = rpcapi_define.KubernetesRpcAPI()

        self.rpc_api.add_resource('zero_svc_regain', self.rpcapi_define.service_create)

        self.rpc_api.add_resource('zero_svc_query', self.rpcapi_define.service_query)

        self.rpc_api.add_resource('zero_pyh_del', self.rpcapi_define.service_delete)

    def rpc_exec(self, rpc_body):

        try:
            return self.rpc_api.rpcapp_run(rpc_body)
        except Exception, e:
            log.error('RPC Server exec error: %s' % e)
            return request_result(599)
