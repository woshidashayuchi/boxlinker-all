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


from authServer.v2.oauthclient.oauthurl import OauthUrl


oauthv2 = Blueprint('oauths', __name__, url_prefix='/api/v2.0/oauths')

api = Api()


test_token = """eyJ1aWQiOiAiYzFhZjllNjYtZTg0Ny0zYmZkLWI4ZmQtNjdkNTQ0N2M4MzJhIiwgInVzZXJfb3JhZyI6ICJib3hsaW5rZXIiLCAidG9rZW5pZCI6ICI2Njg5ZjRkNGJjMjU0ZGExYmI0YjcyMGYiLCAidXNlcl91dWlkIjogImMxYWY5ZTY2LWU4NDctM2JmZC1iOGZkLTY3ZDU0NDdjODMyYSIsICJleHBpcmVzIjogMTQ3OTg1MTc1OC4zODAxMjIsICJ1c2VyX3JvbGUiOiAiMSIsICJ1c2VyX2lwIjogIjEyNy4wLjAuMSIsICJ1c2VyX29yZ2EiOiAiYm94bGlua2VyIiwgInJvbGVfdXVpZCI6IDIwMCwgIm9yZ2FfdXVpZCI6ICJjMWFmOWU2Ni1lODQ3LTNiZmQtYjhmZC02N2Q1NDQ3YzgzMmEiLCAic2FsdCI6ICI3NjkwNTgwMTdjZGQ2OTU4MDgzMGZhMTEiLCAiZW1haWwiOiAiYm94bGlua2VyQGJveGxpbmtlci5jb20iLCAidXNlcl9uYW1lIjogImJveGxpbmtlciJ9CngMm8P04Y17CRtf5WgoQw=="""

from authServer.common.oauthclient.oauthCallback import CallBack
# /api/v2.0/oauths/callback
api.add_resource(CallBack, '/callback')

# https://open.coding.net/
# /api/v2.0/oauths/oauthurl
api.add_resource(OauthUrl, '/oauthurl')   # 获取用户授权地址

# /api/v2.0/oauths/repos/<string:src_type>/<string:user_uuid>  get 获取代码项目列表;   put 刷新代码列表,返回新的代码项目列表
from authServer.v2.oauthclient.oauthrepos import OauthRepo
api.add_resource(OauthRepo, '/repos/<string:src_type>/<string:user_uuid>')   # 代码列表

# /api/v2.0/oauths/webhooks/<string:src_type>/<string:repo_name>  授权平台可以对某个项目具有 hooks 权限;设置部署公钥
from authServer.v2.oauthclient.webhooks import SetWebHooks
api.add_resource(SetWebHooks, '/webhooks/<string:src_type>/<string:repo_name>')


from authServer.v2.oauthclient.webhooks import WebHooksInfo
api.add_resource(WebHooksInfo, '/webhooks')

# /api/v2.0/oauths/oauth/<string:src_type>/<string:user_uuid>  解除绑定
from authServer.v2.oauthclient.oauth import Oauth
api.add_resource(Oauth, '/oauth/<string:src_type>/<string:user_uuid>')




api.init_app(oauthv2)
