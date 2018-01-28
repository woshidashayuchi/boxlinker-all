#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/10/19 10:26
"""

import json
from flask import request
from authServer.pyTools.tools.codeString import request_result

from authServer.pyTools.token.token import get_payload

from authServer.pyTools.token.token import get_payload
from authServer.common.checktoken import system_check_token


def request_form_get_tokenid_token(func):
    """ 对于form中只有tokenid和token数据的请求,进行装饰器解析 """
    def _deco():
        try:
            # 用户名/也可能是邮箱 需要后台判断
            # 不使用 None 为了 .decode('utf-8').encode('utf-8') 不报错
            tokenid = request.form.get('tokenid', '').decode('utf-8').encode('utf-8')
            token = request.form.get('token', '').decode('utf-8').encode('utf-8')  # 密码
        except Exception as msg:
            retdict = request_result(601, ret={'msg': msg.message})
            return retdict

        # 传入的参数有问题
        if tokenid == '' or token == '':
            retdict = request_result(706)
            return retdict

        return func(tokenid, token)
    return _deco


# 从请求头中获取token数据
def get_token_from_headers(func):
    def _deco():
        try:
            # token = request.headers['token', ''].decode('utf-8').encode('utf-8')
            # headers 对象是 werkzeug.datastructures.EnvironHeaders
            token = request.headers.get('token', default='').decode('utf-8').encode('utf-8')
        except Exception as msg:
            retdict = request_result(601, ret={'msg': msg.message})
            return retdict
        if token == '':
            retdict = request_result(706)
            return retdict

        return func(token)
    return _deco


# 从请求头中获取token数据,并且验证token合法性
def get_token_from_headers_check(func):
    def _deco():
        try:
            token = request.headers.get('token', default='').decode('utf-8').encode('utf-8')
        except Exception as msg:
            retdict = request_result(601, ret={'msg': msg.message})
            return retdict
        if token == '':
            retdict = request_result(706)
            return retdict

        ret = get_payload(token=token)
        if ret['status'] != 0:
            return ret

        try:

            payload = ret['result']['payload']
            tokenid = json.loads(payload)['tokenid']

        except Exception as msg:
            return request_result(202, ret=msg.message)

        checkret = system_check_token(tokenid, token)

        if 'status' in checkret and checkret['status'] == 0:
            return func(payload=payload)
        else:
            print 'token error'
            return request_result(202, ret=checkret)
    return _deco

# get_token_from_headers_check 和 check_headers 区别在于  参数, 后期  删除 get_token_from_headers_check


def check_headers(func):
    """ 从请求头中获取token数据,并且验证token合法性, token payload 以字典方式传递"""
    def _deco(kwargs=dict()):
        try:
            token = request.headers.get('token', default='').decode('utf-8').encode('utf-8')
        except Exception as msg:
            return request_result(601, ret={'msg': msg.message})
        if token == '':
            return request_result(706)

        try:
            ret = get_payload(token=token)
            if ret['status'] != 0:
                return ret

            payload = ret['result']['payload']
            tokenid = json.loads(payload)['tokenid']

            checkret = system_check_token(tokenid, token)

            if 'status' in checkret and checkret['status'] == 0:
                kwargs['payload'] = payload
                return func(kwargs=kwargs)
            else:
                return request_result(202, ret=payload)
        except Exception as msg:
            return request_result(202, ret=msg.message)
    return _deco



def get_userinfo_by_payload(func):
    """ 通过 payload 获取用户名和用户id, 放在 kwargs 字典中"""
    def _deco(kwargs=dict()):
        try:
            payload = kwargs['payload']
            payload_d = json.loads(payload)
        except Exception as msg:
            return request_result(206, ret=msg.message)  # payload 中没有需要的信息

        if 'user_name' in payload_d and 'uid' in payload_d and 'email' in payload_d and 'orga_uuid' in payload_d:
            kwargs['user_name'] = payload_d['user_name'].decode('utf-8').encode('utf-8')
            kwargs['uid'] = payload_d['user_uuid'].decode('utf-8').encode('utf-8')
            kwargs['email'] = payload_d['email'].decode('utf-8').encode('utf-8')
            kwargs['orga_uuid'] = payload_d['orga_uuid'].decode('utf-8').encode('utf-8')
            kwargs['role_uuid'] = str(payload_d['role_uuid']).decode('utf-8').encode('utf-8')
            return func(kwargs)
        return request_result(206)  # payload 中没有需要的信息
    return _deco


def check_default_orga(func):
    def _deco(kwargs=dict()):
        try:
            if kwargs['orga_uuid'] == kwargs['uid']:
                return request_result(812)
        except Exception as msg:
            return request_result(100, ret=msg.message)
        return func(kwargs)
    return _deco


def check_orga_uuid_arg_is_orga_uuid(func):
    def _deco(kwargs=dict()):
        try:
            if kwargs['orga_uuid_arg'] != kwargs['orga_uuid']:
                return request_result(806)
        except Exception as msg:
            return request_result(100, ret=msg.message)
        return func(kwargs)
    return _deco

