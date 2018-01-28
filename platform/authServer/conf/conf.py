#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/8/30 9:54
@程序运行配置
"""

import platform
import os

sysstr = platform.system()  # Windows测试模式

CONFPATH = os.path.dirname(os.path.abspath(__file__))
# FONTTTC = CONFPATH + os.path.sep + 'SignPainter.ttc'
FONTTTC = CONFPATH + os.path.sep + 'AppleSDGothicNeo.ttc'


# 数据库是否使用测试数据库
# github 回调, DB 数据库
DEBUG = False

VERIFY_CODE = True  # 是否开启验证码; True 开启; False 关闭验证码

CONFIRM_EMAIL = True  # 是否开启邮箱认证; True 开启

Mask_Public = ['0', '1']
GLOBALS_TOKEN = dict()  # 全局的token运行存储


LOG_DEBUG = True  # 日志是输出方式; False 文件输出; True 终端输出


VERIFY_CODE_URL = 'https://verify-code.boxlinker.com/check_code/$CODE_ID?code=$CODE_STR'
# http://verify-code.boxlinker.com/check_code/c3f32490-95c0-11e6-8982-6fd924e66fdf?code=oyp8


TOKEN_TIMEOUT = 60 * 60 * 24 * 12


if 'Darwin' == sysstr:  # mac
    private_key = '/Users/lzp/Desktop/PythonTools/authServer/RegistryWeb/config/registry/private_key.pem'
elif 'Linux' == sysstr:
    private_key = '/PythonTools/authServer/RegistryWeb/config/registry/private_key.pem'

#
# AccessKeyID = "aifLgFuyz092J0WO"
# AccessKeySecret = "5IRKR16bmjQaypC54MzGtwFROXtTmN"
#
# Endpoint = 'oss-cn-shanghai.aliyuncs.com'
# RepositoryObject = 'repository'
#
# OssHost = "http://boxlinker-develop.oss-cn-shanghai.aliyuncs.com"
# OssInHost = "boxlinker-develop.oss-cn-shanghai-internal.aliyuncs.com"  # 内网地址
# BucketName = 'boxlinker-develop'





AccessKeyID = "LTAIRgaFkdGaZlVM"
AccessKeySecret = "EGv0wHzPE5cv97INkIQ4vYdqyYzxnH"
BucketName = 'boxlinker-images'

if DEBUG:
    OssHost = "http://boxlinker-images.oss-cn-beijing.aliyuncs.com"
    SEND_EMAIL_URL = 'http://email.boxlinker.com/send'
else:
    OssHost = "https://boxlinker-images.oss-cn-beijing.aliyuncs.com"
    # img.boxlinker.com
    SEND_EMAIL_URL = 'https://email.boxlinker.com/send'

Endpoint = 'oss-cn-beijing.aliyuncs.com'
RepositoryObject = 'repository'
UserObject = 'user-dir'

if DEBUG:
    # 消息队列
    queue_name = 'build_code_test'
    exchange_name = 'build_code_exchang_debug_testing'
else:
    queue_name = 'build_code_debug'
    exchange_name = 'build_code_exchang_debug_test'



callback_url = 'https://auth.boxlinker.com/api/v1.0/usercenter/users/email/$OPCODE/$ACTION'


BILLING = "https://billing.boxlinker.com"  # 计费

INITBILLING = BILLING + "/api/v1.0/billing/balances"    #  余额初始化