# -*- coding: utf-8 -*-
# Author: wangxf


service_name = 'Ucenter'


log_level = 'INFO'
log_file = '/var/log/cloud.log'

user = 'service'
password = 'c2VydmljZUAyMDE3\n'
recover_login = 'https://ucenter.boxlinker.com/api/v1.0/ucenter/tokens'
k8s_pod = 'https://api.boxlinker.com/api/v1.0/application/services/'


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

db_server01 = 'mysql'
db_server02 = 'mysql'
db_port = 3306

db_user = 'cloudalarm'
db_passwd = 'cloudalarm'
database = 'monitor_alarm'

alarm_queue = 'alarming_t'
ucenter_api = 'https://ucenter.boxlinker.com/api/v1.0/ucenter/tokens'
email_api = 'https://email.boxlinker.com/send'

GRAFANA = 'grafana-api:3000'
basesql = 'http://grafana-api:3000/api/datasources/proxy/1/query?db=k8s&q='
# basesql = 'http://grafana.boxlinker.com/api/datasources/proxy/1/query?db=k8s&q='
login_url = 'https://ucenter.boxlinker.com/api/v1.0/ucenter/tokens'
all_svc_url = 'http://k8s-test:9000/api/v1.0/application/admin/services'


####################################################################################
device_ip = '172.20.1.18,172.20.1.19,172.20.1.27,172.20.1.28'
# device_ip = '192.168.1.11,192.168.1.12,192.168.1.13,192.168.1.14,192.168.1.18,192.168.1.4'

mongo_host = 'mongodb://127.0.0.1:27017/'
