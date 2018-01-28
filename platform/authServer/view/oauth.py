#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/9/5 下午6:06
"""

# oauthclient

from flask import Blueprint, redirect, render_template, request
from flask_restful import Api, Resource

from authServer.oauth.github import Webhooks, GithubRepo, GithubHooks,\
    GithubBuild, RelateGithub

oauth = Blueprint('oauth', __name__, url_prefix='/oauth')

api = Api()

@oauth.route('/test')
def test():
    print 'http://hostname/oauth/test is ok'
    return 'http://hostname/oauth/test is ok'


# http://0.0.0.0:8025/oauth/tt
@oauth.route('/tt')
def tt():
    redirect_url = "oauth/gredirect?redirect=" + "http://test.boxlinker.com/building/create"
    return redirect(redirect_url)



@oauth.route('/gredirect', methods=['GET', 'POST'])
def front_building():
    print 'front_building.html'

    code = request.args.get('redirect', '').decode('utf-8').encode('utf-8')
    print code
    if code == '':
        item = 'http://test.boxlinker.com/building/create'
    else:
        item = code
    return render_template('front_building.html', item=item)


api.add_resource(RelateGithub, '/relategithub')


from authServer.common.oauthclient.oauthCallback import CallBack
api.add_resource(CallBack, '/callback')

# /oauth/webhook
api.add_resource(Webhooks, '/webhook')

# 获取用户认证地址
from authServer.v1.oauthclient.github.github import GitOauthUrl
api.add_resource(GitOauthUrl, '/oauthurl') # /oauth/oauthurl  # 已经放入新接口


# 获取代码项目列表
api.add_resource(GithubRepo, '/githubrepo')


# 授权平台可以对某个项目具有 hooks 权限
api.add_resource(GithubHooks, '/githubhooks')


# 代码构建 post
api.add_resource(GithubBuild, '/githubbuild')  # 已经放入新接口


api.init_app(oauth)
