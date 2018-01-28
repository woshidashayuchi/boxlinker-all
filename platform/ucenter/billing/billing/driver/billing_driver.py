#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>
# github最新python alipay sdk
# https://github.com/fzlee/alipay

import os

from conf import conf
from common.logs import logging as log
from common.code import request_result

from alipay.alipay_sdk import AliPay
from weixinpay.weixinpay_sdk import WeiXinPay


class BillingDriver(object):

    def __init__(self):

        pwd_path = os.path.dirname(os.path.abspath(__file__))
        private_key_path = '%s/alipay/private.pem' % (pwd_path)
        ali_public_key_path = '%s/alipay/zhifubao_public.pem' % (pwd_path)

        self.local_wan_ip = conf.spbill_create_ip

        self.ali_pay = AliPay(appid=conf.ali_pay_app_id,
                              app_notify_url="boxlinker.com",
                              app_private_key_path=private_key_path,
                              app_alipay_public_key_path=ali_public_key_path,
                              debug=conf.ali_pay_debug)

        self.weixin_pay = WeiXinPay(appid=conf.weixin_pay_app_id,
                                    mch_id=conf.weixin_pay_mch_id,
                                    key=conf.weixin_pay_key,
                                    notify_url=conf.notify_url,
                                    debug=conf.weixin_pay_debug)

    def ali_precreate(self, recharge_uuid, amount):

        # 调用支付宝预下单接口，返回付款二维码
        log.critical('exec zhifubao precreate, recharge_uuid=%s, amount=%s'
                     % (recharge_uuid, amount))

        return self.ali_pay.precreate_face_to_face_trade(
                               out_trade_no=recharge_uuid,
                               total_amount=amount,
                               subject="boxlinker")

    def ali_pay_check(self, recharge_uuid):

        # 调用支付宝支付结果查询接口
        log.debug('exec zhifubao pay check')

        try:
            result = self.ali_pay.query_face_to_face_trade(
                                  out_trade_no=recharge_uuid)
            log.debug('ali_pay_check result=%s' % (result))
            if result.get("trade_status", "") == "TRADE_SUCCESS":
                return True
            else:
                return False
        except Exception, e:
            log.error('alipay query exec error, reason=%s' % (e))
            return False

    def ali_pay_cancel(self, recharge_uuid):

        # 调用支付宝取消预下单的支付操作
        log.critical('exec zhifubao paycancel, recharge_uuid=%s'
                     % (recharge_uuid))

        return self.ali_pay.cancel_face_to_face_trade(
                    out_trade_no=recharge_uuid)

    def ali_pay_refund(self, recharge_uuid, amount):

        # 增加充值失败退款接口
        pass

    def weixin_pay_precreate(self, recharge_uuid, amount):

        # 调用微信预下单接口，返回付款二维码
        log.critical('exec weixin precreate, recharge_uuid=%s, amount=%s'
                     % (recharge_uuid, amount))

        amount = int(float(amount) * 100)

        return self.weixin_pay.generate_prepay_order(
                               out_trade_no=recharge_uuid,
                               product_id=recharge_uuid,
                               total_fee=amount,
                               spbill_create_ip=self.local_wan_ip)

    def weixin_pay_check(self, recharge_uuid):

        # 调用微信支付结果查询接口
        log.debug('exec weixin pay check')

        try:
            result = self.weixin_pay.order_query_result(
                                  out_trade_no=recharge_uuid)
            log.debug('weixin_pay_check result=%s' % (result))
            if result.get("trade_state", "") == "SUCCESS":
                return True
            else:
                return False
        except Exception, e:
            log.error('weixin query exec error, reason=%s' % (e))
            return False

    def weixin_pay_cancel(self, recharge_uuid):

        pass

    def weixin_pay_refund(self, recharge_uuid, amount):

        pass

    def weixin_pay_get_sandbox_key(self):

        return self.weixin_pay.get_sandbox_key()
