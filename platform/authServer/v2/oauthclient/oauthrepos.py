#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/11/9 14:53
"""



import json

from flask import jsonify, g, request
from authServer.common.decorate import check_headers, get_userinfo_by_payload

from authServer.pyTools.tools.codeString import request_result

import time
from authServer.pyTools.token.token import gen_token

import authServer.conf.openOauth as openOauth

from flask_restful import Resource

from authServer.models.db_opt import GitHubOauth



def GetOauthInfo(uid, src_type):
    """ 由用户名 和 代码源 获取 oauth 认证信息 """
    ret = g.db_session.query(GitHubOauth).filter(
        GitHubOauth.uid == uid, GitHubOauth.src_type == src_type).first()

    if ret is None:
        return False, request_result(103)

    access_token = ret.access_token
    if access_token is None or '' == access_token:
        return False, request_result(104)

    git_name = ret.git_name
    git_uid = ret.git_uid

    # 还没有获取用户信息,需要获取用户信息并更新到数据表
    # if git_name is None or ret.git_emain is None or git_uid is None:
    if git_name is None or git_uid is None:  # 对于不显示email的用户设置，无法得到用户邮箱

        from authServer.oauth.github import update_git_hub_oauth

        ret_user = update_git_hub_oauth(uid=uid, token=access_token, src_type=src_type)
        if ret_user['status'] != 0:
            return False, ret_user

        git_name = ret_user['result']['git_name']
        git_uid = ret_user['result']['git_uid']

    return True, (access_token, git_name, uid, git_uid)



# 刷新获取代码列表
@check_headers
@get_userinfo_by_payload
def repo_list(kwargs):
    retbool, result = GetOauthInfo(uid=kwargs['user_uuid_arg'], src_type=kwargs['src_type_arg'])

    if retbool is False:
        return result

    access_token, git_name, uid, git_uid = result

    from authServer.common.oauthclient.repolist import refresh_repos

    return refresh_repos(access_token, git_name, uid, git_uid, src_type=kwargs['src_type_arg'])


# 获取代码列表
@check_headers
@get_userinfo_by_payload
def get_repo_list(kwargs):
    from authServer.common.oauthclient.repolist import DbGetRepoList
    retbool, result = GetOauthInfo(uid=kwargs['user_uuid_arg'], src_type=kwargs['src_type_arg'])


    if retbool is False:
        return result

    access_token, git_name, uid, git_uid = result
    return DbGetRepoList(access_token, git_name, uid, git_uid, src_type=kwargs['src_type_arg'])


class OauthRepo(Resource):
    def put(self, src_type, user_uuid):
        """
        @apiGroup  OauthRepo
        @apiDescription    刷新获取用户对应代码平台下的代码项目, 从对应平台获取最新的数据
        @apiVersion 2.0.0
        @apiHeader {String} token 请求接口的token,放在请求头中
        @api {put} /api/v2.0/oauths/repos/<string:src_type>/<string:user_uuid>   刷新代码项目


        @apiSuccessExample {json} Success-Response:
        status 为 0 成功,其中result-->msg中即用户需要点击进行授权的地址
        {
            "msg": "OK",
            "result":
            {
                "msg": "https://github.com/login/oauth/authorize?client_id=44df81c41ee415b7debd&scope=user%20repo&state=eyJleHBpcmVzIjogMTQ3NTgzNzAxNi4wNzg2ODksICJzYWx0IjogIjAuMjQwNjIyOTU2NjgyIiwgInVpZCI6ICIzIn2ag7sMa7sSf6-vmhEMykRL"
            },
            "status": 0
        }

        @apiParam {String} src_type 第三方平台类型; github, coding
        @apiParam {String} user_uuid  用户uuid
        """

        if src_type not in openOauth.OpenType:
            return jsonify(request_result(706, ret='src_type is error'))

        k = dict()
        k['src_type_arg'] = src_type
        k['user_uuid_arg'] = user_uuid

        repo_list(kwargs=k)

        return jsonify(repo_list(kwargs=k))


    def get(self, src_type, user_uuid):
        """
        @apiGroup  OauthRepo
        @apiDescription         获取用户代码对应平台下的代码项目
        @apiVersion 2.0.0
        @apiHeader {String} token 请求接口的token,放在请求头中
        @api {get} /api/v2.0/oauths/repos/<string:src_type>/<string:user_uuid>   获取用户代码对应平台下的代码项目


        @apiSuccessExample {json} Success-Response:
        status 为 0 成功,其中result-->msg中即用户需要点击进行授权的地址
        {
            "msg": "OK",
            "result":
            {
                "msg": "https://github.com/login/oauth/authorize?client_id=44df81c41ee415b7debd&scope=user%20repo&state=eyJleHBpcmVzIjogMTQ3NTgzNzAxNi4wNzg2ODksICJzYWx0IjogIjAuMjQwNjIyOTU2NjgyIiwgInVpZCI6ICIzIn2ag7sMa7sSf6-vmhEMykRL"
            },
            "status": 0
        }

        @apiParam {String} src_type 第三方平台类型; github, coding
        @apiParam {String} user_uuid  用户uuid
        """

        if src_type not in openOauth.OpenType:
            return jsonify(request_result(706, ret='src_type is error'))

        k = dict()
        k['src_type_arg'] = src_type
        k['user_uuid_arg'] = user_uuid

        repo_list(kwargs=k)

        return jsonify(get_repo_list(kwargs=k))