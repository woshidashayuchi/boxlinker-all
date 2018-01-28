# -*- coding: utf-8 -*-
# Author: Wang-xf <it-wangxf@all-reach.com>

service_name = 'Ucenter'
call_queue = 'rolling_up'
log_level = 'INFO'
log_file = '/var/log/cloud.log'


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

db_server01 = 'database02'
db_server02 = 'database02'
db_port = 3306
rolling_up = 'rolling_update'


db_user = 'cloudsvc'
db_passwd = 'cloudsvc'
database = 'servicedata'

IMAGE_S = 'imageauth:8001'
# IMAGE_S = 'imageauth:8843'
IMAGE_H = 'index.boxlinker.com/'
