#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/11/9 17:02
"""


import requests

import json
import uuid
from flask import request, jsonify, g, redirect, render_template
from flask_restful import Api, Resource

import authServer.conf.openOauth as openOauth
from authServer.pyTools.tools.codeString import request_result

from authServer.models.hub_db_meta import Session, GitHubOauth, CodeRepo
from authServer.pyTools.token.token import gen_token, get_payload, make_random_key


# 第三方oauth授权,回调接口
class CallBack(Resource):
    def get(self):
        # request_headers = dict(request.headers)

        print "ssssssssss-s-s-s--s-s-s-s-s-s-"
        try:
            code = request.args.get('code', '').decode('utf-8').encode('utf-8')
            # 如果不考虑用户篡改认证链接,可以不用加state
            state = request.args.get('state', '').decode('utf-8').encode('utf-8')
        except Exception as msg:
            return jsonify(request_result(code=602))

        if code == '' or state == '':
            return jsonify(request_result(code=706))

        payloadRet = get_payload(token=state)  # token  合法
        if payloadRet['status'] != 0:
            return jsonify(payloadRet)

        payload = payloadRet['result']['payload']

        payload = json.loads(payload)

        uid = payload['uid']

        src_type = payload['src_type']

        headers = {'accept': 'application/json'}
        if src_type == "github":
            params = {
                'code': code,
                'client_id': openOauth.github_client_id,
                'client_secret': openOauth.github_client_secret
            }
            try:
                response = requests.post(openOauth.github_access_token_url, params=params, headers=headers)
                token = response.json()['access_token']
                oauthret = g.db_session.query(GitHubOauth).filter(
                    GitHubOauth.uid == str(uid), GitHubOauth.src_type == src_type).first()
            except Exception as msg:
                print msg.message
                return jsonify(request_result(code=602, ret={"msg": msg.message}))
        elif src_type == "coding":
            try:
                token_url = openOauth.coding_access_token_url.format(code)
                response = requests.post(token_url, headers=headers)

                print "response.json()"
                print code
                print response.json()
                # token = response.json()['access_token']

                response_json = response.json()
                if 'access_token' in response_json:
                    token = response_json['access_token']
                else:
                    responseRet = request_result(code=100, ret=response_json)
                    return jsonify(responseRet)
                print token

                oauthret = g.db_session.query(GitHubOauth).filter(
                    GitHubOauth.uid == str(uid), GitHubOauth.src_type == src_type).first()
            except Exception as msg:
                print msg.message
                ret = request_result(code=602, ret={"msg": msg.message})
                return jsonify(ret)

        else:
            return jsonify(request_result(code=706, ret="src type is error"))

        # 把token 存起来
        from authServer.oauth.github import update_git_hub_oauth
        if oauthret is None:

            from authServer.pyTools.tools.timeControl import get_timestamp_13
            time_str = str(get_timestamp_13)
            auth_id = uuid.uuid3(uuid.NAMESPACE_DNS, str(uid) + str(src_type) + time_str).__str__()
            github_oauth = GitHubOauth(id=auth_id, uid=uid, access_token=token, src_type=src_type)
            g.db_session.add(github_oauth)
            g.db_session.commit()

            ret = update_git_hub_oauth(uid=uid, token=token, src_type=src_type)
        else:
            ret = update_git_hub_oauth(uid=uid, token=token, src_type=src_type, update_token=True)


        if 'redirect_url' not in payload:
            redirect_url = "oauth/gredirect"
        else:
            red_url = payload['redirect_url']
            redirect_url = "oauth/gredirect?redirect=" + red_url

        return redirect(redirect_url)