# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/02/17


"""
@apiDefine CODE_DELETE_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": "service deleted successfully"
}
"""
"""
@apiDefine CODE_POST_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": "service is creating"
}
"""

"""
@apiDefine CODE_UPDATE_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": "service update successfully"
}
"""
"""
@apiDefine CODE_GET_POD_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result":[{"pod_phase": "Pending",
               "pod_ip": "172.16.77.12",
               "pod_name": "newxxx-h0jn6",
               "containers": [{"access_mode": "TCP",
                               "protocol": "TCP",
                               "container_port": 2000},
                              {"access_mode": "HTTP",
                               "protocol": "TCP",
                               "container_port": 3000}]}]
}
"""
"""
@apiDefine CODE_LIST_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": [{"service_name": "aaa",
                "ltime": "56秒前",
                "container":
                    [{"http_domain": "None",
                      "tcp_domain": "lb1.boxlinker.com:30000",
                      "container_port": 2000},
                      {"http_domain": "wangxiaofeng-newaaa.lb1.boxlinker.com",
                       "tcp_domain": "None", "container_port": 3000}],
                "image_dir": "None",
                "service_status": null},

                {"service_name": "bbb",
                "ltime": "58秒前",
                "container":
                    [{"http_domain": "None",
                      "tcp_domain": "lb1.boxlinker.com:30000",
                      "container_port": 2000},
                      {"http_domain": "wangxiaofeng-newaaa.lb1.boxlinker.com",
                       "tcp_domain": "None", "container_port": 3000}],
                "image_dir": "None",
                "service_status": null}]
}
"""
"""
@apiDefine CODE_DETAIL_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {"container": [{"protocol": "TCP",
                              "uuid": "2a319d97-d1e0-47de-8a45-5cfb113481f5",
                              "rc_uuid": "ff1bcfb5-ca13-44e0-9630-d70bef4739e6",
                              "http_domain": "None",
                              "tcp_port": "30000",
                              "access_scope": "outsisde",
                              "container_port": 2000,
                              "identify": null,
                              "tcp_domain": "lb1.boxlinker.com:30000",
                              "private_domain": null,
                              "access_mode": "TCP"},
                             {"protocol": "TCP",
                              "uuid": "708b0b7a-9961-46ea-88dd-e3a8148f0492",
                              "rc_uuid": "ff1bcfb5-ca13-44e0-9630-d70bef4739e6",
                              "http_domain": "wangxiaofeng-newaaa.lb1.boxlinker.com",
                              "tcp_port": "None",
                              "access_scope": "outsisde",
                              "container_port": 3000,
                              "identify": null,
                              "tcp_domain": "None",
                              "private_domain": null,
                              "access_mode": "HTTP"}],
             "env": [{"env_key": "aaa",
                      "env_value": "bbb",
                      "rc_uuid": "ff1bcfb5-ca13-44e0-9630-d70bef4739e6",
                      "uuid": "07fc92f5-171a-48d1-8688-c2df3b8fa8e7"},
                     {"env_key": "ccc",
                      "env_value": "ddd",
                      "rc_uuid": "ff1bcfb5-ca13-44e0-9630-d70bef4739e6",
                      "uuid": "4ea8f78f-d234-4e99-b818-75e71f5d7db6"}],
             "volume": [{"readonly": "True",
                         "volume_uuid": "d54470f6-e3d2-4fbb-8d17-34f321311522",
                         "uuid": "124970e5-2869-4fee-a3c6-6d6c078d7883",
                         "disk_path": "/data",
                         "rc_uuid": "ff1bcfb5-ca13-44e0-9630-d70bef4739e6"}],
             "image_id": "1359447b-3327-3a69-bec0-cdf7d4f6c6df",
             "ltime": "6\u5206\u949f\u524d",
             "command": "",
             "pods_num": 1,
             "policy": 1,
             "container_memory": "50M",
             "isUpdate": 1,
             "auto_startup": 1,
             "uuid": "ff1bcfb5-ca13-44e0-9630-d70bef4739e6",
             "service_uuid": "3266a136-c956-4860-81c4-4e1d9720f9a2",
             "container_cpu": "1",
             "labels_name": "newaaa"
             }
}
"""


###################################################################
#                                                                 #
###################################################################



"""
@api {post} /api/v1.0/application/services 1.1 创建服务
@apiName service create
@apiGroup 1 create
@apiVersion 1.0.0
@apiDescription 服务创建
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
     "service_name":"aaa"
     "image_name":"index.boxlinker.com/boxlinker/web-index",
     "image_version":"latest",
     "policy":1,
     "pods_num":1,
     "containerNum":1,
     "isUpdate":1,
     "auto_startup":1,
     "image_id":"1359447b-3327-3a69-bec0-cdf7d4f6c6df",
     "command":"",
     "container_cpu":1,
     "container_memory":"50M",
     "container":[{"container_port":3000,
                   "protocol":"TCP",
                   "access_mode":"HTTP",
                   "access_scope":"outsisde"},
                  {"container_port":2000,
                   "protocol":"TCP",
                   "access_mode":"TCP",
                   "access_scope":"outsisde"}],
     "env":[{"env_key":"aaa",
             "env_value":"bbb"},
            {"env_key":"ccc",
             "env_value":"ddd"}],
     "volume":[{"volume_uuid":"d54470f6-e3d2-4fbb-8d17-34f321311522",
                "readonly":"True",
                "disk_path":"/data"}]
}
@apiUse CODE_POST_0
"""


