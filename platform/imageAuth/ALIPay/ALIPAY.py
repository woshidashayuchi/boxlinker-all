# coding: utf-8

from __future__ import absolute_import, division, print_function

import sys
import json

import requests

reload(sys)
sys.setdefaultencoding('utf-8')

from datetime import  datetime
from copy import deepcopy

# python 信息安全模块 主要用来做支付宝的
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5

# 以下是兼容python2和python3的导入
if str(sys.version[0]) == "3":
    from base64 import decodebytes, encodebytes
    from urllib import parse as urlparse
    from urllib.parse import quote_plus
    from urllib.request import urlopen
    from urllib.parse import parse_qsl
else:
    from base64 import decodestring as decodebytes
    from base64 import encodestring as encodebytes
    from urllib import quote_plus
    from urllib2 import urlopen
    from urlparse import parse_qsl


class AliPay:
    """
    alipay的Python sdk
    主要做统一收单方面的sdk
    第一步完成统一收单预创建
    """
    def __init__(self, APP_ID, APP_PRIVATE, ALI_PUBLIC, *args, **kw):
        """
        初始化的三个必选参数：APP_ID    APP_PRIVATE   ALI_PUBLIC
        如果 需要别的参数需要通过可变参数 *args, **kw 传进来  但是只用了 kw
        如果项目未上线  可以使用沙箱环境测试  请注意 这时候  appid 支付宝公钥  支付宝apk（只支持安卓不支持ios）支付宝帐号密码  都需要使用沙箱环境的对应参数
        这时候实例化的时候还必须 传入参数 debug=True
        """
        #### -------start-------- 配置参数 -------start-------- ####
        # 支付宝分配给开发者的应用ID
        self._APP_ID = APP_ID
        # 应用私钥路径
        self._APP_PRIVATE = APP_PRIVATE
        # 支付宝公钥路径
        self._ALI_PUBLIC = ALI_PUBLIC
        #### -------end-------- 配置参数 ------end-------- ####

        #### -------start-------- 固定参数 -------start-------- ####
        # 支付宝网关接口
        self.AliGateway = 'https://openapi.alipay.com/gateway.do'

        # 编码方式，官方支持gbk utf8  本sdk使用utf-8
        self.charset = 'utf-8'
        # 版本号  官方只有1.0
        self.version = '1.0'
        #### -------end-------- 固定参数 -------end-------- ####


        # 签名方式 可选RSA2和RSA，官方推荐RSA2
        self.sign_type = "RSA2"
        for k,v in kw.items():
            setattr(self, k, v)

        # debug 为True 则使用沙箱网关
        if hasattr(self, 'debug') and self.debug:
            self.AliGateway = "https://openapi.alipaydev.com/gateway.do"


    def __ordered_data(self, data):
        """
        对参数的参数做排序处理的，不用关心
        """
        complex_keys = []
        for key, value in data.items():
            if isinstance(value, dict):
                complex_keys.append(key)

        # 将字典类型的数据dump出来
        for key in complex_keys:
            data[key] = json.dumps(data[key], separators=(',', ':'))

        return sorted([(k, v) for k, v in data.items()])

    def _rsa_sign(self, unsigned_string=""):
        """
        实现签名的方法, 不用关心
        """
        with open(self._APP_PRIVATE) as fp:
            key = RSA.importKey(fp.read())
            signer = PKCS1_v1_5.new(key)
            if self.sign_type == "RSA":
                signature = signer.sign(SHA.new(unsigned_string.encode("utf8")))
            else:
                signature = signer.sign(SHA256.new(unsigned_string.encode("utf8")))
            # base64 编码，转换为unicode表示并移除回车
            sign = encodebytes(signature).decode("utf8").replace("\n", "")
            # print(sign)
            return sign


    def sign_data_with_private_key(self):
        """
        获取参数，进行处理  返回签名
        """
        unSigneddata=deepcopy(self._orderInfo)
        unSigneddata.pop("sign", None)
        unsigned_items = self.__ordered_data(unSigneddata)
        # print(unsigned_items)
        unsigned_string = "&".join("{}={}".format(k, v) for k, v in unsigned_items)

        print ('unsigned_string')
        print (unsigned_string)
        _sign = self._rsa_sign(unsigned_string=unsigned_string)


        print (_sign)


        return _sign


    def _get_order_info(self):
        """
        """
        self._orderInfo = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            # 'timestamp': '2017-03-20 10:16:30',
            'method': self._method,
            'app_id': self._APP_ID,
            'sign_type': self.sign_type,
            'version': self.version,
            'charset': self.charset,
            'biz_content': self._biz_content
            # 'notify_url': self._notify_url,
        }


    def creart_trade_precreate(self, out_trade_no, total_amount, subject, timeout_express='15m', seller_id='', *args, **kw):
        """
        创建扫码支付订单接口,
        返回 json串   关键参数有 qr_code 扫码支付的二维码地址
        out_trade_no:  商户的订单号， 小于64位，字母数字下划线构成  商户端需唯一
        seller_id: 卖家的支付宝id，如果商家就是卖家  可为空
        total_amount: 订单总金额 单位元，精确到小数点后两位
        subject： 订单标题
        body：可选 订单描述
        timeout_express: 该笔订单允许的最晚付款时间，逾期将关闭交易。
        取值范围：1m～15d。m-分钟，h-小时，d-天，1c-当天（1c-当天的情况下，无论交易何时创建，都在0点关闭）。
        该参数数值不接受小数点， 如 1.5h，可转换为 90m

        注意:如果你的一些参数需要保存到消息通知回调使用，那你可能必须组合拼接到body参数中;经测试只有这个参数不被使用并且支付宝会回调回来
        """
        self._method = 'alipay.trade.precreate'
        # self._notify_url = notify_url

        self._biz_content = {"out_trade_no": out_trade_no,
            "seller_id": seller_id,
            "total_amount": total_amount,
            "subject": "sss",
            "timeout_express": timeout_express
        }

        for k,v in kw.items():
            self._biz_content[k] = v

        self._get_order_info()
        sign = self.sign_data_with_private_key()

        ordered_items = self.__ordered_data(self._orderInfo)

        print ('ordered_items')
        print (ordered_items)
        quoted_string = "&".join("{}={}".format(k, quote_plus(v)) for k, v in ordered_items)

        print ('quoted_string')
        print (quote_plus(sign))
        print (quoted_string)
        signed_string = quoted_string + "&sign=" + quote_plus(sign)
        # signed_string = quoted_string + "&sign=" + sign

        url = self.AliGateway + "?" + signed_string

        # print ('url')
        # print (url)
        # r = urlopen(url)
        r = urlopen(url=self.AliGateway, data=signed_string)
        # r = requests.post(url=self.AliGateway, data=ordered_items)
        result = r.read().decode("utf-8")

        print ('result')
        print (result)
        result = json.loads(result)["alipay_trade_precreate_response"]

        # debug 为True 则使用沙箱网关
        if hasattr(self, 'debug') and self.debug:
            print(result)

            if result["code"] != "10000":
                e = '错误,具体原因请查阅 https://doc.open.alipay.com/docs/doc.htm?spm=a219a.7395905.0.0.xgpaDr&treeId=262&articleId=105806&docType=1'
                print(e)
                print(result["code"], result["sub_msg"])
            else:
                print('调用正确')
                print(result["code"], result["qr_code"], result["out_trade_no"])

        return result


    def _verify(self, sign_type="RSA2", raw_content="", signature=""):
        """
        计算签名
        """
        with open(self._ALI_PUBLIC) as fp:
            key = RSA.importKey(fp.read())
            signer = PKCS1_v1_5.new(key)
            if sign_type == "RSA":
                digest = SHA.new()
            else:
                digest = SHA256.new()
            digest.update(raw_content.encode("utf8"))
            if signer.verify(digest, decodebytes(signature.encode("utf8"))):
                self.notice['code'] = '200'
                return self.notice
            return {'code': '400'}


    def verify_notify(self, mes):
        """
        通知验证接口 (验证消息是否扫支付宝发来的且没有篡改)
        传入的 为收到的json串
        返回 True or False  代表验证正确或失败   验证失败直接忽略这条信息;验证通过最好再确认下 订单号和金额是否对
        卖家有关信息  app_id 开发者的app_id  seller_id  卖家支付宝用户号  seller_email 卖家支付宝账号
        买家有关信息 buyer_id 买家支付宝用户号  buyer_logon_id 买家支付宝帐号
        传过去的参数  version 版本号 total_amount 订单金额  subject 商品标题   sign_type 加密方式 charset 编码方式  out_trade_no  商户订单号（64）
        金额信息   buyer_pay_amount 付款金额  point_amount 集分宝金额  invoice_amount 开票金额  receipt_amount 	实收金额  fund_bill_list 支付金额信息  amount 支付金额
        时间有关信息  notify_time 通知时间  gmt_payment 交易付款时间(Date)  sign 签名  gmt_create 交易创建时间
        重点信息   total_amount   out_trade_no  trade_status 交易状态(32) trade_no 支付宝交易号
        剩余信息   open_id 文档未说明参数      auth_app_id 文档未说明参数  notify_type 通知类型(64) fundChannel 支付渠道   notify_id 通知id
        """
        self.notice = dict(parse_qsl(mes))
        # print(res)
        __sign = self.notice.pop("sign", None)
        __sign_type = self.notice.pop("sign_type", None)

        print (__sign)
        print (__sign_type)
        if not all([__sign, __sign_type]):
            # 参数不合法
            response = list()
            response['code'] = '401'
            response['mes'] = '验签失败:关键参数缺少'
            return response
        unsigned_items = self.__ordered_data(self.notice)
        message = "&".join("{}={}".format(k, v) for k, v in unsigned_items)
        # print(message)
        return self._verify(sign_type=__sign_type, raw_content=message, signature=__sign)


if '__main__' == __name__:
    # 扫码支付 下单
    ali = AliPay(APP_ID='2016080200149684',
                 APP_PRIVATE='/Users/lzp/Desktop/PythonTools/ALIPay/private.pem',
                 ALI_PUBLIC='/Users/lzp/Desktop/PythonTools/ALIPay/public .pem',
                 debug=True)
    ali.creart_trade_precreate(out_trade_no='2446422226278',
                               total_amount=1,
                               subject='sss')
    # #消息回调的验证签名
    # mes = r'message'
    # ali.verify_notify(mes)
