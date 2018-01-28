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

        self.rpcapi_define = rpcapi_define.UcenterRpcManager()

        self.rpc_api.add_resource(
             'uct_usr_usr_crt', self.rpcapi_define.user_create)

        self.rpc_api.add_resource(
             'uct_usr_usr_act', self.rpcapi_define.user_activate)

        self.rpc_api.add_resource(
             'uct_usr_usr_stu', self.rpcapi_define.user_status)

        self.rpc_api.add_resource(
             'uct_usr_usr_chk', self.rpcapi_define.user_check)

        self.rpc_api.add_resource(
             'uct_usr_usr_lst', self.rpcapi_define.user_list)

        self.rpc_api.add_resource(
             'uct_usr_usr_inf', self.rpcapi_define.user_info)

        self.rpc_api.add_resource(
             'uct_usr_usr_udt', self.rpcapi_define.user_update)

        self.rpc_api.add_resource(
             'uct_rol_rol_crt', self.rpcapi_define.role_create)

        self.rpc_api.add_resource(
             'uct_rol_rol_lst', self.rpcapi_define.role_list)

        self.rpc_api.add_resource(
             'uct_rol_rol_inf', self.rpcapi_define.role_info)

        self.rpc_api.add_resource(
             'uct_rol_rol_udt', self.rpcapi_define.role_update)

        self.rpc_api.add_resource(
             'uct_rol_rol_del', self.rpcapi_define.role_delete)

        self.rpc_api.add_resource(
             'uct_usr_pwd_chg', self.rpcapi_define.password_change)

        self.rpc_api.add_resource(
             'uct_usr_pwd_fnd', self.rpcapi_define.password_find)

        self.rpc_api.add_resource(
             'uct_usr_pwd_rst', self.rpcapi_define.password_reset)

        self.rpc_api.add_resource(
             'uct_tkn_tkn_lgi', self.rpcapi_define.token_login)

        self.rpc_api.add_resource(
             'uct_tkn_tkn_swc', self.rpcapi_define.token_switch)

        self.rpc_api.add_resource(
             'uct_tkn_tkn_chk', self.rpcapi_define.token_auth)

        self.rpc_api.add_resource(
             'uct_tkn_tkn_del', self.rpcapi_define.token_delete)

        self.rpc_api.add_resource(
             'uct_tem_tem_crt', self.rpcapi_define.team_create)

        self.rpc_api.add_resource(
             'uct_tem_tem_lst', self.rpcapi_define.team_list)

        self.rpc_api.add_resource(
             'uct_tem_tem_inf', self.rpcapi_define.team_info)

        self.rpc_api.add_resource(
             'uct_tem_tem_udt', self.rpcapi_define.team_update)

        self.rpc_api.add_resource(
             'uct_tem_tem_del', self.rpcapi_define.team_delete)

        self.rpc_api.add_resource(
             'uct_pro_pro_crt', self.rpcapi_define.project_create)

        self.rpc_api.add_resource(
             'uct_pro_pro_lst', self.rpcapi_define.project_list)

        self.rpc_api.add_resource(
             'uct_pro_pro_inf', self.rpcapi_define.project_info)

        self.rpc_api.add_resource(
             'uct_pro_pro_udt', self.rpcapi_define.project_update)

        self.rpc_api.add_resource(
             'uct_pro_pro_del', self.rpcapi_define.project_delete)

        self.rpc_api.add_resource(
             'uct_usr_tem_add', self.rpcapi_define.user_team_add)

        self.rpc_api.add_resource(
             'uct_usr_tem_lst', self.rpcapi_define.user_team_list)

        self.rpc_api.add_resource(
             'uct_usr_tem_act', self.rpcapi_define.user_team_activate)

        self.rpc_api.add_resource(
             'uct_usr_tem_udt', self.rpcapi_define.user_team_update)

        self.rpc_api.add_resource(
             'uct_usr_tem_del', self.rpcapi_define.user_team_delete)

        self.rpc_api.add_resource(
             'uct_usr_pro_add', self.rpcapi_define.user_project_add)

        self.rpc_api.add_resource(
             'uct_usr_pro_lst', self.rpcapi_define.user_project_list)

        self.rpc_api.add_resource(
             'uct_usr_pro_udt', self.rpcapi_define.user_project_update)

        self.rpc_api.add_resource(
             'uct_usr_pro_del', self.rpcapi_define.user_project_delete)

    def rpc_exec(self, rpc_body):

        try:
            return self.rpc_api.rpcapp_run(rpc_body)
        except Exception, e:
            log.error('RPC Server exec error: %s' % (e))
            return request_result(599)