"""
@api {get} /api/v1.0/application/services 2.1 服务列表
@apiName service list
@apiGroup 2 query
@apiVersion 1.0.0
@apiDescription 服务列表
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiUse CODE_LIST_0
"""
"""
@api {get} /api/v1.0/application/services?service_name=<service_name> 2.2 服务列表模糊查询
@apiName service list
@apiGroup 2 query
@apiVersion 1.0.0
@apiDescription 服务列表模糊查询
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiUse CODE_LIST_0
"""

"""
@api {get} /api/v1.0/application/services/<service_uuid> 2.3 服务详情
@apiName service details
@apiGroup 2 query
@apiVersion 1.0.0
@apiDescription 服务详情
@apiPermission project
@apiParam {json} header {"token": "string"}
@apiUse CODE_DETAIL_0
"""
"""
@api {delete} /api/v1.0/application/services/<service_uuid> 3.1 删除服务
@apiName service delete
@apiGroup 3 delete
@apiVersion 1.0.0
@apiDescription 删除服务
@apiPermission project
@apiParam {json} header {"token": "string"}
@apiUse CODE_DELETE_0
"""

"""
@api {put} /api/v1.0/application/services/<service_uuid>?rtype=container 4.1 pod容器更新
@apiName container update
@apiGroup 4 update
@apiVersion 1.0.0
@apiDescription 更新pod内容器相关信息
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "container":[
        {"container_port":3000,
         "protocol":"TCP",
         "access_mode":"HTTP",
         "access_scope":"outsisde"},
        {"container_port":2000,
         "protocol":"TCP",
         "access_mode":"TCP",
         "access_scope":"outsisde"}
    ]
}
@apiUse CODE_UPDATE_0
"""
"""
@api {put} /api/v1.0/application/services/<service_uuid>?rtype=env 4.2 环境变量更新
@apiName env update
@apiGroup 4 update
@apiVersion 1.0.0
@apiDescription 更新服务的环境变量
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "env":[
        {"env_key":"string",
         "env_value":"string"},
        {"env_key":"string",
         "env_value":"string"}
    ]
}
@apiUse CODE_UPDATE_0
"""


"""
@api {put} /api/v1.0/application/services/<service_uuid>?rtype=volume 4.3 存储卷更新
@apiName volume update
@apiGroup 4 update
@apiVersion 1.0.0
@apiDescription 更新服务的存储卷
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "volume":[
        {"volume_uuid":"string",
         "disk_path":"string",
         "readonly":"True/False"},
        {"volume_uuid":"string",
         "disk_path":"string",
         "readonly":"True/False"}
    ]
}
@apiUse CODE_UPDATE_0
"""
"""
@api {put} /api/v1.0/application/services/<service_uuid>?rtype=status 4.4 服务状态更新
@apiName status update
@apiGroup 4 update
@apiVersion 1.0.0
@apiDescription 更新服务的状态
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "data":"waiting"
}
@apiUse CODE_UPDATE_0
"""
"""
@api {put} /api/v1.0/application/services/<service_uuid>?rtype=publish 4.8 服务发布更新
@apiName status update
@apiGroup 4 update
@apiVersion 1.0.0
@apiDescription 更新服务是否自动发布
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "policy":1
}
与
{
    "policy":0,
    "image_id":int
}
@apiUse CODE_UPDATE_0
"""
"""
@api {put} /api/v1.0/application/services/<service_uuid>?rtype=telescopic 4.5 服务伸缩
@apiName telescopic update
@apiGroup 4 update
@apiVersion 1.0.0
@apiDescription 更新服务的pod数量
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "pods_num":int
}
@apiUse CODE_UPDATE_0
"""
"""
@api {put} /api/v1.0/application/services/<service_uuid>?rtype=command 4.6 服务启动命令
@apiName command update
@apiGroup 4 update
@apiVersion 1.0.0
@apiDescription 更新服务的启动命令
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "command":"string"
}
@apiUse CODE_UPDATE_0
"""
"""
@api {put} /api/v1.0/application/services/<service_uuid>?rtype=domain 4.7 服务启动命令
@apiName domain update
@apiGroup 4 update
@apiVersion 1.0.0
@apiDescription 更新服务的域名
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "domain":"string"
}
@apiUse CODE_UPDATE_0
"""

"""
@api {get} api/v1.0/application/services/<service_uuid>?pod=pod 5.1 查询服务的pod信息
@apiName pods read
@apiGroup 5 read_pods
@apiVersion 1.0.0
@apiDescription pods信息查询
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_GET_POD_0
"""