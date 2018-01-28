# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

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

ucenter_api = 'https://ucenter.boxlinker.com/api/v1.0/ucenter/tokens'
# ucenter_api = 'http://ucenter:8001/api/v1.0/ucenter/tokens'
# ucenter_api1 = 'http://ucenter:8001'
rest_host = '0.0.0.0'
rest_port = 8001
rest_debug = True

call_queue = 'kubernetescall_api'
rpc_timeout = 60

STORAGE_HOST = 'https://storage.boxlinker.com/api/v1.0/storage/volumes'
storage_call_queue = 'storage_call_api'
PEOJECT_MSG = "https://ucenter.boxlinker.com/api/v1.0/ucenter/projects"
# PEOJECT_MSG = 'http://ucenter:8001/api/v1.0/ucenter/projects'
TEAM_MSG = 'https://ucenter.boxlinker.com/api/v1.0/ucenter/teams'
# TEAM_MSG = 'http://ucenter:8001/api/v1.0/ucenter/teams'
# VOLUMEIP = '192.168.1.5:5000,192.168.1.8:5000,192.168.1.9:5000'
VOLUMEIP = '10.10.10.11:5000,10.10.10.12:5000,10.10.10.21:5000'
ELASTIC_SEARCH = 'elasticsearch:9200'

IMAGE_S = 'imageauth:8001'
IMAGE_H = 'index.boxlinker.com/'


K8S_POD_API = 'https://kubernetes.default.svc:443/api/v1/pods'
K8S_EVENTS_API = 'https://kubernetes.default.svc:443/api/v1/namespaces/'
TOKEN_PATH = '/run/secrets/kubernetes.io/serviceaccount/token'

BILLING_URL = 'http://billing:8002/api/v1.0/billing/resources'
billing_api = 'http://billing:8002'
