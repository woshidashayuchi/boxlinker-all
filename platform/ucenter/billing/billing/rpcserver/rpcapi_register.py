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

        self.rpcapi_define = rpcapi_define.BillingRpcManager()

        self.rpc_api.add_resource(
             'bil_lvl_lvl_ini', self.rpcapi_define.level_init)

        self.rpc_api.add_resource(
             'bil_lvl_lvl_inf', self.rpcapi_define.level_info)

        self.rpc_api.add_resource(
             'bil_blc_blc_add', self.rpcapi_define.balance_init)

        self.rpc_api.add_resource(
             'bil_blc_blc_inf', self.rpcapi_define.balance_info)

        self.rpc_api.add_resource(
             'bil_blc_blc_chk', self.rpcapi_define.balance_check)

        self.rpc_api.add_resource(
             'bil_rcg_rcg_pcr', self.rpcapi_define.recharge_precreate)

        self.rpc_api.add_resource(
             'bil_rcg_rcg_crt', self.rpcapi_define.recharge_create)

        self.rpc_api.add_resource(
             'bil_rcg_rcg_lst', self.rpcapi_define.recharge_list)

        self.rpc_api.add_resource(
             'bil_rcg_rcg_inf', self.rpcapi_define.recharge_info)

        self.rpc_api.add_resource(
             'bil_rcg_rcg_chk', self.rpcapi_define.recharge_check)

        self.rpc_api.add_resource(
             'bil_cst_cst_inf', self.rpcapi_define.cost_accounting)

        self.rpc_api.add_resource(
             'bil_lmt_lmt_chk', self.rpcapi_define.limit_check)

        self.rpc_api.add_resource(
             'bil_lmt_lmt_lst', self.rpcapi_define.limit_list)

        self.rpc_api.add_resource(
             'bil_lmt_lmt_udt', self.rpcapi_define.limit_update)

        self.rpc_api.add_resource(
             'bil_rss_rss_crt', self.rpcapi_define.resource_create)

        self.rpc_api.add_resource(
             'bil_rss_rss_del', self.rpcapi_define.resource_delete)

        self.rpc_api.add_resource(
             'bil_rss_rss_put', self.rpcapi_define.resource_update)

        self.rpc_api.add_resource(
             'bil_rss_rss_lst', self.rpcapi_define.resource_list)

        self.rpc_api.add_resource(
             'bil_rss_rss_chk', self.rpcapi_define.resource_check)

        self.rpc_api.add_resource(
             'bil_voc_voc_crt', self.rpcapi_define.voucher_create)

        self.rpc_api.add_resource(
             'bil_voc_voc_udt', self.rpcapi_define.voucher_distribute)

        self.rpc_api.add_resource(
             'bil_voc_voc_acp', self.rpcapi_define.voucher_accept)

        self.rpc_api.add_resource(
             'bil_voc_voc_act', self.rpcapi_define.voucher_active)

        self.rpc_api.add_resource(
             'bil_voc_voc_lst', self.rpcapi_define.voucher_list)

        self.rpc_api.add_resource(
             'bil_bls_bls_lst', self.rpcapi_define.bill_list)

        self.rpc_api.add_resource(
             'bil_odr_odr_crt', self.rpcapi_define.order_create)

        self.rpc_api.add_resource(
             'bil_odr_odr_put', self.rpcapi_define.order_update)

        self.rpc_api.add_resource(
             'bil_odr_odr_lst', self.rpcapi_define.order_list)

    def rpc_exec(self, rpc_body):

        try:
            return self.rpc_api.rpcapp_run(rpc_body)
        except Exception, e:
            log.error('RPC Server exec error: reason=%s' % (e))
            return request_result(599)
