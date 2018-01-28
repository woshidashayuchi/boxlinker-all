# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import uuid
import json
import time
import datetime

import levels_manager
import balances_manager

from time import sleep

from common.logs import logging as log
from common.code import request_result
from common.json_encode import CJsonEncoder
from common.parameters import context_data

from billing.db.billing_db import BillingDB
from billing.driver.billing_driver import BillingDriver

from billing.rpcapi import rpc_api as billing_rpcapi


class RechargesManager(object):

    def __init__(self):

        self.billing_db = BillingDB()
        self.billing_driver = BillingDriver()
        self.levels_manager = levels_manager.LevelsManager()
        self.balances_manager = balances_manager.BalancesManager()
        self.billing_api = billing_rpcapi.BillingRpcApi()

    def recharge_precreate(self, token, user_name,
                           recharge_type, recharge_amount):

        recharge_uuid = str(datetime.datetime.now()).replace(
                            '-', '').replace(' ', '').replace(
                            ':', '').replace('.', '')

        log.critical('User(%s) exec recharge precreate, '
                     'recharge_uuid=%s, amount=%s'
                     % (user_name, recharge_uuid, recharge_amount))

        if recharge_type == 'zhifubao':
            # 调用支付宝预付款接口，获取付款二维码地址
            try:
                qr_code = self.billing_driver.ali_precreate(
                               recharge_uuid, recharge_amount)['qr_code']
            except Exception, e:
                log.error('exec ali precreate error, reason=%s' % (e))
                return request_result(601)

        elif recharge_type == 'weixin':
            # 调用微信预付款接口，获取付款二维码地址
            try:
                qr_code = self.billing_driver.weixin_pay_precreate(
                               recharge_uuid, recharge_amount)['code_url']
            except Exception, e:
                log.error('exec weixin precreate error, reason=%s' % (e))
                return request_result(601)

        # 通过cast方式异步调用recharge_create接口

        context = context_data(token, "bil_bil_usr_com", "create")
        parameters = {
                         "recharge_uuid": recharge_uuid,
                         "recharge_type": recharge_type,
                         "recharge_amount": recharge_amount
                     }

        self.billing_api.recharge_create(context, parameters)

        result = {
                     "recharge_uuid": recharge_uuid,
                     "recharge_type": recharge_type,
                     "recharge_amount": recharge_amount,
                     "user_name": user_name,
                     "qr_code": qr_code
                 }

        return request_result(0, result)

    def recharge_create(self, recharge_uuid,
                        recharge_type, recharge_amount,
                        team_uuid, recharge_user):

        cnt = 0
        while True:
            cnt += 1
            if cnt >= 65:
                # 调用支付接口，取消订单预支付，防止页面跳转后用户继续支付
                if recharge_type == 'zhifubao':
                    self.billing_driver.ali_pay_cancel(recharge_uuid)
                elif recharge_type == 'weixin':
                    self.billing_driver.weixin_pay_cancel(recharge_uuid)

                return

            if recharge_type == 'zhifubao':
                # 调用支付宝充值查询接口
                pay_check = self.billing_driver.ali_pay_check(recharge_uuid)
            elif recharge_type == 'weixin':
                # 调用微信充值查询接口
                pay_check = self.billing_driver.weixin_pay_check(recharge_uuid)

            if pay_check:
                break
            else:
                sleep(5)

        try:
            self.billing_db.recharge_create(
                 recharge_uuid, recharge_amount,
                 recharge_type, team_uuid, recharge_user)
        except Exception, e:
            log.error('Database insert error, reason=%s' % (e))
            log.error('Recharge create error, recharge_uuid=%s, '
                      'recharge_amount=%s, recharge_type=%s, '
                      'team_uuid=%s, recharge_user=%s'
                      % (recharge_uuid, recharge_amount,
                         recharge_type, team_uuid, recharge_user))

        experience = recharge_amount
        level_update = self.levels_manager.level_update(
                            team_uuid, experience).get('status')
        if level_update != 0:
            log.error('Level update error, team_uuid=%s, experience=%s'
                      % (team_uuid, experience))

        balance_update = self.balances_manager.balance_update(
                              team_uuid, recharge_amount).get('status')
        if balance_update != 0:
            log.error('Balance update error, team_uuid=%s, amount=%s'
                      % (team_uuid, recharge_amount))

        result = {
                     "recharge_uuid": recharge_uuid,
                     "team_uuid": team_uuid,
                     "recharge_amount": recharge_amount,
                     "recharge_type": recharge_type,
                     "recharge_user": recharge_user
                 }

        return request_result(0, result)

    def recharge_info(self, recharge_uuid, team_uuid):

        try:
            recharge_record = self.billing_db.recharge_info(
                                   recharge_uuid, team_uuid)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        try:
            recharge_amount = recharge_record[0][0]
            recharge_type = recharge_record[0][1]
            user_name = recharge_record[0][2]
            create_time = recharge_record[0][3]
        except Exception, e:
            result = 0
            return request_result(0, result)

        v_recharge_info = {
                              "recharge_uuid": recharge_uuid,
                              "recharge_amount": recharge_amount,
                              "recharge_type": recharge_type,
                              "team_uuid": team_uuid,
                              "user_name": user_name,
                              "create_time": create_time
                          }

        v_recharge_info = json.dumps(v_recharge_info, cls=CJsonEncoder)
        result = json.loads(v_recharge_info)

        return request_result(0, result)

    def recharge_list(self, team_uuid,
                      start_time, end_time,
                      page_size, page_num):

        try:
            start_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                       time.localtime(float(start_time)))
            end_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                     time.localtime(float(end_time)))
            recharge_list_info = self.billing_db.recharge_list(
                                      team_uuid, start_time, end_time,
                                      page_size, page_num)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        user_recharge_list = recharge_list_info.get('recharge_list')
        count = recharge_list_info.get('count')

        recharges_list = []
        for recharge_info in user_recharge_list:
            recharge_uuid = recharge_info[0]
            recharge_amount = recharge_info[1]
            recharge_type = recharge_info[2]
            user_name = recharge_info[3]
            create_time = recharge_info[4]

            v_recharge_info = {
                                  "team_uuid": team_uuid,
                                  "recharge_uuid": recharge_uuid,
                                  "recharge_amount": recharge_amount,
                                  "recharge_type": recharge_type,
                                  "user_name": user_name,
                                  "create_time": create_time
                              }
            v_recharge_info = json.dumps(v_recharge_info, cls=CJsonEncoder)
            v_recharge_info = json.loads(v_recharge_info)
            recharges_list.append(v_recharge_info)

        result = {"recharge_list": recharges_list}
        result["count"] = count

        return request_result(0, result)

    def recharge_check(self, user_uuid, recharge_type,
                       start_time, end_time,
                       page_size, page_num):

        if user_uuid != 'sysadmin':

            return request_result(202)

        try:
            start_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                       time.localtime(float(start_time)))
            end_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                     time.localtime(float(end_time)))
            recharge_list_info = self.billing_db.recharge_check_list(
                                      recharge_type,
                                      start_time, end_time,
                                      page_size, page_num)
            recharge_total_info = self.billing_db.recharge_check_total(
                                      recharge_type, start_time, end_time)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        user_recharge_list = recharge_list_info.get('recharge_list')
        count = recharge_list_info.get('count')
        recharges_total = recharge_total_info[0][0]
        log.debug('recharges_total_info=%s, recharges_total=%s'
                  % (recharge_total_info, recharges_total))

        result = {"recharges_total": float('%.2f' % (recharges_total))}
        result["count"] = count

        recharges_list = []
        for recharge_info in user_recharge_list:
            recharge_uuid = recharge_info[0]
            recharge_amount = recharge_info[1]
            recharge_type = recharge_info[2]
            team_uuid = recharge_info[3]
            user_name = recharge_info[4]
            create_time = recharge_info[5]

            v_recharge_info = {
                                  "team_uuid": team_uuid,
                                  "recharge_uuid": recharge_uuid,
                                  "recharge_amount": recharge_amount,
                                  "recharge_type": recharge_type,
                                  "team_uuid": team_uuid,
                                  "user_name": user_name,
                                  "create_time": create_time
                              }
            v_recharge_info = json.dumps(v_recharge_info, cls=CJsonEncoder)
            v_recharge_info = json.loads(v_recharge_info)
            recharges_list.append(v_recharge_info)

        result["recharge_list"] = recharges_list

        return request_result(0, result)
