#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/10/20 11:02
"""


import uuid
from flask_restful import Resource

import json
import requests
from flask import request, jsonify, g

from authServer.pyTools.tools.codeString import request_result

from authServer.common.decorate import check_headers, get_userinfo_by_payload


from authServer.tools.db_check import signup_check, check_username_password

from authServer.conf.conf import VERIFY_CODE, VERIFY_CODE_URL

from authServer.models.hub_db_meta import OrgsUser, OrgsBase, UserBase


from authServer.user.UserBaseHandle import UserBaseHandle
from authServer.common.usercenter.token import get_login_token, get_access_token



def signup_request_get_msg_from_json(func):
    """ 从注册请求的json数据中获取,注册信息 """
    def _deco(kwargs):
        try:

            data = request.data
            data_json = json.loads(data)
            username = data_json.get('user_name', '').decode('utf-8').encode('utf-8')
            password = data_json.get('pass_word', '').decode('utf-8').encode('utf-8')
            email = data_json.get('email', '').decode('utf-8').encode('utf-8')
            code_id = data_json.get('code_id', '').decode('utf-8').encode('utf-8')
            code_str = data_json.get('code_str', '').decode('utf-8').encode('utf-8')
            if username == '' or password == '' or email == '':
                return request_result(706)
            kwargs['username'] = username
            kwargs['password'] = password
            kwargs['email'] = email
            kwargs['code_id'] = code_id
            kwargs['code_str'] = code_str
        except Exception as msg:
            return request_result(710, ret=msg.message)

        return func(kwargs)
    return _deco


def verify_code(func):
    def _deco(kwargs):
        if VERIFY_CODE is False:
            return func(kwargs)
        try:
            # 'http://verify-code.boxlinker.com/check_code/$CODE_ID?code=$CODE_STR'
            verify_url = VERIFY_CODE_URL.replace('$CODE_ID', kwargs['code_id']).replace('$CODE_STR', kwargs['code_str'])

            print 'verify_code'
            print verify_url

            response = requests.get(url=verify_url, timeout=4)
            print response.status_code

            if response.json()['status'] != 0:
                return request_result(805)
        except Exception as msg:
            return request_result(100, ret=msg.message)
        return func(kwargs)
    return _deco


@signup_request_get_msg_from_json
@verify_code
@signup_check
def sign_up(kwargs):
    # 主服务系统注册
    user_base = UserBaseHandle()
    return user_base.siggup_init(user_name=kwargs['username'],
                                 email=kwargs['email'],
                                 password=kwargs['password'])



class UserSignup(Resource):
    def post(self):
        """
        @apiGroup User
        @apiDescription  注册用户操作
        @apiVersion 1.0.0
        @api {post} /api/v1.0/usercenter/users  用户注册
        @apiExample {post} Example usage: data json

        post http://auth.boxlinker.com/api/v1.0/usercenter/users  ParamExample
        {
            "user_name": username,
            "pass_word": password,
            "email": email,
            "code_id": code_id,
            "code_str": code_str
        }

        @apiParam {String} user_name  用户名
        @apiParam {String} pass_word  用户密码
        @apiParam {String} email     用户邮箱(唯一)
        @apiParam {String} code_id   验证码id
        @apiParam {String} code_str  验证码字符内容
        """
        k = dict()
        return jsonify(sign_up(kwargs=k))

    def get(self):
        """
        @apiGroup User
        @apiDescription  用户信息
        @apiVersion 1.0.0
        @api {get} /api/v1.0/usercenter/users  用户信息
        @apiExample {get} Example usage: data json

        get http://auth.boxlinker.com/api/v1.0/usercenter/users  ParamExample

        @apiSuccessExample {json} 返回用户信息:
            {
                "msg": "OK",
                "result":
                {
                    "email": "1212@12.com",
                    "expires": 1478399550.918677,
                    "github": 1,
                    "is_user": "1",     # 1:用户账号token;  0:组织token
                    "orga_uuid": "a58385e0-7fdc-3458-a7cf-7d3764b9ac84",
                    "role_uuid": "1",
                    "salt": "86387afc4c49a48d7d671845",
                    "tokenid": "9a3d26fea0c7e5a16785e3e7",
                    "uid": "a58385e0-7fdc-3458-a7cf-7d3764b9ac84",
                    "user_ip": "127.0.0.1",
                    "user_name": "liuzhangpei",
                    "user_orag": "liuzhangpei",
                    "user_orga": "liuzhangpei",
                    "user_role": "1",
                    "user_uuid": "a58385e0-7fdc-3458-a7cf-7d3764b9ac84"
                },
                "status": 0
            }
        """
        from authServer.common.usercenter.users import get_user_info
        return jsonify(get_user_info())




class TokenUser(Resource):
    def get(self):
        """
        @apiGroup User
        @apiDescription  获取用户最基本信息
        @apiVersion 1.0.0
        @api {get} /api/v1.0/usercenter/tokens/user  获取用户最基本信息
        @apiHeader {String} token 请求接口的token,放在请求头中
        @apiExample {get} Example usage: data json
        get http://auth.boxlinker.com/api/v1.0/usercenter/tokens/user  ParamExample

        @apiSuccessExample {json} 返回用户信息:
            {
                "msg": "OK",
                "result":
                {
                    "is_user": "1",     # 用户token,还是 组织token
                    "orga_uuid": "ac0b5a11-96aa-37a5-992f-e5a43fe5c55d",
                    "role_uuid": "200",
                    "user_name": "zhangsai",
                    "user_orga": "zhangsai",
                    "user_uuid": "ac0b5a11-96aa-37a5-992f-e5a43fe5c55d"
                },
                "status": 0
            }
        """
        from authServer.common.usercenter.users import get_user_base_info
        return jsonify(get_user_base_info())

class UserLogin(Resource):
    @staticmethod
    @check_username_password
    def user_login(username, password):
        return get_login_token(username=username)

    def post(self):
        """
        @apiGroup User
        @apiDescription 用户登录, 用户名/也可能是邮箱 和 密码
        @apiVersion 1.0.0
        @apiName 用户登录
        @api {post} /api/v1.0/usercenter/tokens  用户登录
        @apiExample {post} Example usage:
        post http://auth.boxlinker.com/api/v1.0/usercenter/tokens  Example:
            {
                "pass_word": password,
                "user_name": asss,
            }

        @apiSuccessExample {json} 返回token信息:
        {
            "msg": "OK",
            "result":
            {
                "token": "eyJ1aWQiOiAiYTBjN2UNzc2QiLCAidyvOEm",
                "tokenid": "64325dedb56f951a65d8526a"
            },
            "status": 0
        }
        @apiParam {String} user_name  用户名（其中user_name可以是用户名或邮箱）
        @apiParam {String} pass_word  用户密码
        """
        try:

            print 'UserLogin--'
            print request
            data = request.data

            data_json = json.loads(data)
            pass_word = data_json.get('pass_word', '').decode('utf-8').encode('utf-8')
            user_name = data_json.get('user_name', '').decode('utf-8').encode('utf-8')
            if pass_word == '' or user_name == '':
                return request_result(706)
        except Exception as msg:
            print msg.message
            return request_result(710, ret=msg.message)
        return jsonify(self.user_login(username=user_name, password=pass_word))


    @staticmethod
    @check_headers
    @get_userinfo_by_payload
    def change_token(kwargs):
        try:
            org_base = g.db_session.query(OrgsBase).filter(
                OrgsBase.org_id == kwargs['orga_uuid_arg']).first()

            org_user = g.db_session.query(OrgsUser).filter(
                OrgsUser.org_id == kwargs['orga_uuid_arg'], OrgsUser.uid == kwargs['uid']).first()

            if org_base is None or org_user is None:
                return request_result(806)

            role = org_user.role
            org_name = org_base.org_name

            return get_access_token(
                user_name=kwargs['user_name'], email=kwargs['email'], uid=kwargs['uid'],
                user_role=role, user_orag=org_name, orga_uuid=kwargs['orga_uuid_arg'])
        except Exception as msg:
            return request_result(403, ret=msg.message)

    def put(self):
        """
        @apiGroup User
        @apiDescription  用户账号切换到组织账号下的token切换
        @apiVersion 1.0.0
        @apiHeader {String} token    请求API的token
        @api {put} /api/v1.0/usercenter/tokens  身份切换
        @apiExample {post} Example usage:
        post http://auth.boxlinker.com/api/v1.0/usercenter/tokens  Example:
            {
                "orga_uuid": "8425b6eb-eb77-382f-9acb-385d85eab70c"
            }

        @apiParam {String} orga_uuid  组织id
        """
        try:
            data = request.data
            data_json = json.loads(data)
            orga_uuid = data_json.get('orga_uuid', '').decode('utf-8').encode('utf-8')
            if orga_uuid == '':
                return request_result(706)
        except Exception as msg:
            return request_result(710, ret=msg.message)

        k = dict()
        k['orga_uuid_arg'] = orga_uuid

        return jsonify(self.change_token(k))


    def delete(self):
        """
        @apiGroup User
        @apiDescription  退出登录,清除token数据
        @apiVersion 1.0.0
        @apiHeader {String} token    请求API的token
        @api {delete} /api/v1.0/usercenter/tokens  退出登录
        """
        from authServer.common.usercenter.token import clear_token
        return jsonify(clear_token())

    def get(self):
        """
        @apiGroup User
        @apiDescription  验证token, k8s token 认证
        @apiVersion 1.0.0
        @apiHeader {String} token    请求API的token
        @api {get} /api/v1.0/usercenter/tokens  验证token
        """
        from authServer.common.usercenter.token import check_token_head_token
        return jsonify(check_token_head_token())


@check_headers
@get_userinfo_by_payload
def userFuzzy(kwargs):
    from sqlalchemy import or_
    use = '%' + kwargs['user_fuzzy'] + '%'
    user_bases = g.db_session.query(UserBase).filter(
        or_(UserBase.username.like(use), UserBase.email.like(use))
    ).offset(0).limit(15)

    user_list = list()

    for user_node in user_bases:
        user_d = dict()

        if user_node.username == 'admin' or user_node.username == kwargs['user_name']:
            continue

        user_d['username'] = user_node.username
        user_d['user_id'] = user_node.user_id
        user_d['email'] = user_node.email
        user_d['logo'] = user_node.logo
        user_d['user_id'] = user_node.user_id
        user_list.append(user_d)

    return request_result(0, ret=user_list)

class UserFuzzy(Resource):
    def get(self, user_fuzzy):
        """
        @apiGroup User
        @apiDescription       用户列表模糊查询
        @apiVersion 1.0.0
        @apiHeader {String} token 请求接口的token,放在请求头中
        @api {get} /api/v1.0/usercenter/users/list/<string:user_fuzzy>   用户列表模糊查询

        @apiParamExample {json} Request-Param-Example:
            {
                "status": 0,
                "msg": "OK",
                "result": "user.uid"
            }
            成功时,result返回用户uid
        @apiParam {String} user_fuzzy   用户名或用户注册的邮箱的部分信息
        """

        k = dict()
        k['user_fuzzy'] = user_fuzzy

        return jsonify(userFuzzy(kwargs=k))