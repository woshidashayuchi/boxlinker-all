# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import os


mq_server01 = 'rabbitmq'
mq_server02 = 'rabbitmq'
mq_port = 5672

# mq_server01 = os.environ.get('MQ_SERVER01')
# mq_server02 = os.environ.get('MQ_SERVER02')
# mq_port = os.environ.get('MQ_PORT')

db_server01 = 'database'
db_server02 = 'database'
db_port = 3306
db_user = 'cloudsvc'
db_passwd = 'cloudsvc'
database = 'servicedata'

api_host = '0.0.0.0'
api_port = 8001
api_debug = False

log_level = 'WARNING'
log_file = '/var/log/cloud.log'

log_call_queue = 'log_call_api'

ucenter_api = 'https://ucenter.boxlinker.com'
kibana_log_api = 'http://kibana:5601/elasticsearch/_msearch'
