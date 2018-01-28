# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import os


mq_server01 = 'rabbitmq01'
mq_server02 = 'rabbitmq02'
mq_port = 5672

# mq_server01 = os.environ.get('MQ_SERVER01')
# mq_server02 = os.environ.get('MQ_SERVER02')
# mq_port = os.environ.get('MQ_PORT')


db_server01 = 'database01'
db_server02 = 'database02'
db_port = 3306
db_user = 'cloud'
db_passwd = 'cloud'
database = 'storage'

# db_server01 = os.environ.get('DB_SERVER01')
# db_server02 = os.environ.get('DB_SERVER02')
# db_port = os.environ.get('DB_PORT')
# db_user = os.environ.get('DB_USER')
# db_passwd = os.environ.get('DB_PASSWD')
# database = os.environ.get('DATABASE')

api_host = '0.0.0.0'
api_port = 8001
api_debug = False

log_level = 'WARNING'
log_file = '/var/log/cloud.log'

billing = True

storage_call_queue = 'storage_call_api'
ceph_call_queue = 'ceph_call'
ceph_exchange_name = 'ceph_bcast'

security_call_queue = 'security_call_api'
security_cast_queue = 'security_cast_api'

ucenter_api = 'https://ucenter.boxlinker.com'
billing_api = 'https://ucenter.boxlinker.com'
