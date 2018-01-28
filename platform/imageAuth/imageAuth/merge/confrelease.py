# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import platform


# 业务数据库
sysstr = platform.system()  # Windows测试模式


log_level = 'INFO'
log_file = '/var/log/cloud.log'

db_server01 = '101.200.45.76'
db_server02 = '101.200.45.76'

db_port = 3306
db_user = 'root'
db_passwd = 'root123admin'
database = 'release'
