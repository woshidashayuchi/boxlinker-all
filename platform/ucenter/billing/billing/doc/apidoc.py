#! /usr/bin python
# -*- coding:utf8 -*-
# Date:2016-10-12
# Author: YanHua


"""
@apiDefine DELETE_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {}
}
"""


"""
@apiDefine POST_RESOURCES_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "resource_uuid": "string",
        "resource_name": "string",
        "resource_type": "string",
        "resource_conf": "string",
        "resource_status": "string",
        "team_uuid": "string",
        "project_uuid": "string",
        "user_uuid": "string"
    }
}
"""


"""
@apiDefine POST_COSTS_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "resource_type": "string",
        "resource_conf": "string",
        "resource_status": "string",
        "hours": int,
        "resource_cost": float
    }
}
"""


"""
@apiDefine POST_LIMITS_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "team_uuid": "string",
        "resource_type": "string",
        "balance_check": 0/1,
        "limit_check": 0/1
    }
}
"""


"""
@apiDefine GET_LIMITS_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "count": int,
        "limits_list": [
            {
                "team_level": int,
                "teams": int,
                "teamusers": int,
                "projects": int,
                "projectusers": int,
                "roles": int,
                "images": int,
                "services": int,
                "volumes": int,
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                "team_level": int,
                "teams": int,
                "teamusers": int,
                "projects": int,
                "projectusers": int,
                "roles": int,
                "images": int,
                "services": int,
                "volumes": int,
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                "team_level": int,
                "teams": int,
                "teamusers": int,
                "projects": int,
                "projectusers": int,
                "roles": int,
                "images": int,
                "services": int,
                "volumes": int,
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            }
        ]
    }
}
"""


"""
@apiDefine PUT_LIMITS_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "team_level": int,
        "resource_type": "string",
        "limit": int
    }
}
"""


"""
@apiDefine PUT_RESOURCES_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "resource_uuid": "string",
        "resource_conf": "string",
        "resource_status": "string",
        "team_uuid": "string",
        "project_uuid": "string",
        "user_uuid": "string"
    }
}
"""


"""
@apiDefine GET_RESOURCES_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "count": int,
        "resources_list": [
            {
                "resource_uuid": "string",
                "resource_name": "string",
                "resource_type": "string",
                "resource_conf": "string",
                "resource_status": "string",
                "team_uuid": "string",
                "project_uuid": "string",
                "user_uuid": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                "resource_uuid": "string",
                "resource_name": "string",
                "resource_type": "string",
                "resource_conf": "string",
                "resource_status": "string",
                "team_uuid": "string",
                "project_uuid": "string",
                "user_uuid": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                "resource_uuid": "string",
                "resource_name": "string",
                "resource_type": "string",
                "resource_conf": "string",
                "resource_status": "string",
                "team_uuid": "string",
                "project_uuid": "string",
                "user_uuid": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            }
        ]
    }
}
"""


"""
@apiDefine POST_VOUCHERS_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "voucher_uuid": "string",
        "denomination": int,
        "invalid_time": "YYYY-MM-DD HH:MM:SS"
    }
}
"""


"""
@apiDefine PUT_VOUCHERS_STATUS_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "voucher_uuid": "string"
    }
}
"""


"""
@apiDefine PUT_VOUCHERS_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "vouchers_uuid": "string",
        "team_uuid": "string",
        "project_uuid": "string",
        "user_uuid": "string"
    }
}
"""


"""
@apiDefine GET_VOUCHERS_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "count": int,
        "vouchers_list": [
            {
                "vouchers_uuid": "string",
                "denomination": int,
                "balance": float,
                "status": "string",
                "accepter": "string",
                "activator": "string",
                "active_time": "YYYY-MM-DD HH:MM:SS",
                "invalid_time": "YYYY-MM-DD HH:MM:SS",
            },
            {
                "vouchers_uuid": "string",
                "denomination": int,
                "balance": float,
                "status": "string",
                "accepter": "string",
                "activator": "string",
                "active_time": "YYYY-MM-DD HH:MM:SS",
                "invalid_time": "YYYY-MM-DD HH:MM:SS",
            },
            {
                "vouchers_uuid": "string",
                "denomination": int,
                "balance": float,
                "status": "string",
                "accepter": "string",
                "activator": "string",
                "active_time": "YYYY-MM-DD HH:MM:SS",
                "invalid_time": "YYYY-MM-DD HH:MM:SS",
            }
        ]
    }
}
"""


