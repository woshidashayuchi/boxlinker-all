# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import rpcapi_define

from common.logs import logging as log
from common.code import request_result
from common.rpc_api import RpcAPI


class RabbitmqResponse(object):

    def __init__(self):

        self.rpc_api = RpcAPI()
        self.rpc_add_resource()

    def rpc_add_resource(self):

        self.rpcapi_define = rpcapi_define.SecurityRpcManager()

        self.rpc_api.add_resource(
             'sec_opr_rcd_crt', self.rpcapi_define.operation_create)

        self.rpc_api.add_resource(
             'sec_opr_rcd_lst', self.rpcapi_define.operation_list)

        self.rpc_api.add_resource(
             'sec_opr_rcd_inf', self.rpcapi_define.operation_info)

        self.rpc_api.add_resource(
             'sec_opr_rcd_udt', self.rpcapi_define.operation_update)

    def rpc_exec(self, rpc_body):

        try:
            return self.rpc_api.rpcapp_run(rpc_body)
        except Exception, e:
            log.error('RPC Server exec error: %s' % (e))
            return request_result(599)
