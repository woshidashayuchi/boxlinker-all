#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/10/26 18:23
"""


from flask import jsonify
from authServer.common.decorate import check_headers, get_userinfo_by_payload

from authServer.v1.oauthclient.github.giturl import create_oauth_url
from authServer.pyTools.tools.codeString import request_result


from flask_restful import Resource






@check_headers
@get_userinfo_by_payload
def get_oauth_url_state(kwargs):
    url_state = create_oauth_url(kwargs['uid'])
    return request_result(0, ret={'msg': url_state})


class GitOauthUrl(Resource):
    def get(self):
        """
        @apiGroup  OauthClient
        @apiDescription   获取用户授权跳转链接
        @apiVersion 1.0.0
        @apiHeader {String} token 请求接口的token,放在请求头中
        @api {get} /api/v1.0/oauthclient/githuboauthurl   获取用户授权跳转链接

        old:--> /oauth/oauthurl

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

        @apiErrorExample {json} Error-Response:
        {
            "msg": "An exception occurs",
            "result":
            {
                "msg": "Incorrect padding"
            },
            "status": 602
        }
        """
        return jsonify(get_oauth_url_state())