"""
@apiDefine GET_ACCPET_VOUCHERS_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "count": int,
        "vouchers_list": [
            {
                "vouchers_uuid": "string",
                "denomination": int,
                "status": "string",
                "invalid_time": "YYYY-MM-DD HH:MM:SS",
            },
            {
                "vouchers_uuid": "string",
                "denomination": int,
                "status": "string",
                "invalid_time": "YYYY-MM-DD HH:MM:SS",
            },
            {
                "vouchers_uuid": "string",
                "denomination": int,
                "status": "string",
                "invalid_time": "YYYY-MM-DD HH:MM:SS",
            }
        ]
    }
}
"""


"""
@apiDefine GET_BILLS_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "count": int,
        "bills_total": {
                           "resource_cost": float,
                           "voucher_cost": float
                       },
        "bills_list": [
            {
                "start_time": "YY-MM-DD",
                "end_time": "YY-MM-DD",
                "team_uuid": "string",
                "project_uuid": "string",
                "user_uuid": "string",
                "resource_uuid": "string",
                "resource_name": "string",
                "resource_type": "string",
                "resource_conf": "string",
                "resource_status": "string",
                "resource_cost": float,
                "voucher_cost": float
            },
            {
                "start_time": "YY-MM-DD",
                "end_time": "YY-MM-DD",
                "team_uuid": "string",
                "project_uuid": "string",
                "user_uuid": "string",
                "resource_uuid": "string",
                "resource_name": "string",
                "resource_type": "string",
                "resource_conf": "string",
                "resource_status": "string",
                "resource_cost": float,
                "voucher_cost": float
            },
            {
                "start_time": "YY-MM-DD",
                "end_time": "YY-MM-DD",
                "team_uuid": "string",
                "project_uuid": "string",
                "user_uuid": "string",
                "resource_uuid": "string",
                "resource_name": "string",
                "resource_type": "string",
                "resource_conf": "string",
                "resource_status": "string",
                "resource_cost": float,
                "voucher_cost": float
            }
        ]
    }
}
"""


"""
@apiDefine GET_LEVELS_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "team_uuid": "string",
        "level": int,
        "experience": int,
        "up_required": int,
        "create_time": "YYYY-MM-DD HH:MM:SS",
        "update_time": "YYYY-MM-DD HH:MM:SS"
    }
}
"""


"""
@apiDefine GET_BALANCES_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "team_uuid": "string",
        "balance": float,
        "update_time": "YYYY-MM-DD HH:MM:SS"
    }
}
"""


"""
@apiDefine BALANCES_CHECK_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "teams_list": [
            {
                "team_uuid": "string",
                "balance": float
            },
            {
                "team_uuid": "string",
                "balance": float
            },
            {
                "team_uuid": "string",
                "balance": float
            }
        ]
    }
}
"""


"""
@apiDefine POST_RECHARGES_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "recharge_uuid": int,
        "recharge_type": "string",
        "recharge_amount": int,
        "user_name": "string",
        "qr_code": "url"
    }
}
"""


"""
@apiDefine GET_RECHARGES_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "recharge_uuid": int,
        "recharge_amount": int,
        "recharge_type": "string",
        "team_uuid": "string",
        "user_name": "string",
        "create_time": "YYYY-MM-DD HH:MM:SS"
    }
}
"""


"""
@apiDefine LIST_RECHARGES_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "count": int,
        "recharge_list": [
            {
                "team_uuid": "string",
                "recharge_uuid": "string",
                "recharge_amount": int,
                "recharge_type": "string",
                "user_name": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                "team_uuid": "string",
                "recharge_uuid": "string",
                "recharge_amount": int,
                "recharge_type": "string",
                "user_name": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                "team_uuid": "string",
                "recharge_uuid": "string",
                "recharge_amount": int,
                "recharge_type": "string",
                "user_name": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS"
            }
        ]
    }
}
"""


"""
@apiDefine POST_ORDERS_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "order_uuid": "string",
        "resource_uuid": "string",
        "cost": float,
        "status": "string",
        "team_uuid": "string",
        "project_uuid": "string",
        "user_uuid": "string"
    }
}
"""


"""
@apiDefine PUT_ORDERS_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "order_uuid": "string",
        "cost": float,
        "status": "string"
    }
}
"""


"""
@apiDefine GET_ORDERS_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "count": int,
        "orders_list": [
            {
                "order_uuid": "string",
                "resource_uuid": "string",
                "cost": float,
                "status": "string",
                "team_uuid": "string",
                "project_uuid": "string",
                "user_uuid": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            },
                "order_uuid": "string",
                "resource_uuid": "string",
                "cost": float,
                "status": "string",
                "team_uuid": "string",
                "project_uuid": "string",
                "user_uuid": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            {
            },
            {
                "order_uuid": "string",
                "resource_uuid": "string",
                "cost": float,
                "status": "string",
                "team_uuid": "string",
                "project_uuid": "string",
                "user_uuid": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            }
        ]
    }
}
"""


