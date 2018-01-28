# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

service_name = 'Ucenter'

log_level = 'INFO'
log_file = '/var/log/cloud.log'

mq_server01 = 'rabbitmq'
mq_server02 = 'rabbitmq'
mq_port = 5672

db_server01 = 'boxlinker.com'
db_server02 = 'boxlinker.com'
db_port = 30000
db_user = 'cloudsvc'
db_passwd = 'cloudsvc'
database = 'servicedata'

ucenter_api = 'https://ucenter.boxlinker.com/api/v1.0/ucenter/tokens'

rest_host = '0.0.0.0'
rest_port = 8001
rest_debug = True

call_queue = 'kubernetescall_api'
rpc_timeout = 60

STORAGE_HOST = 'https://storage.boxlinker.com/api/v1.0/storage/volumes'
PROJECT_MSG = 'https://ucenter.boxlinker.com/api/v1.0/ucenter/projects'
VOLUMEIP = '192.168.1.5:5000,192.168.1.8:5000,192.168.1.9:5000'

