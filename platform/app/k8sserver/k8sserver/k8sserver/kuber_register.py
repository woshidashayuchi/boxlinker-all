# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/02/07
import kuber_define

from common.logs import logging as log
from common.code import request_result
from common.rpc_api import RpcAPI


class RabbitmqResponse(object):

    def __init__(self):

        self.rpc_api = RpcAPI()
        self.rpc_add_resource()

    def rpc_add_resource(self):

        self.rpcapi_define = kuber_define.KubernetesRpcAPIs()

        self.rpc_api.add_resource('kuber_cre', self.rpcapi_define.service_crea)

        self.rpc_api.add_resource('ns_show', self.rpcapi_define.ns_show)

        self.rpc_api.add_resource('ns_cre', self.rpcapi_define.ns_cre)

        self.rpc_api.add_resource('secret_cre', self.rpcapi_define.secret_cre)

        self.rpc_api.add_resource('account_get', self.rpcapi_define.svc_account_show)

        self.rpc_api.add_resource('account_cre', self.rpcapi_define.svc_account_create)

        self.rpc_api.add_resource('svc_delete', self.rpcapi_define.svc_delete)

        self.rpc_api.add_resource('pods_get', self.rpcapi_define.pods_messages)

        self.rpc_api.add_resource('up_service', self.rpcapi_define.svc_update)

        self.rpc_api.add_resource('get_one', self.rpcapi_define.get_one_re)

        self.rpc_api.add_resource('del_ns', self.rpcapi_define.delete_ns)

        self.rpc_api.add_resource('cre_ingress', self.rpcapi_define.default_ingress)

        self.rpc_api.add_resource('g_default_ingress', self.rpcapi_define.get_default_ingress)

        self.rpc_api.add_resource('up_ingress', self.rpcapi_define.update_ingress)

        self.rpc_api.add_resource('secret_update', self.rpcapi_define.update_secret)

    def rpc_exec(self, rpc_body):

        try:
            return self.rpc_api.rpcapp_run(rpc_body)
        except Exception, e:
            log.error('RPC Server exec error: %s' % e)
            return request_result(599)
