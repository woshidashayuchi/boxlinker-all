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

        self.rpcapi_define_certify = rpcapi_define.CertifyRpcAPI()

        self.rpcapi_define_admin = rpcapi_define.AdminServiceRpcAPI()

        self.rpc_api.add_resource('svc_cre', self.rpcapi_define.service_create)

        self.rpc_api.add_resource('svc_query', self.rpcapi_define.service_query)

        self.rpc_api.add_resource('svc_detail', self.rpcapi_define.service_detail)

        self.rpc_api.add_resource('svc_delete', self.rpcapi_define.service_delete)

        self.rpc_api.add_resource('svc_update', self.rpcapi_define.service_update)

        self.rpc_api.add_resource('pod_msg', self.rpcapi_define.pods_message)

        self.rpc_api.add_resource('name_check', self.rpcapi_define.check_name_if_use)

        self.rpc_api.add_resource('certify_cre', self.rpcapi_define_certify.create_identify)

        self.rpc_api.add_resource('certify_query', self.rpcapi_define_certify.query_certify)

        self.rpc_api.add_resource('certify_update', self.rpcapi_define_certify.update_certify)

        self.rpc_api.add_resource('admin_services_get', self.rpcapi_define_admin.get_all_services)

    def rpc_exec(self, rpc_body):

        try:
            return self.rpc_api.rpcapp_run(rpc_body)
        except Exception, e:
            log.error('RPC Server exec error: %s' % e)
            return request_result(599)
