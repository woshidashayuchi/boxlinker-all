#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 17/3/14 11:32
"""

"""
@apiDefine ResourcesStorageRetList
@apiSuccessExample 返回:
{
    "status": 0,
    "msg": "OK",
    "result":
    [
        {
            "resource_domain": "39828489-1bf6-334b-acdb-6a15bbd7c5a3s",
            "update_time": None,
            "storage_uuid": 2,
            "resource_uuid":
            "cabb719f-4a9a-475f-89f1-717231ae7eb5",
            "create_time": None,
            "team_uuid": "39828489-1bf6-334b-acdb-6a15bbd7c5a3s",
            "storage_url": "sssss",
            "resource_type": "UserAvatars'
        },
        ...
    ]
}

"""

"""
UserAvatars:    用户头像
ImageAvatars:   镜像头像
ServiceAvatars: 服务头像
"""



"""
@apiGroup  ResourcesStorage
@apiVersion 1.0.0
@apiDescription         申请上传key
@apiHeader {String} token 请求接口的token,放在请求头中
@api {post} http://192.168.1.6:8765/api/v1.0/files/policy  4.0 申请key

@apiExample {post} Example usage:
    {
        "resource_type": "UserAvatar",
        "resource_uuid": "39828489-1bf6-334b-acdb-6a15bbd7c5a3",
        "resource_domain": "boxlinker"
    }
@apiUse CODE_IMAGE_REPO_0
"""

"""
@apiGroup  ResourcesStorage
@apiVersion 1.0.0
@apiDescription         获取一类资源的信息
@apiHeader {String} token 请求接口的token,放在请求头中
@api {post} /api/v1.0/files/team_uuid  4.1 查询参数中含有team_uuid

@apiExample {post} Example usage:
    {
        "queryparameter" :
            [
                {
                    "team_uuid": "39828489-1bf6-334b-acdb-6a15bbd7c5a3s",
                    "resource_type": "UserAvatars",
                    "resource_uuid": "cabb719f-4a9a-475f-89f1-717231ae7eb5",
                    "resource_domain": "39828489-1bf6-334b-acdb-6a15bbd7c5a3s"
                },
                {
                    "team_uuid": "39828489-1bf6-334b-acdb-6a15bbd7c5a3s",
                    "resource_type": "UserAvatars",
                    "resource_uuid": "cabb719f-4a9a-475f-89f1-717231ae7eb5",
                    "resource_domain": "39828489-1bf6-334b-acdb-6a15bbd7c5a3s"
                }
            ]
    }

@apiParam {String} team_uuid       资源组织uuid
@apiParam {String} resource_type   资源类型(Favicon: 头像, ServiceIco: 服务图标)
@apiParam {String} resource_uuid   资源uuid(对应进行的uuid，服务的uuid，或者用户的组织uuid)
@apiParam {String} resource_domain 资源域(boxlinker)
@apiUse ResourcesStorageRetList
"""



"""
@apiGroup  ResourcesStorage
@apiVersion 1.0.0
@apiDescription         获取资源列表
@apiHeader {String} token 请求接口的token,放在请求头中
@api {post} /api/v1.0/files  4.2 查询参数中不含team_uuid

@apiExample {post} Example usage:
    {
        "queryparameter" :
            [
                {
                    "resource_type": "UserAvatars",
                    "resource_uuid": "cabb719f-4a9a-475f-89f1-717231ae7eb5",
                    "resource_domain": "39828489-1bf6-334b-acdb-6a15bbd7c5a3s"
                },
                {
                    "resource_type": "UserAvatars",
                    "resource_uuid": "cabb719f-4a9a-475f-89f1-717231ae7eb5",
                    "resource_domain": "39828489-1bf6-334b-acdb-6a15bbd7c5a3s"
                }
            ]
    }

@apiUse ResourcesStorageRetList
"""

#

"""
@apiGroup  ResourcesStorage
@apiVersion 1.0.0
@apiDescription         获取资源列表
@apiHeader {String} token 请求接口的token,放在请求头中
@api {get} /api/v1.0/files/{team_uuid}/{resource_type}/{resource_uuid}/{resource_domain}  4.3 资源参数中含team_uuid

@apiUse ResourcesStorageRetList
"""

"""
@apiGroup  ResourcesStorage
@apiVersion 1.0.0
@apiDescription         获取资源列表
@apiHeader {String} token 请求接口的token,放在请求头中
@api {get} /api/v1.0/files/{resource_type}/{resource_uuid}/{resource_domain}  4.4 资源参数中不含team_uuid

@apiUse ResourcesStorageRetList
"""


"""
@apiGroup  ResourcesStorage
@apiVersion 1.0.0
@apiDescription         设置一个资源
@apiHeader {String} token 请求接口的token,放在请求头中
@api {post} /api/v1.0/files/{team_uuid}/{resource_type}/{resource_uuid}/{resource_domain}  4.5 设置一个资源

@apiExample {post} Example usage:
    {
        "file_url": "file_urltest"
    }

@apiParam {String} file_url   资源的路径
@apiUse ResourcesStorageRetList
"""