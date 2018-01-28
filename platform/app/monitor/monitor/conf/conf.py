# -*- coding: utf-8 -*-
# Author: YanHua <it-wangxf@all-reach.com>

service_name = 'Ucenter'

log_level = 'INFO'
log_file = '/var/log/cloud.log'

# mq_server01 = 'boxlinker.com'
# mq_server02 = 'boxlinker.com'
# mq_port = 30001

mq_server01 = 'rabbitmq'
mq_server02 = 'rabbitmq'
mq_port = 5672

# db_server01 = 'boxlinker.com'
# db_server02 = 'boxlinker.com'
# db_port = 30000
db_server01 = 'database'
db_server02 = 'database'
db_port = 3306
db_user = 'cloudsvc'
db_passwd = 'cloudsvc'
database = 'servicedata'

# ucenter_api = 'https://ucenter.boxlinker.com/api/v1.0/ucenter/tokens'
ucenter_api = 'https://ucenter.boxlinker.com/api/v1.0/ucenter/tokens'
rest_host = '0.0.0.0'
rest_port = 8001
rest_debug = True

call_queue = 'kubernetescall_api'
rpc_timeout = 60

STORAGE_HOST = 'https://storage.boxlinker.com/api/v1.0/storage/volumes'
storage_call_queue = 'storage_call_api'
#TEAM_MSG = 'https://ucenter.boxlinker.com/api/v1.0/ucenter/teams'
TEAM_MSG = 'http://ucenter:8001/api/v1.0/ucenter/teams'
#VOLUMEIP = '192.168.1.5:5000,192.168.1.8:5000,192.168.1.9:5000'
VOLUMEIP = '10.10.10.11:5000,10.10.10.12:5000,10.10.10.21:5000'
IMAGE_SERVER = 'https://imageauth.boxlinker.com/api/v1.0/imagerepo/image/image_uuid/public_info'


GRAFANA = 'grafana-api:3000'