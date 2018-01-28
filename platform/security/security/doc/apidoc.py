#! /usr/bin python
# -*- coding:utf8 -*-
# Date:2016-08-31
# Author: YanHua


"""
@apiDefine CODE_GET_INFO_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "operations_list": [
            {
                "user_uuid": "string",
                "user_name": "string",
                "source_ip": "string",
                "resource_uuid": "string",
                "resource_name": "string",
                "resource_type": "string",
                "action": "string",
                "return_code": int,
                "return_msg": "string",
                "start_time": "YYYY-MM-DD HH:MM:SS",
                "end_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                "user_uuid": "string",
                "user_name": "string",
                "source_ip": "string",
                "resource_uuid": "string",
                "resource_name": "string",
                "resource_type": "string",
                "action": "string",
                "return_code": int,
                "return_msg": "string",
                "start_time": "YYYY-MM-DD HH:MM:SS",
                "end_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                "user_uuid": "string",
                "user_name": "string",
                "source_ip": "string",
                "resource_uuid": "string",
                "resource_name": "string",
                "resource_type": "string",
                "action": "string",
                "return_code": int,
                "return_msg": "string",
                "start_time": "YYYY-MM-DD HH:MM:SS",
                "end_time": "YYYY-MM-DD HH:MM:SS"
            }
        ]
    }
}
"""


"""
@apiDefine CODE_GET_LIST_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "count": int,
        "operations_list": [
            {
                "user_uuid": "string",
                "user_name": "string",
                "source_ip": "string",
                "resource_uuid": "string",
                "resource_name": "string",
                "resource_type": "string",
                "action": "string",
                "return_code": int,
                "return_msg": "string",
                "start_time": "YYYY-MM-DD HH:MM:SS",
                "end_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                "user_uuid": "string",
                "user_name": "string",
                "source_ip": "string",
                "resource_uuid": "string",
                "resource_name": "string",
                "resource_type": "string",
                "action": "string",
                "return_code": int,
                "return_msg": "string",
                "start_time": "YYYY-MM-DD HH:MM:SS",
                "end_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                "user_uuid": "string",
                "user_name": "string",
                "source_ip": "string",
                "resource_uuid": "string",
                "resource_name": "string",
                "resource_type": "string",
                "action": "string",
                "return_code": int,
                "return_msg": "string",
                "start_time": "YYYY-MM-DD HH:MM:SS",
                "end_time": "YYYY-MM-DD HH:MM:SS"
            }
        ]
    }
}
"""


###################################################################
#                       安全服务接口定义                          #
###################################################################


"""
@api {get} /api/v1.0/security/operations?start_time=<epoch_seconds>&end_time=<epoch_seconds>&page_size=<int>&page_num=<int> 1.1 操作记录(管理员)
@apiName list all operations record
@apiGroup 1 operation
@apiVersion 1.0.0
@apiDescription 管理员查询操作记录列表
@apiPermission admin
@apiParam {json} header {"token": "string"}
@apiUse CODE_GET_LIST_0
"""


"""
@api {get} /api/v1.0/security/operations?start_time=<epoch_seconds>&end_time=<epoch_seconds> 1.2 操作记录(普通用户)
@apiName list user operations record
@apiGroup 1 operation
@apiVersion 1.0.0
@apiDescription 普通用户查询操作记录列表
@apiPermission user
@apiParam {json} header {"token": "string"}
@apiUse CODE_GET_INFO_0
"""
