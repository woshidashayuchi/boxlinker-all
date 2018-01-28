#! /usr/bin python
# -*- coding:utf8 -*-
# Date:2016-08-31
# Author: YanHua


"""
@apiDefine CODE_POST_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "volume_uuid": "string",
        "volume_name": "string",
        "pool_name": "string",
        "image_name": "string",
        "volume_size": int,
        "fs_type": "string"
    }
}
"""


"""
@apiDefine CODE_DELETE_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {}
}
"""


"""
@apiDefine CODE_PUT_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "volume_uuid": "string",
        "volume_name": "string",
        "pool_name": "string",
        "image_name": "string",
        "volume_size": int
    }
}
"""


"""
@apiDefine CODE_PUT_STATUS0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "volume_uuid": "string",
        "volume_status": "string"
    }
}
"""


"""
@apiDefine CODE_GET_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "volume_uuid": "string",
        "volume_name": "string",
        "volume_size": int,
        "volume_status": "string",
        "image_name": "string",
        "fs_type": "string",
        "mount_point": "string",
        "pool_name": "string",
        "create_time": "YYYY-MM-DD HH:MM:SS",
        "update_time": "YYYY-MM-DD HH:MM:SS"
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
        "volume_list": [
            {
                "volume_uuid": "string",
                "volume_name": "string",
                "volume_size": int,
                "volume_status": "string",
                "image_name": "string",
                "fs_type": "string",
                "mount_point": "string",
                "pool_name": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                "volume_uuid": "string",
                "volume_name": "string",
                "volume_size": int,
                "volume_status": "string",
                "image_name": "string",
                "fs_type": "string",
                "mount_point": "string",
                "pool_name": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                "volume_uuid": "string",
                "volume_name": "string",
                "volume_size": int,
                "volume_status": "string",
                "image_name": "string",
                "fs_type": "string",
                "mount_point": "string",
                "pool_name": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            }
        ]
    }
}
"""


###################################################################
#                       存储服务接口定义                          #
###################################################################


"""
@api {post} /api/v1.0/storage/volumes 1.1 存储卷创建
@apiName create volume
@apiGroup 1 storage
@apiVersion 1.0.0
@apiDescription 存储卷创建
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "volume_name": "string",
    "volume_size": int,
    "fs_type": "xfs/ext4"
}
@apiUse CODE_POST_0
"""


"""
@api {get} /api/v1.0/storage/volumes 1.2 存储卷列表
@apiName list volumes
@apiGroup 1 storage
@apiVersion 1.0.0
@apiDescription 存储卷列表查询
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_GET_LIST_0
"""


"""
@api {get} /api/v1.0/storage/volumes/<volume_uuid> 1.3 存储卷信息
@apiName list single volume
@apiGroup 1 storage
@apiVersion 1.0.0
@apiDescription 存储卷详细信息查询
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_GET_0
"""


"""
@api {put} /api/v1.0/storage/volumes/<volume_uuid>?update=<size> 1.4 存储卷更新（容量）
@apiName update volume size
@apiGroup 1 storage
@apiVersion 1.0.0
@apiDescription 存储卷容量更新
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "volume_size": int
}
@apiUse CODE_PUT_0
"""


"""
@api {put} /api/v1.0/storage/volumes/<volume_uuid>?update=<status> 1.5 存储卷更新（状态）
@apiName update volume status
@apiGroup 1 storage
@apiVersion 1.0.0
@apiDescription 存储卷状态更新
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "volume_status": "using/unused"
}
@apiUse CODE_PUT_STATUS0
"""


"""
@api {delete} /api/v1.0/storage/volumes/<volume_uuid> 1.6 存储卷删除
@apiName delete volume
@apiGroup 1 storage
@apiVersion 1.0.0
@apiDescription 存储卷删除
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_DELETE_0
"""
