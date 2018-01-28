#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/10/17 09:59
@func: 组织相关 organization
"""

from flask import Blueprint
from flask_restful import Api



from authServer.v1.usercenter.orgs_base import OrganizationBase, OrganizationBaseMsg
from authServer.v1.usercenter.orgs_user import OrganizationUser, OrganizationUserHandle
from authServer.v1.usercenter.orgs_owner import OrganizationOwner


from authServer.v1.usercenter.users import UserSignup, UserLogin, UserFuzzy, TokenUser

usercenter = Blueprint('usercenter', __name__, url_prefix='/api/v1.0/usercenter')

api = Api()


# /api/v1.0/usercenter/users   注册用户
api.add_resource(UserSignup, '/users')   # 注册用户

# http://auth.boxlinker.com/api/v1.0/usercenter/users/email/<string:opcode>/<string:action> # 邮箱确认
from authServer.v1.usercenter.emailConfirm import EmailConfirm
#
api.add_resource(EmailConfirm, '/users/email/<string:opcode>/<string:action>')




# /api/v1.0/usercenter/users/list/<string:user_fuzzy>   用户列表模糊查询
api.add_resource(UserFuzzy, '/users/list/<string:user_fuzzy>')   # 用户列表模糊查询

# /api/v1.0/usercenter/tokens  # 用户组织列表，用户登录
api.add_resource(UserLogin, '/tokens')

from authServer.v1.usercenter.passwordFind import PasswordFindEmail
# /api/v1.0/usercenter/passwords/email
# http://auth.boxlinker.com/api/v1.0/usercenter/passwords/email/B56BF435DA3EC8753498BDF5BD73874B/FindEmail
api.add_resource(PasswordFindEmail, '/passwords/email', '/passwords/email/<string:opcode>/<string:action>')  # 通过邮箱找回密码

# from authServer.v1.usercenter.passwordFind import EmailActionCode
# api.add_resource(EmailActionCode, '/passwords/email/<string:opcode>/<string:action>')  # 通过邮箱找回密码

# /api/v1.0/usercenter/tokens/user  # 获取用户最基本信息
api.add_resource(TokenUser, '/tokens/user')

# /api/v1.0/usercenter/orgs  新建组织; 用户组织列表
api.add_resource(OrganizationBase, '/orgs')

# /api/v1.0/usercenter/users/orgs/<string:orga_uuid>    获取组织信息; 主动离开组织;  解散组织
api.add_resource(OrganizationBaseMsg, '/orgs/<string:orga_uuid>')



# /api/v1.0/usercenter/orgs/users
api.add_resource(OrganizationUser,'/orgs/<string:orga_uuid>/users')  # 添加组织成员; 组织成员列表

api.add_resource(OrganizationUserHandle, '/orgs/<string:orga_uuid>/users/<string:user_uuid>')

# /api/v1.0/usercenter/orgs/<string:org_id>/owers/<string:user_name>  组织拥有者
api.add_resource(OrganizationOwner, '/orgs/<string:orga_uuid>/owner/<string:user_uuid>')



api.init_app(usercenter)
