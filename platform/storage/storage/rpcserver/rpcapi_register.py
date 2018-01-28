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

        self.rpcapi_define = rpcapi_define.StorageRpcManager()

        self.rpc_api.add_resource(
             'stg_ceh_cls_crt', self.rpcapi_define.cephcluster_create)

        self.rpc_api.add_resource(
             'stg_ceh_cls_inf', self.rpcapi_define.cephcluster_info)

        self.rpc_api.add_resource(
             'stg_ceh_cls_lst', self.rpcapi_define.cephcluster_list)

        self.rpc_api.add_resource(
             'stg_ceh_cls_mnt', self.rpcapi_define.cephcluster_mount)

        self.rpc_api.add_resource(
             'stg_ceh_hst_crt', self.rpcapi_define.host_create)

        self.rpc_api.add_resource(
             'stg_ceh_hst_del', self.rpcapi_define.host_delete)

        self.rpc_api.add_resource(
             'stg_ceh_hst_inf', self.rpcapi_define.host_info)

        self.rpc_api.add_resource(
             'stg_ceh_hst_lst', self.rpcapi_define.host_list)

        self.rpc_api.add_resource(
             'stg_ceh_mon_int', self.rpcapi_define.cephmon_init)

        self.rpc_api.add_resource(
             'stg_ceh_mon_add', self.rpcapi_define.cephmon_add)

        self.rpc_api.add_resource(
             'stg_ceh_mon_lst', self.rpcapi_define.cephmon_list)

        self.rpc_api.add_resource(
             'stg_ceh_mon_inf', self.rpcapi_define.cephmon_info)

        self.rpc_api.add_resource(
             'stg_ceh_osd_add', self.rpcapi_define.cephosd_add)

        self.rpc_api.add_resource(
             'stg_ceh_osd_del', self.rpcapi_define.cephosd_delete)

        self.rpc_api.add_resource(
             'stg_ceh_osd_rwt', self.rpcapi_define.cephosd_reweight)

        self.rpc_api.add_resource(
             'stg_ceh_osd_inf', self.rpcapi_define.cephosd_info)

        self.rpc_api.add_resource(
             'stg_ceh_osd_lst', self.rpcapi_define.cephosd_list)

        self.rpc_api.add_resource(
             'stg_ceh_pol_crt', self.rpcapi_define.cephpool_create)

        self.rpc_api.add_resource(
             'stg_ceh_pol_inf', self.rpcapi_define.cephpool_info)

        self.rpc_api.add_resource(
             'stg_ceh_pol_lst', self.rpcapi_define.cephpool_list)

        self.rpc_api.add_resource(
             'stg_ceh_dsk_crt', self.rpcapi_define.volume_create)

        self.rpc_api.add_resource(
             'stg_ceh_dsk_lst', self.rpcapi_define.volume_list)

        self.rpc_api.add_resource(
             'stg_ceh_dsk_inf', self.rpcapi_define.volume_info)

        self.rpc_api.add_resource(
             'stg_ceh_dsk_del', self.rpcapi_define.volume_delete)

        self.rpc_api.add_resource(
             'stg_ceh_dsk_udt', self.rpcapi_define.volume_update)

        self.rpc_api.add_resource(
             'stg_ceh_rcm_lst', self.rpcapi_define.volume_reclaim_list)

        self.rpc_api.add_resource(
             'stg_ceh_rcm_rcv', self.rpcapi_define.volume_reclaim_recovery)

    def rpc_exec(self, rpc_body):

        try:
            return self.rpc_api.rpcapp_run(rpc_body)
        except Exception, e:
            log.error('RPC Server exec error: %s' % (e))
            return request_result(599)