###################################################################
#                       计费服务接口定义                          #
###################################################################


"""
@api {post} /api/v1.0/billing/resources 1.1 资源创建
@apiName create resources record
@apiGroup 1 resources
@apiVersion 1.0.0
@apiDescription 创建需要计费的资源信息
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "resource_uuid": "string",
    "resource_name": "string",
    "resource_type": "string",
    "resource_conf": "string",
    "resource_status": "string"
}
@apiUse POST_RESOURCES_0
"""


"""
@api {get} /api/v1.0/billing/resources?page_size=<int>&page_num=<int> 1.2 资源列表
@apiName get resources record
@apiGroup 1 resources
@apiVersion 1.0.0
@apiDescription 获取需要计费的资源列表
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse GET_RESOURCES_0
"""


"""
@api {put} /api/v1.0/billing/resources/<resource_uuid> 1.3 资源更新
@apiName update resources record
@apiGroup 1 resources
@apiVersion 1.0.0
@apiDescription 更新需要计费的资源信息
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "resource_conf": "string",
    "resource_status": "string",
    "team_uuid": "string",
    "project_uuid": "string",
    "user_uuid": "string"
}
@apiUse PUT_RESOURCES_0
"""


"""
@api {delete} /api/v1.0/billing/resources/<resource_uuid> 1.4 资源删除
@apiName delete resources record
@apiGroup 1 resources
@apiVersion 1.0.0
@apiDescription 删除需要计费的资源信息
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse DELETE_0
"""


"""
@api {put} /api/v1.0/billing/resources 1.5 资源核对
@apiName check resources record
@apiGroup 1 resources
@apiVersion 1.0.0
@apiDescription 核对需要计费的资源信息与资源提供端信息是否匹配
@apiPermission organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    add_list: [
        {
            "resource_uuid": "string",
            "resource_name": "string",
            "resource_type": "string",
            "resource_conf": "string",
            "resource_status": "string",
            "team_uuid": "string",
            "project_uuid": "string",
            "user_uuid": "string"
        }
    ],
    delete_list: [
        {
            "resource_uuid": "string"
        }
    ],
    update_list: [
        {
            "resource_uuid": "string",
            "resource_name": "string",
            "resource_type": "string",
            "resource_conf": "string",
            "resource_status": "string",
            "team_uuid": "string",
            "project_uuid": "string",
            "user_uuid": "string"
        }
    ]
}
@apiUse DELETE_0
"""


"""
@api {post} /api/v1.0/billing/vouchers 2.1 礼券生成
@apiName create vouchers
@apiGroup 2 vouchers
@apiVersion 1.0.0
@apiDescription 系统管理员生成礼券
@apiPermission admin
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "denomination": int,
    "invalid_time": "epoch_seconds"
}
@apiUse POST_VOUCHERS_0
"""


"""
@api {put} /api/v1.0/billing/vouchers/<voucher_uuid> 2.2 礼券分发
@apiName distribute vouchers
@apiGroup 2 vouchers
@apiVersion 1.0.0
@apiDescription 系统管理员分发礼券给用户
@apiPermission admin
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "accepter": "string"
}
@apiUse PUT_VOUCHERS_STATUS_0
"""


"""
@api {get} /api/v1.0/billing/vouchers?voucher_accept=<true>&page_size=<int>&page_num=<int> 2.3 礼券查询
@apiName get accept vouchers
@apiGroup 2 vouchers
@apiVersion 1.0.0
@apiDescription 用户查询收到的礼券列表
@apiPermission admin
@apiParam {json} header {"token": "string"}
@apiUse GET_ACCPET_VOUCHERS_0
"""


"""
@api {post} /api/v1.0/billing/vouchers/<voucher_uuid> 2.4 礼券激活
@apiName active vouchers
@apiGroup 2 vouchers
@apiVersion 1.0.0
@apiDescription 用户激活领用到的礼券
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse PUT_VOUCHERS_0
"""


"""
@api {get} /api/v1.0/billing/vouchers?start_time=<epoch_seconds>&end_time=<epoch_seconds>&page_size=<int>&page_num=<int> 2.5 礼券列表
@apiName get vouchers
@apiGroup 2 vouchers
@apiVersion 1.0.0
@apiDescription 查询用户已激活的礼劵列表
@apiPermission user and organization and admin
@apiParam {json} header {"token": "string"}
@apiUse GET_VOUCHERS_0
"""


"""
@api {post} /api/v1.0/billing/orders 3.1 订单创建
@apiName create orders
@apiGroup 3 orders
@apiVersion 1.0.0
@apiDescription 创建订单信息
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "resource_uuid": "string",
    "cost": float,
    "status": "string"
}
@apiUse POST_ORDERS_0
"""


