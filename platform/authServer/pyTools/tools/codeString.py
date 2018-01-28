#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/8/11 6:49
@func: 返回码对应的文字描述
"""

# 程序执行状态码定义,分类说明如下：
# 0      OK 只有返回码为0才有result值。
# 1xx    API接口自身错误，如参数错误、接口已停用、找不到接口。
# 2xx    认证或权限错误
# 3xx    逻辑错误，如名称冲突，资源超过限额，余额不足等。
# 4xx    数据库错误
# 5xx    驱动层错误
# 6xx    系统级别错误
# 7xx    参数缺失


# from enum import Enum, unique
#
# @unique
# class OrgCode(Enum):  # 组织相关
#     ORG_NOT_EXIST = 'Organization does not exist',  # 组织不存在
#     ORG_DEFAULT = "The default organization, can't do anything",  #默认组织,不能进行任何操作
#     ORG_TOKEN_ERROR = "toekn is error, needs of the organization to operation, is not in token" # token中的组织和需要操作的不符
#

# @unique
# class UserCode(Enum):
#     USER_NAME_NOT_EXIST = 'User name does not exist'  # 用户名不存在
#




status_code = {
    0: "OK",
    100: 'api error',  # api 错误,大类 lzp
    101: 'Parameters error',
    102: 'token get_payload is error',  # lzp token解码失败
    103: 'Not the binding operation and making', # 没有和github进行绑定操作,或者上次绑定时发生错误  add lzp
    104: 'github msg is err',  # github 授权信息有误需要重新授权   add lzp
    201: 'Operation denied',
    202: 'Token is error',  # lzp token 验证失败
    203: 'Forged Signature',  # lzp 伪造签名
    204: 'Signature Expired',  # lzp  签名过期
    205: 'authentication required', # lzp 需要认证
    206: 'payload no date ', # lzp payload 中没有需要的信息
    301: 'Resource name already exists',
    401: 'Database insert error',
    402: 'Database delete error',
    403: 'Database update error',
    404: 'Database select error',
    405: 'Database no data',
    511: 'Ceph disk create failure',
    512: 'Ceph disk delete failure',
    513: 'Ceph disk resize failure',

    # add lzp
    601: 'Service internal abnormal',  # Python 异常
    602: 'An exception occurs',  # 引起Python异常



    # add lzp
    701: 'Your user name is unknown',  # 用户名不存在
    702: 'The user name has already been registered',  # 用户名已经被注册
    703: 'Your email is unknown',  # 邮箱没有被注册
    704: 'The email has already been registered',  # 邮箱已经有被注册
    705: 'User name does not exist or password mistake',  #     705: '用户名或密码错误'
    706: 'Parameters missing or wrong',  # 参数缺失或有误
    707: 'GenerateToken no username or email uid key',
    708: 'GenerateToken no email',
    709: 'GenerateToken no uid',
    710: 'request no data or data no is json type',  # lzp 请求中没有数据
    711: "User name and image name prefix don't match",  # 用户名和镜像名前缀不匹配
    712: "repository name not known to RegistryWeb",
    713: "repository is code build",   # 不是自动构建项目
    714: "image repository build is error",   # 不是自动构建项目
    715: "E-mail address is not active",      # 注册邮箱没有激活

    804: "Not Found, Resources to address does not exist",
    805: "verify code is error",  # 验证码错误
    806: "Not enough permissions",   # 权限不够
    807: "The user has are members of the organization", # 用户已经是组织成员
    808: "Users are not members of the organization",  # 用户不是是组织成员
    809: "There is no resources",  # 资源不存在
    810: "Group owners can not leave, You can delete",
    811: "Organization does not exist",
    812: "The default organization, can't do anything",
    813: "toekn is error, needs of the organization to operation, is not in token"

}


def request_result(code, ret={}):
    result = {
        "status": code,
        "msg": status_code[code],
        "result": ret
    }
    return result




if __name__ == '__main__':
    print request_result(811)