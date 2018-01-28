# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import platform


# 业务数据库
sysstr = platform.system()  # Windows测试模式

queue = 'rpc_queue'

github_queue = 'gitauth_rpc_queue'

if 'Darwin' == sysstr:  # mac
    mq_server01 = '127.0.0.1'
    mq_server02 = '127.0.0.1'
elif 'Linux' == sysstr:
    mq_server01 = 'rabbitmq'
    mq_server02 = 'rabbitmq'

mq_port = 5672

log_level = 'INFO'
log_file = '/var/log/cloud.log'


issuer = "Auth Service"  # 和镜像库配置相同,用于register token生成
# private_key = '/Users/lzp/Desktop/v1.0/boxlinker-auth-test/ssl/ca.key'  # 加密
private_key = '/ImageRepo/registry/ssl/ca.key'  # 加密


# ucenter_api_prefix = 'http://192.168.1.7:8001'
ucenter_api_prefix = 'https://ucenter.boxlinker.com'
image_api_prefix = 'http://0.0.0.0:8001'


# ucenter_api = 'http://192.168.1.7:8001/api/v1.0/ucenter/tokens'
ucenter_api = 'https://ucenter.boxlinker.com/api/v1.0/ucenter/tokens'



rest_host = '0.0.0.0'
rest_port = 8001
rest_debug = True

call_queue = 'ucentercall_api'
rpc_timeout = 60


DEBUG = False
if DEBUG:
    OssHost = "http://boxlinker-images.oss-cn-beijing.aliyuncs.com"
    SEND_EMAIL_URL = 'http://email.boxlinker.com/send'
else:
    OssHost = "https://boxlinker-images.oss-cn-beijing.aliyuncs.com"
    SEND_EMAIL_URL = 'https://email.boxlinker.com/send'


class hub_db:
    charset = 'utf8'
    port = 3306
    if DEBUG:
        user = 'root'
        pawd = 'root123admin'
        cydb = 'debug'
        host = 'mysql'
        mysql_engine = 'mysql://' + user + ':' + pawd + '@' + host + ':' + str(port) + '/' + cydb + '?charset=utf8'
    else:
        host = '101.200.45.76'  # 线上
        user = 'root'
        pawd = 'root123admin'
        cydb = 'release'
        mysql_engine = 'mysql://' + user + ':' + pawd + '@' + host + ':' + str(port) + '/' + cydb + '?charset=utf8'

if DEBUG:
    db_server01 = 'mysql'
    db_server02 = 'mysql'
    database = 'debug'
else:
    db_server01 = '101.200.45.76'
    db_server02 = '101.200.45.76'
    database = 'release'


db_port = 3306
db_user = 'root'
db_passwd = 'root123admin'


# aliyun
RepositoryObject = 'repository'
AccessKeyID = 'LTAIRgaFkdGaZlVM'
AccessKeySecret = 'EGv0wHzPE5cv97INkIQ4vYdqyYzxnH'
Endpoint = 'oss-cn-beijing.aliyuncs.com'
BucketName = 'boxlinker-images'



if 'Darwin' == sysstr:  # mac
    FONTTYPE = '/Users/lzp/Desktop/PythonTools/authServer/conf/AppleSDGothicNeo.ttc'
    LOCAL_PATH = '/Users/lzp/Desktop/v1.0/pyTools/tools'
elif 'Linux' == sysstr:
    FONTTYPE = '/ImageRepo/conf/AppleSDGothicNeo.ttc'
    LOCAL_PATH = '/ImageRepo/pyTools'