#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/11/8 10:26
"""

import json

from flask import jsonify, g, request
from authServer.common.decorate import check_headers, get_userinfo_by_payload

from authServer.pyTools.tools.codeString import request_result

import time
from authServer.pyTools.token.token import gen_token

import authServer.conf.openOauth as openOauth

from flask_restful import Resource


def create_oauth_url(uid, src_type, redirect_url):
    """ 生成带有用户信息的url认证地址, state 码 """
    state_msg = {
        'uid': str(uid),       # 用户uid
        'src_type': src_type,  # 第三方平台类型, github, coding
        'redirect_url': redirect_url,
        'expires': time.time() + 30 * 24 * 60 * 60
    }

    # state_msg['redirect_url'] = 'http://0.0.0.0:8046/api/v2.0/oauths/callback'
    state_ret = gen_token(key=g.secret_key, data=state_msg)

    if src_type == "github":
        return openOauth.user_oauth_url.format(state_ret)
    else:
        return openOauth.coding_oauth_url.format(state_ret)


@check_headers
@get_userinfo_by_payload
def get_oauth_url_state(kwargs):
    url_state = create_oauth_url(uid=kwargs['uid'], src_type=kwargs['src_type'], redirect_url=kwargs['redirect_url'])
    return request_result(0, ret={'msg': url_state})


class OauthUrl(Resource):
    def post(self):
        """
        @apiGroup  OauthUrl
        @apiDescription   获取用户授权跳转链接
        @apiVersion 2.0.0
        @apiHeader {String} token 请求接口的token,放在请求头中
        @api {post} /api/v2.0/oauths/oauthurl   获取用户授权跳转链接

        @apiExample {POST} Example usage:
            post  http://0.0.0.0:8025/api/v2.0/oauths/oauthurl

        {
            "src_type": "github",
            "redirect_url": "http://test.boxlinker.com/building/create"
        }

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
        @apiParam {String} redirect_url 跳转地址
        """

        try:
            data = request.data
            data_json = json.loads(data)

            src_type = data_json.get('src_type', '').decode('utf-8').encode('utf-8')  # .lower()
            redirect_url = data_json.get('redirect_url', '').decode('utf-8').encode('utf-8')  # .lower()

            if src_type not in openOauth.OpenType:
                return jsonify(request_result(706, ret="src type is error"))
        except Exception as msg:
            return request_result(706, ret=msg.message)

        k = dict()
        k['src_type'] = src_type
        k['redirect_url'] = redirect_url

        return jsonify(get_oauth_url_state(kwargs=k))