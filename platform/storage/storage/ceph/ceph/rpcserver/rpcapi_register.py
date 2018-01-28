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

        self.rpcapi_define = rpcapi_define.CephRpcManager()

        self.rpc_api.add_resource(
             'drv_hst_hst_inf', self.rpcapi_define.host_info)

        self.rpc_api.add_resource(
             'drv_ceh_mon_ini', self.rpcapi_define.cephmon_init)

        self.rpc_api.add_resource(
             'drv_ceh_mon_add', self.rpcapi_define.cephmon_add)

        self.rpc_api.add_resource(
             'drv_ceh_clt_mnt', self.rpcapi_define.cephcluster_mount)

        self.rpc_api.add_resource(
             'drv_ceh_osd_add', self.rpcapi_define.cephosd_add)

        self.rpc_api.add_resource(
             'drv_ceh_osd_del', self.rpcapi_define.cephosd_delete)

        self.rpc_api.add_resource(
             'drv_ceh_osd_rwt', self.rpcapi_define.cephosd_reweight)

        self.rpc_api.add_resource(
             'drv_ceh_pol_crt', self.rpcapi_define.cephpool_create)

        self.rpc_api.add_resource(
             'drv_ceh_pol_inf', self.rpcapi_define.cephpool_info)

        self.rpc_api.add_resource(
             'drv_ceh_dsk_crt', self.rpcapi_define.disk_create)

        self.rpc_api.add_resource(
             'drv_ceh_dsk_del', self.rpcapi_define.disk_delete)

        self.rpc_api.add_resource(
             'drv_ceh_dsk_rsz', self.rpcapi_define.disk_resize)

        self.rpc_api.add_resource(
             'drv_ceh_dsk_gow', self.rpcapi_define.rbd_growfs)

    def rpc_exec(self, rpc_body):

        try:
            return self.rpc_api.rpcapp_run(rpc_body)
        except Exception, e:
            log.error('RPC Server exec error: %s' % (e))
            return request_result(599)
