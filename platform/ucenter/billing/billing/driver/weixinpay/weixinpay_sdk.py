# -*- coding:utf-8 -*-

import json
import time
import uuid
from hashlib import md5

import dicttoxml
import requests
import xmltodict

from common.logs import logging as log


class WeiXinPay(object):

    def __init__(self, appid, mch_id, key, notify_url, debug=False):

        u"""
        args:
            appid: 应用id
            mch_id: 商户号
            key: API密钥
        """
        self.appid = appid
        self.mch_id = mch_id
        self.key = key
        self.notify_url = notify_url
        self.default_params = {
            'appid': appid,
        }

        if debug is True:
            self.getsignkey_url = 'https://api.mch.weixin.qq.com/sandboxnew/pay/getsignkey'
            self.unifiedorder_url = 'https://api.mch.weixin.qq.com/sandboxnew/pay/unifiedorder'
            self.orderquery_url = 'https://api.mch.weixin.qq.com/sandboxnew/pay/orderquery'
            self.closeorder_url = 'https://api.mch.weixin.qq.com/sandboxnew/pay/closeorder'
        else:
            self.unifiedorder_url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
            self.orderquery_url = 'https://api.mch.weixin.qq.com/pay/orderquery'
            self.closeorder_url = 'https://api.mch.weixin.qq.com/pay/closeorder'

    def _generate_nonce_str(self):

        u"""生成随机字符串
        """

        return str(uuid.uuid4()).replace('-', '')

    def generate_sign(self, params):

        u"""生成md5签名的参数
        """
        src = '&'.join(['%s=%s' % (k, v) for k,
                        v in sorted(params.iteritems())]) + '&key=%s' % self.key

        return md5(src.encode('utf-8')).hexdigest().upper()

    def generate_request_data(self, **kwargs):

        u"""生成统一下单请求所需要提交的数据

        https://pay.weixin.qq.com/wiki/doc/api/app/app.php?chapter=9_1

        """
        params = self.default_params.copy()
        params['mch_id'] = self.mch_id
        params['fee_type'] = 'CNY'
        params['device_info'] = 'WEB'
        # params['trade_type'] = 'APP'
        params['trade_type'] = 'NATIVE'
        params['body'] = 'Boxlinker'
        time_start = time.time()
        time_expire = time_start + 302
        params['time_start'] = str(time.strftime(
                                   "%Y%m%d%H%M%S",
                                   time.localtime(time_start)))
        params['time_expire'] = str(time.strftime(
                                    "%Y%m%d%H%M%S",
                                    time.localtime(time_expire)))
        params['notify_url'] = self.notify_url
        params['nonce_str'] = self._generate_nonce_str()
        params.update(kwargs)

        params['sign'] = self.generate_sign(params)

        return '<xml>%s</xml>' % dicttoxml.dicttoxml(params, root=False)

    def generate_prepay_order(self, **kwargs):

        u"""生成预支付交易单

        签名后的数据请求 URL地址：https://api.mch.weixin.qq.com/pay/unifiedorder
        """
        headers = {'Content-Type': 'application/xml'}
        data = self.generate_request_data(**kwargs)

        res = requests.post(self.unifiedorder_url, data=data, headers=headers)

        if res.status_code != 200:
            pass
            # return 'error'
            #return json.loads(json.dumps(xmltodict.parse(res.content)))

        result = json.loads(json.dumps(xmltodict.parse(res.content)))
        log.debug('weixin pay prepay_order exec result=%s' % (result))

        if result['xml']['return_code'] == 'SUCCESS':
            log.debug('result=%s, type=%s' % (result['xml'], type(result['xml'])))
            return result['xml']
        else:
            return result['xml']['return_msg']

    def generate_call_app_data(self, prepayid):

        u""""生成调起客户端app的请求参数
        args:
            prepayid: 预支付交易单

        https://pay.weixin.qq.com/wiki/doc/api/app/app.php?chapter=9_12&index=2
        """
        params = self.default_params.copy()
        params['partnerid'] = self.mch_id
        params['package'] = 'Sign=WXPay'
        params['noncestr'] = self._generate_nonce_str()
        params['timestamp'] = str(int(time.time()))
        params['prepayid'] = str(prepayid)
        params['sign'] = self.generate_sign(params)

        return params

    def generate_query_data(self, transaction_id='', out_trade_no=''):

        u"""生成查询订单的数据
        """
        params = self.default_params.copy()
        params['mch_id'] = self.mch_id
        params['nonce_str'] = self._generate_nonce_str()

        if transaction_id:
            params['transaction_id'] = transaction_id
        elif out_trade_no:
            params['out_trade_no'] = out_trade_no
        else:
            raise Exception(
                'generate_query_data need transaction_id or out_trade_no')

        params['sign'] = self.generate_sign(params)

        return '<xml>%s</xml>' % dicttoxml.dicttoxml(params, root=False)

    def order_query_result(self, transaction_id='', out_trade_no=''):

        u"""查询订单

        args:
            transaction_id: 微信订单号(优先使用）
            out_trade_no: 商户订单号

        https://pay.weixin.qq.com/wiki/doc/api/app/app.php?chapter=9_2&index=4

        """
        headers = {'Content-Type': 'application/xml'}
        data = self.generate_query_data(
            transaction_id=transaction_id, out_trade_no=out_trade_no)

        res = requests.post(self.orderquery_url, data=data, headers=headers)
        log.debug('weixin pay order query exec result=%s' % (res))

        if res.status_code != 200:
            #return 'error'
            pass

        result = json.loads(json.dumps(xmltodict.parse(res.content)))

        if result['xml']['return_code'] == 'SUCCESS':
            return result['xml']
        else:
            return result['xml']['return_msg']

    def verify_notify(self, **kwargs):

        u"""验证通知签名的有效性
        """
        sign = kwargs.pop('sign', '')

        if self.generate_sign(kwargs) == sign:
            return True
        else:
            return False

    def parse_notify_request(self, body):

        u"""通知请求的解析

        args:
            body: 微信异步通知的请求体
        """
        if not isinstance(body, str):
            raise Exception('body is not an xml str')

        return json.loads(json.dumps(xmltodict.parse(body)))

    def get_sandbox_key(self):

        params = {}
        params['mch_id'] = self.mch_id
        params['nonce_str'] = self._generate_nonce_str()
        params['sign'] = self.generate_sign(params)

        data = '<xml>%s</xml>' % dicttoxml.dicttoxml(params, root=False)
        headers = {'Content-Type': 'application/xml'}

        res = requests.post(self.getsignkey_url, data=data, headers=headers)

        if res.status_code != 200:
            log.debug('get sandbox key exec error, result=%s' % (res))
            return json.loads(json.dumps(xmltodict.parse(res.content)))

        result = json.loads(json.dumps(xmltodict.parse(res.content)))
        log.debug('Get weixin pay sandbox key exec result=%s' % (result))

        if result['xml']['return_code'] == 'SUCCESS':
            return result['xml']
        else:
            return result['xml']['return_msg']
