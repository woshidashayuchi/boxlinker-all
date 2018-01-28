#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/9/2 上午10:43
@用户相关
"""

from flask import Blueprint
from flask_restful import Api, Resource

from authServer.user.signup import signup
from authServer.user.login import Login, CheckToken, FlushToken, LogOut, CheckTokenGet
from authServer.user.user import UserInfo


from authServer.user.UserBaseView import PassWord, PersonalHead

user = Blueprint('user', __name__, url_prefix='/user')

api = Api()

@user.route('/test')
def test():
    print 'http://hostname/user/test is ok'
    return 'http://hostname/user/test is ok'

# 所有接口前添加了  user
# 用户注册  20160816 初步测试通过
api.add_resource(signup, '/signup', '/')

# 用户登录 20160816 初步测试通过
api.add_resource(Login, '/login', '/')

# 验证token
api.add_resource(CheckToken, '/check_token', '/')

# 刷新系统token
api.add_resource(FlushToken, '/flush_token', '/')

# 退出系统
api.add_resource(LogOut, '/log_out', '/')

api.add_resource(UserInfo, '/userinfo', '')

# token 验证
api.add_resource(CheckTokenGet, '/check_token_get', '/')


# 密码相关
api.add_resource(PassWord, '/password', '/')

# 个人头像
api.add_resource(PersonalHead, '/personalhead', '/')

api.init_app(user)
