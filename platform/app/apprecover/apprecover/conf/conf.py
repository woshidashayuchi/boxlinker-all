# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>


service_name = 'Ucenter'

log_level = 'INFO'
log_file = '/var/log/cloud.log'

recover_url = 'https://ucenter.boxlinker.com/api/v1.0/billing/balances?balance_check=true'

recover_login = 'https://ucenter.boxlinker.com/api/v1.0/ucenter/tokens'

user = 'service'
password = 'c2VydmljZUAyMDE3\n'


# mq_server01 = 'boxlinker.com'
# mq_server02 = 'boxlinker.com'
# mq_port = 30001
#
# db_server01 = 'boxlinker.com'
# db_server02 = 'boxlinker.com'
# db_port = 30000

mq_server01 = 'rabbitmq'
mq_server02 = 'rabbitmq'
mq_port = 5672

db_server01 = 'database'
db_server02 = 'database'
db_port = 3306
db_user = 'cloudsvc'
db_passwd = 'cloudsvc'
database = 'servicedata'
call_queue = 'zero_services_list'
queue1 = 'kubernetes_api'
queue2 = 'ks_call_api'

SERVICE_URL = 'http://k8s-test:9000/api/v1.0/application/services'

BILLING_URL = 'https://ucenter.boxlinker.com/api/v1.0/billing/resources'
ucenter_api = 'https://ucenter.boxlinker.com/api/v1.0/ucenter/tokens'
IMAGE_S = 'imageauth:8001'
IMAGE_H = 'index.boxlinker.com/'

billing_api = 'https://ucenter.boxlinker.com'
# k8s_api = 'https://api.boxlinker.com/api/v1.0/application/services'
k8s_api = 'http://k8s-test:9000/api/v1.0/application/services'
