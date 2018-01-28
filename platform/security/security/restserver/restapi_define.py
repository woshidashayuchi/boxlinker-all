#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import json

from flask import request
from flask_restful import Resource

from common.logs import logging as log
from common.code import request_result
from common.time_log import time_log
from common.parameters import context_data
from common.token_ucenterauth import token_auth

from security.rpcapi import rpc_api as security_rpcapi


class OperationsApi(Resource):

    def __init__(self):

        self.security_rpcapi = security_rpcapi.SecurityRpcApi()

    @time_log
    def get(self):

        try:
            token = request.headers.get('token')
            user_info = token_auth(token)['result']
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            start_time = request.args.get('start_time')
            end_time = request.args.get('end_time')
            page_size = request.args.get('page_size')
            page_num = request.args.get('page_num')
            parameters = {
                             "start_time": start_time,
                             "end_time": end_time,
                             "page_size": page_size,
                             "page_num": page_num
                         }
        except Exception, e:
            log.warning('Parameters error, reason=%s' % (e))

            return request_result(101)

        user_uuid = user_info['user_uuid']
        if user_uuid == 'sysadmin':
            context = context_data(token, "sec_sec_adm_com", "read")
            return self.security_rpcapi.operation_list(context, parameters)
        else:
            context = context_data(token, "sec_sec_usr_com", "read")
            return self.security_rpcapi.operation_info(context, parameters)
