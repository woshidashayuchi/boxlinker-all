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
from common.token_localauth import token_auth

from billing.rpcapi import rpc_api as billing_rpcapi


class LevelApi(Resource):

    def __init__(self):

        self.billing_api = billing_rpcapi.BillingRpcApi()

    @time_log
    def get(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        context = context_data(token, "bil_lvl_lvl_inf", "read")

        return self.billing_api.level_info(context)


class BalanceApi(Resource):

    def __init__(self):

        self.billing_api = billing_rpcapi.BillingRpcApi()

    @time_log
    def get(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            balance_check = request.args.get('balance_check')
        except Exception, e:
            log.warning('Parameters error, reason=%s' % (e))

            return request_result(101)

        context = context_data(token, "bil_bil_usr_com", "read")

        if balance_check == 'true':
            return self.billing_api.balance_check(context)
        else:
            return self.billing_api.balance_info(context)


class RechargesApi(Resource):

    def __init__(self):

        self.billing_api = billing_rpcapi.BillingRpcApi()

    @time_log
    def post(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, "bil_bil_usr_com", "create")

        return self.billing_api.recharge_precreate(context, parameters)

    @time_log
    def get(self):

        try:
            token = request.headers.get('token')
            user_info = token_auth(token)['result']
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            recharge_type = request.args.get('recharge_type')
            start_time = request.args.get('start_time')
            end_time = request.args.get('end_time')
            page_size = request.args.get('page_size')
            page_num = request.args.get('page_num')
            parameters = {
                             "recharge_type": recharge_type,
                             "start_time": start_time,
                             "end_time": end_time,
                             "page_size": page_size,
                             "page_num": page_num
                         }
        except Exception, e:
            log.warning('Parameters error, reason=%s' % (e))

            return request_result(101)

        if user_info['user_uuid'] == 'sysadmin':
            context = context_data(token, "bil_bil_adm_com", "read")

            return self.billing_api.recharge_check(context, parameters)
        else:
            context = context_data(token, "bil_rcg_rcg_lst", "read")

            return self.billing_api.recharge_list(context, parameters)


class RechargeApi(Resource):

    def __init__(self):

        self.billing_api = billing_rpcapi.BillingRpcApi()

    @time_log
    def get(self, recharge_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        parameters = {
                         "recharge_uuid": recharge_uuid
                     }

        context = context_data(token, "bil_bil_usr_com", "read")

        return self.billing_api.recharge_info(context, parameters)


class CostsApi(Resource):

    def __init__(self):

        self.billing_api = billing_rpcapi.BillingRpcApi()

    @time_log
    def post(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, "bil_cst_cst_inf", "create")

        return self.billing_api.cost_accounting(context, parameters)


class LimitsApi(Resource):

    def __init__(self):

        self.billing_api = billing_rpcapi.BillingRpcApi()

    @time_log
    def post(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, "bil_lmt_lmt_chk", "create")

        return self.billing_api.limit_check(context, parameters)

    @time_log
    def get(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            page_size = request.args.get('page_size')
            page_num = request.args.get('page_num')
            parameters = {
                             "page_size": page_size,
                             "page_num": page_num
                         }
        except Exception, e:
            log.warning('Parameters error, reason=%s' % (e))

            return request_result(101)

        context = context_data(token, "bil_bil_usr_com", "read")

        return self.billing_api.limit_list(context, parameters)

    @time_log
    def put(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, "bil_lmt_lmt_udt", "update")

        return self.billing_api.limit_update(context, parameters)


class ResourcesApi(Resource):

    def __init__(self):

        self.billing_api = billing_rpcapi.BillingRpcApi()

    @time_log
    def post(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, "bil_rss_rss_crt", "create")

        return self.billing_api.resource_create(context, parameters)

    @time_log
    def get(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            page_size = request.args.get('page_size')
            page_num = request.args.get('page_num')
            parameters = {
                             "page_size": page_size,
                             "page_num": page_num
                         }
        except Exception, e:
            log.warning('Parameters error, reason=%s' % (e))

            return request_result(101)

        context = context_data(token, "bil_rss_rss_lst", "read")

        return self.billing_api.resource_list(context, parameters)

    @time_log
    def put(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, "bil_bil_tem_com", "update")

        return self.billing_api.resource_check(context, parameters)


class ResourceApi(Resource):

    def __init__(self):

        self.billing_api = billing_rpcapi.BillingRpcApi()

    @time_log
    def delete(self, resource_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        context = context_data(token, resource_uuid, "delete")

        return self.billing_api.resource_delete(context)

    @time_log
    def put(self, resource_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, resource_uuid, "update")

        return self.billing_api.resource_update(context, parameters)


class VouchersApi(Resource):

    def __init__(self):

        self.billing_api = billing_rpcapi.BillingRpcApi()

    @time_log
    def post(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, "bil_voc_voc_crt", "create")

        return self.billing_api.voucher_create(context, parameters)

    @time_log
    def get(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            voucher_accept = request.args.get('voucher_accept')
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

        if voucher_accept == 'true':
            context = context_data(token, "bil_bil_usr_com", "read")
            return self.billing_api.voucher_accept(context, parameters)
        else:
            context = context_data(token, "bil_voc_voc_lst", "read")
            return self.billing_api.voucher_list(context, parameters)


class VoucherApi(Resource):

    def __init__(self):

        self.billing_api = billing_rpcapi.BillingRpcApi()

    @time_log
    def post(self, voucher_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        parameters = {
                         "voucher_uuid": voucher_uuid
                     }

        context = context_data(token, "bil_voc_voc_act", "create")

        return self.billing_api.voucher_active(context, parameters)

    @time_log
    def put(self, voucher_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        parameters['voucher_uuid'] = voucher_uuid

        context = context_data(token, "bil_bil_adm_com", "update")

        return self.billing_api.voucher_distribute(context, parameters)


class BillsAPI(Resource):

    def __init__(self):

        self.billing_api = billing_rpcapi.BillingRpcApi()

    @time_log
    def get(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
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

        context = context_data(token, "bil_bls_bls_lst", "read")

        return self.billing_api.bill_list(context, parameters)


class OrdersApi(Resource):

    def __init__(self):

        self.billing_api = billing_rpcapi.BillingRpcApi()

    @time_log
    def post(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, "bil_odr_odr_crt", "create")

        return self.billing_api.order_create(context, parameters)

    @time_log
    def get(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
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

        context = context_data(token, "bil_odr_odr_lst", "read")

        return self.billing_api.order_list(context, parameters)


class OrderApi(Resource):

    def __init__(self):

        self.billing_api = billing_rpcapi.BillingRpcApi()

    @time_log
    def put(self, order_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, order_uuid, "update")

        return self.billing_api.order_update(context, parameters)


class WeiXinNotifyApi(Resource):

    @time_log
    def post(self):

        try:
            body = request.get_data()
            #parameters = json.loads(body)
            log.info('Notify data=%s' % (body))
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        return '<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>'
