#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/11/10 10:28
"""

import json

import authServer.conf.openOauth as openOauth

from flask import request, jsonify, g, redirect, render_template
from flask_restful import Api, Resource


from authServer.pyTools.tools.codeString import request_result
from authServer.common.decorate import check_headers, get_userinfo_by_payload


# 创建webhooks
@check_headers
@get_userinfo_by_payload
def CreateWebHook(kwargs):

    from authServer.v2.oauthclient.oauthrepos import GetOauthInfo

    retbool, result = GetOauthInfo(uid=kwargs['uid'], src_type=kwargs['src_type_arg'])
    if retbool is False:
        return result

    access_token, git_name, uid, git_uid = result


    from authServer.common.oauthclient.githubApi import SetGitHook
    from authServer.common.oauthclient.webhooks import SetWebHook

    if kwargs['src_type_arg'] == 'github':
        return SetGitHook(git_name, kwargs['repo_name_arg'], access_token, uid, del_hooks=True)
    elif kwargs['src_type_arg'] == 'coding':
        return SetWebHook(git_name=git_name, repo_name=kwargs['repo_name_arg'],
                          access_token=access_token, uid=uid, src_type=kwargs['src_type_arg'])



class SetWebHooks(Resource):
    def post(self, src_type, repo_name):
        """
        @apiGroup  WebHooks
        @apiDescription   授权平台可以对某个项目具有 hooks 权限
        @apiVersion 1.0.0

        @api {post} /api/v2.0/oauths/webhooks/<string:src_type>/<string:repo_name> 设置webhook

        @apiHeader {String} token  请求接口的token,放在请求头中

        @apiParam {String} src_type   代码源类型;github or coding
        @apiParam {String} repo_name  代码项目名
        """

        if src_type not in openOauth.OpenType:
            return jsonify(request_result(706, ret='src_type is error'))

        k = dict()
        k['src_type_arg'] = src_type
        k['repo_name_arg'] = repo_name


        return jsonify(CreateWebHook(kwargs=k))


class WebHooksInfo(Resource):
    def post(self):
        """
        @apiGroup  WebHooks
        @apiDescription   接受第三方代码平台的webhooks通知;不需要前端页面提供接口
        @apiVersion 1.0.0

        @api {post} /api/v2.0/oauths/webhooks/  接受webhooks通知

        http://coding.livenowhy.com:8080/api/v2.0/oauths/webhooks
        """

        # User-Agent
        # value: GitHub-Hookshot/d9ba1f0    github
        # value: Coding.net Hook            coding
        request_headers = dict(request.headers)
        print "-- WebHooksInfo -- 01"
        for kk in request_headers:
            print "kk: " + str(kk)
            print "kk: " + str(kk) + "     value: " + str(request_headers[kk])

        print "-- WebHooksInfo -- 02"

        userAgent = request_headers.get('User-Agent', '')

        if 'GitHub' in userAgent:
            print "userAgent --> GitHub"
            from authServer.common.oauthclient.githubApi import GithubWebHookInfo
            ret = GithubWebHookInfo()
            return jsonify(ret)
        elif 'Coding.net' in userAgent:
            print 'userAgent --> Coding.net'


        try:
            print '-----plyload----'
            payload = json.loads(request.data)
            print type(payload)
            print payload
        except Exception as msg:
            print msg.message
            return request_result(100, ret=msg.message)


        return jsonify(request_result(0))