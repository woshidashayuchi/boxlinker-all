# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import os


mq_server01 = '127.0.0.1'
mq_server02 = '127.0.0.1'
mq_port = 5672

# mq_server01 = os.environ.get('MQ_SERVER01')
# mq_server02 = os.environ.get('MQ_SERVER02')
# mq_port = os.environ.get('MQ_PORT')


db_server01 = '127.0.0.1'
db_server02 = '127.0.0.1'
db_port = 3306
db_user = 'cloud'
db_passwd = 'cloud'
database = 'billing'

# db_server01 = os.environ.get('DB_SERVER01')
# db_server02 = os.environ.get('DB_SERVER02')
# db_port = os.environ.get('DB_PORT')
# db_user = os.environ.get('DB_USER')
# db_passwd = os.environ.get('DB_PASSWD')
# database = os.environ.get('DATABASE')

api_host = '0.0.0.0'
api_port = 8002
api_debug = True

log_level = 'WARNING'
log_file = '/var/log/cloud.log'

balance_check = True
limit_check = True

ucenter_call_queue = 'ucenter_call_api'
billing_call_queue = 'billing_call_api'
billing_cast_queue = 'billing_cast_api'

level_up_exp = {
                   1: 100,
                   2: 1000,
                   3: 10000,
                   4: 100000,
                   5: 1000000
               }

app_datum_cost = 0.02
hdd_datum_cost = 0.001
ssd_datum_cost = 0.004
bwh_datum_cost = 0.5
fip_datum_cost = 0.1
def_datum_cost = 0.02

#ali_pay_app_id = '2016080200149684'  #沙箱环境app_id
ali_pay_app_id = '2017032406390773'  #正式环境app_id
ali_pay_debug = False  #是否使用沙箱环境

weixin_pay_app_id = 'wx53a1112475d4a196'  #微信支付分配的公众账号ID
weixin_pay_mch_id = '1457863602'  #微信支付分配的商户号
weixin_pay_key = 'HA7d3gN7M51g0oe1tzV2aSxAX2FYbiE5'  #key设置路径：微信商户平台(pay.weixin.qq.com)-->账户设置-->API安全-->密钥设置
spbill_create_ip = '59.110.125.30'  #Native支付为调用微信支付API的机器IP
#spbill_create_ip = '106.38.76.170'  #本地测试
notify_url = 'https://ucenter.boxlinker.com/api/v1.0/billing/weixin/notify'  #微信支付结果发回地址
weixin_pay_debug = False  #是否使用沙箱环境
