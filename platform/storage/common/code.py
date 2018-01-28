# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

# 程序执行状态码定义,分类说明如下：
# 0      OK 只有返回码为0才有result值。
# 1xx    API接口自身错误，如参数错误、接口已停用、找不到接口。
# 2xx    认证或权限错误
# 3xx    逻辑错误，如名称冲突，资源超过限额，余额不足等。
# 4xx    数据库错误
# 5xx    驱动层错误
# 6xx    系统级别错误

import json

status_code = {
        0:   "OK",
        101: "Parameters error",
        102: "RPC API routing error",
        103: "Http requests error",
        104: "Verify code error",
        201: "Authentication failure",
        202: "Operation denied",
        203: "User not exists",
        204: "User not active",
        301: "Resource name already exists",
        302: "Balance not enough",
        303: "Limit denied",
        401: "Database insert error",
        402: "Database delete error",
        403: "Database update error",
        404: "Database select error",
        501: "Kubernetes resource create failure",
        502: "Kubernetes resource update failure",
        503: "Kubernetes resource delete failure",
        511: "Ceph disk create failure",
        512: "Ceph disk delete failure",
        513: "Ceph disk resize failure",
        521: "Host already exists",
        522: "Host connect timeout",
        523: "Host password not correct",
        524: "Host info get failure",
        525: "Ceph config file operation failure",
        526: "Ceph mon init install failure",
        527: "Ceph mon count reach the maximum",
        528: "Ceph mon add install failure",
        529: "Disk already used",
        530: "Ceph osd add install failure",
        531: "Ceph insufficient storage capacity",
        532: "Ceph osd delete failure",
        533: "Ceph osd reweight failure",
        534: "Ceph pool create failure",
        535: "Ceph cluster mount failure",
        597: "RabbitMQ rpc client exec timeout",
        598: "RabbitMQ rpc client exec error",
        599: "RabbitMQ rpc server exec error",
        601: "System error"
}


def request_result(code, ret={}):

    result = {
                 "status": code,
                 "msg": status_code[code],
                 "result": ret
             }

    return result
