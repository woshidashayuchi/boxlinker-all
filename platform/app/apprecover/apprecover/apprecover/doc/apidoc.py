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
    "result": "service is recovering..."
}
"""

"""
@apiDefine CODE_DELETE_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": "service delete successfully"
}
"""
"""
@apiDefine CODE_GET_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": [{"service_name": "test001",
                "ltime": "2\u5929\u524d",
                "service_uuid": "bde7610f-2243-4596-aa89-761a8280c950"},
                {"service_name": "test002",
                "ltime": "2\u5929\u524d",
                "service_uuid": "bde7610f-2243-4596-aa89-761a8280c951"}]
}
"""

###################################################################
#                                                                 #
###################################################################


"""
@api {get} /api/v1.0/application/services 1.1 获取逻辑删除的服务列表
@apiName service list
@apiGroup 1 list
@apiVersion 1.0.0
@apiDescription 服务获取
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiUse CODE_GET_0
"""


"""
@api {post} /api/v1.0/application/services 2.1 恢复逻辑删除的服务
@apiName service recover
@apiGroup 2 create
@apiVersion 1.0.0
@apiDescription 服务列表
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{"service_uuid":
    ["bde7610f-2243-4596-aa89-761a8280c950",
     "bde7610f-2243-4596-aa89-761a8280c951"],
    "cost":-1}
@apiUse CODE_POST_0
"""
"""
@api {delete} /api/v1.0/application/services 2.2 回收站服务删除
@apiName service list
@apiGroup 2 query
@apiVersion 1.0.0
@apiDescription 服务列表模糊查询
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{"service_uuid":
    ["bde7610f-2243-4596-aa89-761a8280c950",
     "bde7610f-2243-4596-aa89-761a8280c951"],
    "cost":-1}
@apiUse CODE_DELETE_0
"""