"""
@api {put} /api/v1.0/billing/orders/<order_uuid> 3.2 订单更新
@apiName update orders
@apiGroup 3 orders
@apiVersion 1.0.0
@apiDescription 更新订单信息
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "cost": float,
    "status": "string"
}
@apiUse PUT_ORDERS_0
"""


"""
@api {get} /api/v1.0/billing/orders?start_time=<epoch_seconds>&end_time=<epoch_seconds>&page_size=<int>&page_num=<int> 3.3 订单列表
@apiName get orders
@apiGroup 3 orders
@apiVersion 1.0.0
@apiDescription 查询订单信息
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse GET_ORDERS_0
"""


"""
@api {post} /api/v1.0/billing/limits 4.1 限额检查
@apiName limits check
@apiGroup 4 limits
@apiVersion 1.0.0
@apiDescription 检查限额值
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "resource_type": "string",
    "cost": float
}
@apiUse POST_LIMITS_0
"""


"""
@api {get} /api/v1.0/billing/limits?page_size=<int>&page_num=<int> 4.2 限额列表
@apiName limits list
@apiGroup 4 limits
@apiVersion 1.0.0
@apiDescription 系统管理员查询限额列表
@apiPermission system admin
@apiParam {json} header {"token": "string"}
@apiUse GET_LIMITS_0
"""


"""
@api {put} /api/v1.0/billing/limits 4.3 限额更新
@apiName limits update
@apiGroup 4 limits
@apiVersion 1.0.0
@apiDescription 系统管理员更新限额信息
@apiPermission system admin
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "team_level": "string",
    "resource_type": "string",
    "limit": int
}
@apiUse PUT_LIMITS_0
"""


"""
@api {get} /api/v1.0/billing/levels 5.1 等级信息
@apiName get levels
@apiGroup 5 levels
@apiVersion 1.0.0
@apiDescription 查询等级信息
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse GET_LEVELS_0
"""


"""
@api {get} /api/v1.0/billing/balances 6.1 余额信息
@apiName get balances
@apiGroup 6 balances
@apiVersion 1.0.0
@apiDescription 查询余额信息
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse GET_BALANCES_0
"""


"""
@api {get} /api/v1.0/billing/balances?balance_check=<true> 6.2 余额检查
@apiName check balances
@apiGroup 6 balances
@apiVersion 1.0.0
@apiDescription 查询余额小于零的组织并进行资源回收
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse BALANCES_CHECK_0
"""


"""
@api {post} /api/v1.0/billing/costs 7.1 费用信息
@apiName get resource cost
@apiGroup 7 costs
@apiVersion 1.0.0
@apiDescription 计算资源费用
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "resource_type": "string",
    "resource_conf": "string",
    "resource_status": "string",
    "hours": int
}
@apiUse POST_COSTS_0
"""


"""
@api {post} /api/v1.0/billing/recharges 8.1 用户充值
@apiName create recharge records
@apiGroup 8 recharges
@apiVersion 1.0.0
@apiDescription 用户执行充值
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "recharge_type": "zhifubao/weixin",
    "recharge_amount": int
}
@apiUse POST_RECHARGES_0
"""


"""
@api {get} /api/v1.0/billing/recharges/<recharge_uuid> 8.2 充值查询
@apiName get recharge info record
@apiGroup 8 recharges
@apiVersion 1.0.0
@apiDescription 查询充值结果
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse GET_RECHARGES_0
"""


"""
@api {get} /api/v1.0/billing/recharges?start_time=<epoch_seconds>&end_time=<epoch_seconds>&page_size=<int>&page_num=<int> 8.3 充值记录
@apiName get recharge_records
@apiGroup 8 recharges
@apiVersion 1.0.0
@apiDescription 查询充值记录
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse LIST_RECHARGES_0
"""


"""
@api {get} /api/v1.0/billing/recharges?recharge_type=<all/zhifubao/weixin>&start_time=<epoch_seconds>&end_time=<epoch_seconds>&page_size=<int>&page_num=<int> 8.4 充值核对
@apiName check recharge_records
@apiGroup 8 recharges
@apiVersion 1.0.0
@apiDescription 管理员查询核对充值记录
@apiPermission admin
@apiParam {json} header {"token": "string"}
@apiUse LIST_RECHARGES_0
"""


"""
@api {get} /api/v1.0/billing/bills?start_time=<epoch_seconds>&end_time=<epoch_seconds>&page_size=<int>&page_num=<int> 9.1 账单查询
@apiName get bills
@apiGroup 9 bills
@apiVersion 1.0.0
@apiDescription 查询账单信息
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse GET_BILLS_0
"""
