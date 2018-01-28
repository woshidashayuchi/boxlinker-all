#! /usr/bin python
# -*- coding:utf8 -*-
# Date:2016-09-12
# Author: YanHua


"""
@apiDefine CODE_GET_USER0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "end_time": float,
        "logs_list": [
            {
                "log_info": "string",
                "pod_name": "string"
            }, 
            {
                "log_info": "string",
                "pod_name": "string"
            }, 
            {
                "log_info": "string",
                "pod_name": "string"
            }
        ]
    }
}
"""

"""
@apiDefine CODE_GET_SYS0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "end_time": float,
        "logs_list": [
            {
                "file": "string",
                "level": "string",
                "log_info": "string",
                "pod_name": "string",
                "log_time": "string",
                "time": "datetime"
            }, 
            {
                "file": "string",
                "level": "string",
                "log_info": "string",
                "pod_name": "string",
                "log_time": "string",
                "time": "datetime"
            }, 
            {
                "file": "string",
                "level": "string",
                "log_info": "string",
                "pod_name": "string",
                "log_time": "string",
                "time": "datetime"
            }
        ]
    }
}
"""


"""
@api {get} /api/v1.0/logs/labels/<label_value>?service_uuid=<service_uuid>?date_time=<epoch_seconds>&start_time=<epoch_milliseconds>&end_time=<epoch_milliseconds> 1.1 根据label查日志
@apiName Get log from label_value
@apiGroup 1 log
@apiVersion 1.0.0
@apiDescription 通过容器label_value查询日志
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_GET_SYS0
"""


"""
@api {get} /api/v1.0/logs/polling/labels/<label_value>?service_uuid=<service_uuid>?start_time=<epoch_milliseconds> 1.2 根据label轮询日志
@apiName Get log polling from label_value
@apiGroup 1 log
@apiVersion 1.0.0
@apiDescription 通过容器label_value轮询日志
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_GET_SYS0
"""
