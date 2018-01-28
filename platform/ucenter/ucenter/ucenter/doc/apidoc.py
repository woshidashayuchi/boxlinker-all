#! /usr/bin python
# -*- coding:utf8 -*-
# Date:2016-08-31
# Author: YanHua


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
@apiDefine CODE_USER_REGISTER_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "user_name": "string",
        "email": "string",
        "mobile": "string"
    }
}
"""


"""
@apiDefine CODE_USER_ACTIVATE_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "user_uuid": "string",
        "user_name": "string",
        "team_uuid": "string",
        "project_uuid": "string"
    }
}
"""


"""
@apiDefine CODE_USER_INFO_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "user_uuid": "string",
        "user_name": "string",
        "real_name": "string",
        "email": "string",
        "mobile": "string",
        "sex": "string",
        "status": "string",
        "birth_date": "YYYY-MM-DD HH:MM:SS",
        "create_time": "YYYY-MM-DD HH:MM:SS",
        "update_time": "YYYY-MM-DD HH:MM:SS"
    }
}
"""


"""
@apiDefine CODE_USER_CHECK_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": 0/1
}
"""


"""
@apiDefine CODE_USER_LIST_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "user_list": [
            {
                "user_uuid": "string",
                "user_name": "string"
            },
            {
                "user_uuid": "string",
                "user_name": "string"
            },
            {
                "user_uuid": "string",
                "user_name": "string"
            }
        ]
    }
}
"""


"""
@apiDefine CODE_USER_UPDATE_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "user_uuid": "string",
        "real_name": "string",
        "mobile": "string",
        "sex": "man/woman",
        "birth_date": "YYYY-MM-DD HH:MM:SS"
    }
}
"""


"""
@apiDefine CODE_USER_STATUS_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "user_uuid": "string",
        "user_status": "enable/disable"
    }
}
"""


"""
@apiDefine CODE_ROLE_CREATE_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "role_uuid": "string",
        "role_name": "string",
        "role_priv": "string",
        "role_owner": "string",
        "role_team": "string"
    }
}
"""


"""
@apiDefine CODE_ROLE_LIST_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "role_list": [
            {
                "role_uuid": "string",
                "role_name": "string",
                "role_priv": "string",
                "role_type": "string",
                "status": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                "role_uuid": "string",
                "role_name": "string",
                "role_priv": "string",
                "role_type": "string",
                "status": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                "role_uuid": "string",
                "role_name": "string",
                "role_priv": "string",
                "role_type": "string",
                "status": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            }
        ]
    }
}
"""


"""
@apiDefine CODE_ROLE_INFO_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "role_uuid": "string",
        "role_name": "string",
        "role_priv": "string",
        "role_type": "string",
        "status": "string",
        "create_time": "YYYY-MM-DD HH:MM:SS",
        "update_time": "YYYY-MM-DD HH:MM:SS"
    }
}
"""


"""
@apiDefine CODE_ROLE_UPDATE_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "role_uuid": "string",
        "role_priv": "string"
    }
}
"""


"""
@apiDefine CODE_PASSWORD_CHANGE_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "user_name": "string"
    }
}
"""


"""
@apiDefine CODE_USER_LOGIN_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "user_token": "string"
    }
}
"""


"""
@apiDefine CODE_TOKEN_AUTH_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "user_uuid": "string",
        "user_name": "string",
        "team_uuid": "string",
        "team_priv": "string",
        "project_uuid": "string",
        "project_priv": "string"
    }
}
"""


"""
@apiDefine CODE_TOKEN_SWITCH_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "orga_token": "string"
    }
}
"""


"""
@apiDefine CODE_TEAM_CREATE_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "team_uuid": "string",
        "team_name": "string",
        "team_owner": "string",
        "team_desc": "string",
        "project_uuid": "string"
    }
}
"""


"""
@apiDefine CODE_TEAM_LIST_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "team_list": [
            {
                "team_uuid": "string",
                "team_name": "string",
                "team_owner": "string",
                "team_type": "string",
                "team_desc": "string",
                "status": "string",
                "role_name": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                "team_uuid": "string",
                "team_name": "string",
                "team_owner": "string",
                "team_type": "string",
                "team_desc": "string",
                "status": "string",
                "role_name": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                "team_uuid": "string",
                "team_name": "string",
                "team_owner": "string",
                "team_type": "string",
                "team_desc": "string",
                "status": "string",
                "role_name": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            }
        ]
    }
}
"""


"""
@apiDefine CODE_TEAM_UUID_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "team_uuid": "string",
        "team_name": "string",
        "team_owner": "string"
    }
}
"""


"""
@apiDefine CODE_TEAM_INFO_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "team_uuid": "string",
        "team_name": "string",
        "team_owner": "string",
        "team_type": "string",
        "team_desc": "string",
        "status": "string",
        "create_time": "YYYY-MM-DD HH:MM:SS",
        "update_time": "YYYY-MM-DD HH:MM:SS"
    }
}
"""


"""
@apiDefine CODE_TEAM_UPDATE_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "team_uuid": "string",
        "team_owner": "string",
        "team_type": "string",
        "team_desc": "string"
    }
}
"""


"""
@apiDefine CODE_PROJECTS_CREATE_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "project_uuid": "string",
        "project_name": "string",
        "project_owner": "string",
        "project_team": "string",
        "project_desc": "string"
    }
}
"""


"""
@apiDefine CODE_PROJECTS_LIST_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "project_list": [
            {
                "project_uuid": "string",
                "project_name": "string",
                "project_owner": "string",
                "project_team": "string",
                "project_type": "string",
                "project_desc": "string",
                "status": "string",
                "role_name": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                "project_uuid": "string",
                "project_name": "string",
                "project_owner": "string",
                "project_team": "string",
                "project_type": "string",
                "project_desc": "string",
                "status": "string",
                "role_name": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                "project_uuid": "string",
                "project_name": "string",
                "project_owner": "string",
                "project_team": "string",
                "project_type": "string",
                "project_desc": "string",
                "status": "string",
                "role_name": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            }
        ]
    }
}
"""


"""
@apiDefine CODE_PROJECTS_INFO_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "project_uuid": "string",
        "project_name": "string",
        "project_owner": "string",
        "project_team": "string",
        "project_type": "string",
        "project_desc": "string",
        "status": "string",
        "create_time": "YYYY-MM-DD HH:MM:SS",
        "update_time": "YYYY-MM-DD HH:MM:SS"
    }
}
"""


"""
@apiDefine CODE_PROJECTS_UPDATE_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "project_uuid": "string",
        "project_owner": "string",
        "project_desc": "string"
    }
}
"""


"""
@apiDefine CODE_USERSTEAMS_ADD_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "user_uuid": "string",
        "team_uuid": "string",
        "team_role": "string"
    }
}
"""


"""
@apiDefine CODE_USERSTEAMS_ACTIVATE_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "user_uuid": "string",
        "team_uuid": "string"
    }
}
"""


"""
@apiDefine CODE_USERSTEAMS_LIST_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "count": int,
        "user_list": [
            {
                "user_uuid": "string",
                "user_name": "string",
                "team_role": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                "user_uuid": "string",
                "user_name": "string",
                "team_role": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                "user_uuid": "string",
                "user_name": "string",
                "team_role": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            }
        ]
    }
}
"""


"""
@apiDefine CODE_USERSPROJECTS_ADD_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "user_uuid": "string",
        "project_uuid": "string",
        "project_role": "string"
    }
}
"""


"""
@apiDefine CODE_USERSPROJECTS_LIST_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "count": int,
        "user_list": [
            {
                "user_uuid": "string",
                "user_name": "string",
                "project_role": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                "user_uuid": "string",
                "user_name": "string",
                "project_role": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                "user_uuid": "string",
                "user_name": "string",
                "project_role": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            }
        ]
    }
}
"""


###################################################################
#                        用户服务接口定义                         #
###################################################################



"""
@api {post} /api/v1.0/ucenter/users 1.1 用户注册
@apiName user register
@apiGroup 1 users
@apiVersion 1.0.0
@apiDescription 用户注册
@apiPermission user
@apiParam {json} body
@apiParamExample body
{
    "user_name": "string",
    "password": "string",
    "email": "string",
    "mobile": "string",
    "code_id": "string",
    "code_str": "string"
}
@apiUse CODE_USER_REGISTER_0
"""


"""
@api {get} /api/v1.0/ucenter/users/status/<user_uuid> 1.2 用户激活
@apiName user activate
@apiGroup 1 users
@apiVersion 1.0.0
@apiDescription 用户激活
@apiPermission user
@apiUse CODE_USER_ACTIVATE_0
"""


"""
@api {get} /api/v1.0/ucenter/users?user_name=<string> 1.3 用户列表
@apiName user list
@apiGroup 1 users
@apiVersion 1.0.0
@apiDescription 根据用户输入模糊查询用户列表
@apiPermission organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_USER_LIST_0
"""


"""
@api {get} /api/v1.0/ucenter/users?user_name=<string>&name_check=<true> 1.4 用户检测
@apiName user exist check
@apiGroup 1 users
@apiVersion 1.0.0
@apiDescription 用户注册时检测用户名是否存在
@apiPermission organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_USER_CHECK_0
"""


"""
@api {get} /api/v1.0/ucenter/users/<user_uuid> 1.5 用户信息
@apiName user info
@apiGroup 1 users
@apiVersion 1.0.0
@apiDescription 用户详细信息查询
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_USER_INFO_0
"""


"""
@api {put} /api/v1.0/ucenter/users/<user_uuid> 1.6 用户更新
@apiName user update
@apiGroup 1 users
@apiVersion 1.0.0
@apiDescription 用户信息更新
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "real_name": "string",
    "mobile": "string",
    "sex": "man/woman",
    "birth_date": epoch_milliseconds
}
@apiUse CODE_USER_UPDATE_0
"""


"""
@api {put} /api/v1.0/ucenter/users/status/<user_uuid> 1.7 用户状态
@apiName user status update
@apiGroup 1 users
@apiVersion 1.0.0
@apiDescription 用户状态更新（启用/禁用）
@apiPermission system admin
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "user_status": "enable/disable"
}
@apiUse CODE_USER_STATUS_0
"""


"""
@api {post} /api/v1.0/ucenter/roles 2.1 角色创建
@apiName role create
@apiGroup 2 roles
@apiVersion 1.0.0
@apiDescription 角色创建
@apiPermission organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "role_name": "string",
    "role_priv": "CRUD"
}
@apiUse CODE_ROLE_CREATE_0
"""


"""
@api {get} /api/v1.0/ucenter/roles 2.2 角色列表
@apiName role list
@apiGroup 2 roles
@apiVersion 1.0.0
@apiDescription 角色列表查询
@apiPermission organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_ROLE_LIST_0
"""


"""
@api {get} /api/v1.0/ucenter/roles/<role_uuid> 2.3 角色信息
@apiName role info
@apiGroup 2 roles
@apiVersion 1.0.0
@apiDescription 角色详细信息查询
@apiPermission organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_ROLE_INFO_0
"""


"""
@api {put} /api/v1.0/ucenter/roles/<role_uuid> 2.4 角色更新
@apiName role update
@apiGroup 2 roles
@apiVersion 1.0.0
@apiDescription 角色权限更新
@apiPermission organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "role_priv": "CRUD"
}
@apiUse CODE_ROLE_UPDATE_0
"""


"""
@api {delete} /api/v1.0/ucenter/roles/<role_uuid> 2.5 角色删除
@apiName role delete
@apiGroup 2 roles
@apiVersion 1.0.0
@apiDescription 角色删除
@apiPermission organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_DELETE_0
"""


"""
@api {post} /api/v1.0/ucenter/passwords/<user_uuid> 3.1 密码修改
@apiName password change
@apiGroup 3 passwords
@apiVersion 1.0.0
@apiDescription 用户主动修改密码
@apiPermission user
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "old_password": "string",
    "new_password": "string"
}
@apiUse CODE_PASSWORD_CHANGE_0
"""


"""
@api {get} /api/v1.0/ucenter/passwords/<user_name> 3.2 密码找回
@apiName password find
@apiGroup 3 passwords
@apiVersion 1.0.0
@apiDescription 密码找回邮件发送
@apiPermission user
@apiUse CODE_PASSWORD_CHANGE_0
"""


"""
@api {put} /api/v1.0/ucenter/passwords/<user_uuid> 3.3 密码重置
@apiName password reset
@apiGroup 3 passwords
@apiVersion 1.0.0
@apiDescription 密码找回时用新密码重置
@apiPermission user
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "password": "string"
}
@apiUse CODE_PASSWORD_CHANGE_0
"""


"""
@api {post} /api/v1.0/ucenter/tokens 4.1 Token创建（登录）
@apiName user login
@apiGroup 4 tokens
@apiVersion 1.0.0
@apiDescription 用户登录时创建Token
@apiPermission user
@apiParam {json} body
@apiParamExample body
{
    "user_name": "string",
    "password": "string"
}
@apiUse CODE_USER_LOGIN_0
"""


"""
@api {get} /api/v1.0/ucenter/tokens 4.2 Token验证
@apiName token auth
@apiGroup 4 tokens
@apiVersion 1.0.0
@apiDescription 验证Token正确性
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_TOKEN_AUTH_0
"""


"""
@api {put} /api/v1.0/ucenter/tokens 4.3 Token切换
@apiName token switch
@apiGroup 4 tokens
@apiVersion 1.0.0
@apiDescription 用户切换组织或项目时更新Token
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "team_uuid": "string",
    "project_uuid": "string"
}
@apiUse CODE_TOKEN_SWITCH_0
"""


"""
@api {delete} /api/v1.0/ucenter/tokens 4.4 Token注销
@apiName token delete
@apiGroup 4 tokens
@apiVersion 1.0.0
@apiDescription 用户注销时删除Token
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_DELETE_0
"""


"""
@api {post} /api/v1.0/ucenter/teams 5.1.1 组织创建
@apiName team create
@apiGroup 5 teams
@apiVersion 1.0.0
@apiDescription 组织创建
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "team_name": "string",
    "team_desc": "string"
}
@apiUse CODE_TEAM_CREATE_0
"""


"""
@api {get} /api/v1.0/ucenter/teams 5.1.2 组织列表
@apiName team list
@apiGroup 5 teams
@apiVersion 1.0.0
@apiDescription 查询用户所属的组织列表
@apiPermission organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_TEAM_LIST_0
"""


"""
@api {get} /api/v1.0/ucenter/teams?team_name=<team_name>&name_check=<true> 5.1.3 组织检测
@apiName team exist check
@apiGroup 5 teams
@apiVersion 1.0.0
@apiDescription 创建组织时检测组织名是否存在
@apiPermission organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_USER_CHECK_0
"""


"""
@api {get} /api/v1.0/ucenter/teams?team_name=<team_name>&uuid_info=<true> 5.1.4 组织UUID
@apiName team uuid get
@apiGroup 5 teams
@apiVersion 1.0.0
@apiDescription 根据组织名查询组织UUID
@apiPermission organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_TEAM_UUID_0
"""


"""
@api {get} /api/v1.0/ucenter/teams?team_name=<team_name>&public_info=<true> 5.1.5 组织列表(公开团队)
@apiName public team uuid get
@apiGroup 5 teams
@apiVersion 1.0.0
@apiDescription 根据组织名查询平台公开的组织信息
@apiPermission organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_TEAM_INFO_0
"""


"""
@api {get} /api/v1.0/ucenter/teams/<team_uuid> 5.1.6 组织信息
@apiName team info
@apiGroup 5 teams
@apiVersion 1.0.0
@apiDescription 组织详细信息查询
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_TEAM_INFO_0
"""


"""
@api {put} /api/v1.0/ucenter/teams/<team_uuid> 5.1.7 组织更新
@apiName team update
@apiGroup 5 teams
@apiVersion 1.0.0
@apiDescription 更新组织拥有者或描述信息
@apiPermission organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "team_owner": "string",
    "team_type": "private/public"
    "team_desc": "string"
}
@apiUse CODE_TEAM_UPDATE_0
"""


"""
@api {delete} /api/v1.0/ucenter/teams/<team_uuid> 5.1.8 组织删除
@apiName team delete
@apiGroup 5 teams
@apiVersion 1.0.0
@apiDescription 组织删除
@apiPermission organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_DELETE_0
"""


"""
@api {post} /api/v1.0/ucenter/projects 6.1.1 项目创建
@apiName projects create
@apiGroup 6 projects
@apiVersion 1.0.0
@apiDescription 项目创建
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "project_name": "string",
    "project_desc": "string"
}
@apiUse CODE_PROJECTS_CREATE_0
"""


"""
@api {get} /api/v1.0/ucenter/projects 6.1.2 项目列表
@apiName project list
@apiGroup 6 projects
@apiVersion 1.0.0
@apiDescription 查询用户在某一特定组织下所属的项目列表
@apiPermission organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_PROJECTS_LIST_0
"""


"""
@api {get} /api/v1.0/ucenter/projects/<project_uuid> 6.1.3 项目信息
@apiName project info
@apiGroup 6 projects
@apiVersion 1.0.0
@apiDescription 项目详细信息查询
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_PROJECTS_INFO_0
"""


"""
@api {put} /api/v1.0/ucenter/projects/<project_uuid> 6.1.4 项目更新
@apiName project update
@apiGroup 6 projects
@apiVersion 1.0.0
@apiDescription 项目更新
@apiPermission organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "project_owner": "string",
    "project_desc": "string"
}
@apiUse CODE_PROJECTS_UPDATE_0
"""


"""
@api {delete} /api/v1.0/ucenter/projects/<project_uuid> 6.1.5 项目删除
@apiName project delete
@apiGroup 6 projects
@apiVersion 1.0.0
@apiDescription 项目删除
@apiPermission organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_DELETE_0
"""


"""
@api {post} /api/v1.0/ucenter/usersteams 5.2.1 组织用户添加
@apiName team user add
@apiGroup 5 teams
@apiVersion 1.0.0
@apiDescription 添加用户到组织
@apiPermission organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "user_uuid": "string",
    "role_uuid": "string"
}
@apiUse CODE_USERSTEAMS_ADD_0
"""


"""
@api {get} /api/v1.0/ucenter/usersteams?page_size=<int>&page_num=<int> 5.2.2 组织用户列表
@apiName team user list
@apiGroup 5 teams
@apiVersion 1.0.0
@apiDescription 查询一个组织下的用户列表
@apiPermission organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_USERSTEAMS_LIST_0
"""


"""
@api {post} /api/v1.0/ucenter/usersteams/<user_uuid> 5.2.3 组织用户激活
@apiName team user activate
@apiGroup 5 teams
@apiVersion 1.0.0
@apiDescription 用户确认是否加入特定组织
@apiPermission user
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "team_uuid": "string"
}
@apiUse CODE_USERSTEAMS_ACTIVATE_0
"""


"""
@api {put} /api/v1.0/ucenter/usersteams/<user_uuid> 5.2.4 组织用户权限
@apiName team user update
@apiGroup 5 teams
@apiVersion 1.0.0
@apiDescription 修改用户在特定组织中的角色
@apiPermission organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "role_uuid": "string"
}
@apiUse CODE_USERSTEAMS_ADD_0
"""


"""
@api {delete} /api/v1.0/ucenter/usersteams?user_uuid=<string>&team_uuid=<string> 5.2.5 组织用户删除
@apiName team user delete
@apiGroup 5 teams
@apiVersion 1.0.0
@apiDescription 将用户移出特定组织
@apiPermission organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_DELETE_0
"""


"""
@api {post} /api/v1.0/ucenter/usersprojects 6.2.1 项目用户添加
@apiName project user add
@apiGroup 6 projects
@apiVersion 1.0.0
@apiDescription 添加用户到项目
@apiPermission organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "user_uuid": "string",
    "role_uuid": "string"
}
@apiUse CODE_USERSPROJECTS_ADD_0
"""


"""
@api {get} /api/v1.0/ucenter/usersprojects?page_size=<int>&page_num=<int> 6.2.2 项目用户列表
@apiName project user list
@apiGroup 6 projects
@apiVersion 1.0.0
@apiDescription 查询一个项目下的用户列表
@apiPermission organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_USERSPROJECTS_LIST_0
"""


"""
@api {put} /api/v1.0/ucenter/usersprojects/<user_uuid> 6.2.3 项目用户权限
@apiName project user update
@apiGroup 6 projects
@apiVersion 1.0.0
@apiDescription 修改用户在特定组织中的角色
@apiPermission organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "role_uuid": "string"
}
@apiUse CODE_USERSPROJECTS_ADD_0
"""


"""
@api {delete} /api/v1.0/ucenter/usersprojects/<user_uuid> 6.2.4 项目用户删除
@apiName project user delete
@apiGroup 6 projects
@apiVersion 1.0.0
@apiDescription 将用户移出特定项目
@apiPermission organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_DELETE_0
"""
