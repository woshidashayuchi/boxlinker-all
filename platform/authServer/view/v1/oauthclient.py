#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/10/26 16:58
@func: 第三方授权认证,客户服务
"""


from flask import Blueprint
from flask_restful import Api


from authServer.v1.oauthclient.github.github import GitOauthUrl


oauthclient = Blueprint('oauthclient', __name__, url_prefix='/api/v1.0/oauthclient')

api = Api()


# /api/v1.0/oauthclient/githuboauthurl
api.add_resource(GitOauthUrl, '/githuboauthurl')   # 获取用户授权地址



api.init_app(oauthclient)
