#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/9/5 下午5:57
"""

import requests


import json
import time
import uuid
from flask import request, jsonify, g, redirect, render_template
from flask_restful import Api, Resource



from authServer.oauth.send_build_msg import Send_Build_Msg, send_build_rabbit, github_Webhooks, send_build_rabbit_by_repouuid
from authServer.pyTools.tools.codeString import request_result


from authServer.tools.decorate import get_varbox_from_headers, \
    request_form_git_build, image_repository_is_exist

from authServer.models.hub_db_meta import Session, GitHubOauth, CodeRepo

from authServer.models.db_opt import git_hub_oauth

from authServer.common.decorate import get_token_from_headers_check, check_headers, get_userinfo_by_payload

from authServer.v1.oauthclient.github.giturl import create_oauth_url





class Webhooks(Resource):
    def post(self):

        from authServer.common.oauthclient.githubApi import GithubWebHookInfo

        ret = GithubWebHookInfo()

        return jsonify(ret)



def user_info(token):
    headers = {
        'authorization': 'token ' + str(token)
    }
    try:
        r = requests.get('https://api.github.com/user', headers=headers, timeout=5)
        return r.status_code, r.json()
    except Exception as msg:
        return 300, msg.message




def update_git_hub_oauth(uid, token, src_type, update_token=False):

    if src_type == 'github':
        status_code, json_ret = user_info(token=token)
        if status_code != 200:
            return request_result(100, ret=json_ret)

        try:
            git_name = json_ret['login']
            git_uid = json_ret['id']
            git_emain = json_ret['email']
        except Exception as msg:
            print msg.message
            return request_result(403, ret={"msg": msg.message})
    elif src_type == 'coding':
        from authServer.common.oauthclient.CodingApi import GetUserInfo
        status_code, json_ret = GetUserInfo(access_token=token)

        if status_code is False:
            return request_result(100, ret=json_ret)

        try:
            git_name = json_ret['data']['global_key']

            print 'global_key'
            print git_name
            git_uid = json_ret['data']['id']
            git_emain = ''
        except Exception as msg:
            print msg.message
            return request_result(403, ret={"msg": msg.message})

    try:
        print "sdsdsd-s-d-sd-s-ds"
        if update_token:
            print 'ssdsds0d-s-ds-d-s-ds-d-s-d-s-ds-'
            g.db_session.query(GitHubOauth).filter(GitHubOauth.uid == uid, GitHubOauth.src_type == src_type).update(
                {"git_name": git_name, "git_emain": git_emain, "git_uid": git_uid, 'access_token': token})
        else:
            g.db_session.query(GitHubOauth).filter(GitHubOauth.uid == uid, GitHubOauth.src_type == src_type).update(
                {"git_name": git_name, "git_emain": git_emain, "git_uid": git_uid})
        g.db_session.commit()
    except Exception as msg:
        print msg.message
        ret = request_result(403, ret={"msg": msg.message})
    finally:
        ret = request_result(0, ret={'git_name': git_name, 'git_uid': git_uid})
        return ret





## 获取代码列表
@check_headers
@get_userinfo_by_payload
def github_repo_list(kwargs):
    uid = kwargs['uid']
    ret = g.db_session.query(GitHubOauth).filter(GitHubOauth.uid == kwargs['uid']).first()

    if ret is None:
        ret = request_result(103)
        return ret

    access_token = ret.access_token
    if access_token is None or '' == access_token:
        ret = request_result(104)
        return ret

    git_name = ret.git_name
    git_uid = ret.git_uid

    # 还没有获取用户信息,需要获取用户信息并更新到数据表
    # if git_name is None or ret.git_emain is None or git_uid is None:
    if git_name is None or git_uid is None:  # 对于不显示email的用户设置，无法得到用户邮箱

        src_type = "github"  # 暂时这样
        ret_user = update_git_hub_oauth(uid=uid, token=access_token, src_type=src_type)

        if ret_user['status'] != 0:
            return ret_user

        git_name = ret_user['result']['git_name']
        git_uid = ret_user['result']['git_uid']

    from authServer.common.oauthclient.repolist import refresh_repo_list

    # 是否强制刷新
    try:
        refresh_c = request.args.get('refresh', '').decode('utf-8').encode('utf-8').lower()
    except Exception as msg:
        return request_result(706, ret=msg.message)

    if refresh_c == 'true':   # 执行强制刷新操作
        refresh_repo_list(access_token, git_name, uid, git_uid)

    # 用户的 uid, 获取 github_repo 数据   github 项目列表
    ret_github_repo = g.db_session.query(CodeRepo).filter(CodeRepo.uid == str(uid)).all()

    if ret_github_repo is None or len(ret_github_repo) <= 0:
        # 如果数据不存在，强制刷新(从github请求)
        refresh_repo_list(access_token, git_name, uid, git_uid)
        ret_github_repo = g.db_session.query(CodeRepo).filter(CodeRepo.uid == str(uid)).all()

    repo_list = list()
    for node in ret_github_repo:
        repo_list.append(
            {'repo_name': node.repo_name, 'git_uid': node.repo_uid, 'is_hook': node.is_hook,
             'id': node.id, 'html_url': node.html_url, 'ssh_url': node.ssh_url,
             'url': node.url, 'description': node.description})

    return request_result(0, ret=repo_list)



class GithubRepo(Resource):
    def get(self):
        """
        @apiDescription   获取github 项目列表
        @apiVersion 1.0.0
        @apiHeader {String} token 请求接口的token,放在请求头中
        @api {get} /oauth/githubrepo
        @apiName GithubRepo

        @apiParam {String} refresh 默认没有该参数;强制从github获取数据,并更新数据库请求地址:/oauth/githubrepo?refresh=true
        @apiErrorExample {json} Error-Response:
        {
          "msg": "OK",
          "result": [
            {
              "git_uid": "6070423",
              "id": 14,
              "is_hook": 0,
              "repo_name": "beego"
            },
            {
              "git_uid": "6070423",
              "id": 15,
              "is_hook": 0,
              "repo_name": "crawler"
            }
          ],
          "status": 0
        }
            成功:result 是一个列表,每一个元素数据是一个代码项目工程,其中 repo_name 是项目名:
        """
        return jsonify(github_repo_list())





@get_token_from_headers_check
@get_varbox_from_headers
def create_web_hook(payload, var_box):
    print var_box
    print payload

    payload = json.loads(payload)
    uid = payload['uid']

    ret = git_hub_oauth(uid=uid)
    if ret is None:
        ret = request_result(103)
        return ret

    access_token = ret.access_token
    if access_token is None or '' == access_token:
        ret = request_result(104)
        return ret

    git_name = ret.git_name

    from authServer.common.oauthclient.githubApi import SetGitHook

    return SetGitHook(git_name, var_box, access_token, uid, del_hooks=True)





class GithubHooks(Resource):

    def post(self):
        """
        @apiDescription   授权平台可以对某个项目具有 hooks 权限
        @apiVersion 1.0.0
        @apiHeader {String} token  请求接口的token,放在请求头中
        @apiHeader {String} varbox 需要授权的用户项目
        @api {post} /oauth/githubhooks

        @apiSuccessExample {json} Success-Response:
        {
          "msg": "OK",
          "result": {
            "active": true,
            "config": {
              "content_type": "json",
              "secret": "********",
              "url": "http://index.boxlinker.com:8080/oauth/webhook"
            },
            "created_at": "2016-10-08T07:24:49Z",
            "events": [
              "push",
              "pull_request"
            ],
            "id": 10236269,
            "last_response": {
              "code": null,
              "message": null,
              "status": "unused"
            },
            "name": "web",
            "ping_url": "https://api.github.com/repos/liuzhangpei/Dockerfile-back/hooks/10236269/pings",
            "test_url": "https://api.github.com/repos/liuzhangpei/Dockerfile-back/hooks/10236269/test",
            "type": "Repository",
            "updated_at": "2016-10-08T07:24:49Z",
            "url": "https://api.github.com/repos/liuzhangpei/Dockerfile-back/hooks/10236269"
          },
          "status": 0
        }
        """
        return jsonify(create_web_hook())

# 代码构建
class GithubBuild(Resource):
    def put(self):
        """ 立即构建镜像 """
        return jsonify(github_rightaway_build())




@get_token_from_headers_check
@get_varbox_from_headers   # 此时 varbox 里传入的是 自动构建数据库记录的 id
def github_rightaway_build(payload, var_box):
    return send_build_rabbit_by_repouuid(var_box)



@get_token_from_headers_check
def RelateGithubRedirect(payload):
    payload = json.loads(payload)
    uid = payload['uid']
    print payload
    print type(payload)

    url_state = create_oauth_url(uid)

    return request_result(0, ret={'msg': url_state})



# http://0.0.0.0:8081/oauth/relategithub
class RelateGithub(Resource):
    def get(self):

        return redirect('/oauth/githubredirect')

        ret = get_oauth_url_state()

        if 'status' in ret and ret['status'] != 0:
            return jsonify(ret)

        if 'result' in ret and 'msg' in ret['result']:
            return redirect('/oauth/githubredirect')

        return jsonify(ret)