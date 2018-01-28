#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/8/16 2:09
@func: 登录
"""

import json
import time

from flask import jsonify, g
from flask_restful import Resource

import authServer.pyTools.token.token as TK
from authServer.models.hub_db_meta import AccessToken
from authServer.tools.db_check import check_username_password, is_email
from authServer.tools.decorate import request_form_get_username_password


from authServer.common.decorate import request_form_get_tokenid_token
from authServer.conf.conf import GLOBALS_TOKEN
from authServer.pyTools.tools.codeString import request_result

from authServer.common.usercenter.token import check_token_head_token, GenerateToken


from authServer.common.usercenter.token import get_login_token, check_token




@request_form_get_username_password
@check_username_password
def _login(username, password):
    return get_login_token(username=username)


class Login(Resource):
    def post(self):
        """
        @apiDescription 用户登录, 用户登录 用户名/也可能是邮箱 和 密码
        @apiVersion 1.0.0
        @apiName 用户登录
        @api {post} /user/login
        @apiExample {post} Example usage: 数据放进 form 中
        post http://auth.boxlinker.com/user/login  Python Example

            url = 'http://auth.boxlinker.com'

            def test_login(username, password):
                payload = {
                    'user_name': username,
                    'password': password
                }
                urltag = url + '/user/login'
                response = requests.request('POST', url=urltag, data=payload)
                return response.text.decode('utf-8').encode('utf-8')

        @apiParam {String} username  用户名（其中username可以是用户名或邮箱email）
        @apiParam {String} password  用户密码
        """
        return jsonify(_login())



def _flush_token(tokenid, token):
    """
    刷新token
    :param tokenid:
    :param token:
    """
    retmsg = TK.verify_token(key=g.secret_key, token=token)
    if retmsg['status'] != 0:
        return retmsg

    retdict = GenerateToken(user_uuid=retmsg['result']['msg']['uid'],
                            user_name=retmsg['result']['msg']['user_name'],
                            email=retmsg['result']['msg']['email'],
                            user_role=retmsg['result']['msg']['user_role'],
                            user_orga=retmsg['result']['msg']['user_orga'],
                            tokenid=tokenid,
                            orga_uuid=retmsg['result']['msg']['orga_uuid'])  # 刷新token时,传入 tokenid
    if retdict['status'] != 0:
        return retdict

    try:
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        g.db_session.query(AccessToken).filter(AccessToken.token_uuid == tokenid).update(
            {"token": retdict['result']['token'], "update_time": now})
        g.db_session.commit()
    except Exception as msg:
        retdict = request_result(403, ret={"msg": msg.message})
    finally:
        return retdict


def check_token_ret_bool(tokenid, token):
    """ 校验token, 返回bool """
    if tokenid in GLOBALS_TOKEN and GLOBALS_TOKEN[tokenid] == token:  # 此时系统token符合
        return True

    if tokenid not in GLOBALS_TOKEN:
        ret = g.db_session.query(AccessToken).filter(AccessToken.token_uuid == tokenid, AccessToken.deleted=='0').first()
        if ret is not None and ret.token == token:
            return True
    return False




@request_form_get_tokenid_token
def flush_token(tokenid, token):
    return _flush_token(tokenid, token)

class FlushToken(Resource):
    def post(self):
        """
        @apiDescription 刷新系统token
        @apiVersion 1.0.0
        @apiName 用户登录
        @api {POST} /user/flush_token

        @apiParam {String} tokenid  token id
        @apiParam {String} token    token
        """
        return jsonify(flush_token())

    def get(self):
        return self.__class__.__name__


class CheckToken(Resource):
    """校验token"""
    def post(self):
        return jsonify(check_token())


from authServer.common.usercenter.token import log_out

class LogOut(Resource):

    def post(self):
        """
        @apiDescription 退出登录
        @apiVersion 1.0.0
        @api {POST} /user/log_out

        @apiParam {String} tokenid  token id
        @apiParam {String} token    token
        """
        return jsonify(log_out())



class CheckTokenGet(Resource):
    def get(self):
        """
        @apiDescription 验证token, k8s token 认证
        @apiVersion 1.0.0
        @apiName 用户登录
        @api {get} /user/check_token_get

        @apiParam {String} token    token  (headers 中)
        """
        return jsonify(check_token_head_token())
