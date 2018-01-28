#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/10/21 15:59
"""
import json
import os
from flask import g


from authServer.common.decorate import get_token_from_headers_check
from authServer.models.hub_db_meta import UserBase, GitHubOauth

from authServer.pyTools.tools.codeString import request_result


@get_token_from_headers_check
def get_user_info(payload):
    """ 获取用户信息 """
    try:
        payload = json.loads(payload)
        print payload
        print type(payload)

        if payload['user_orga'] == payload['user_name']:
            payload['is_user'] = '1'
        else:
            payload['is_user'] = '0'
    except Exception as msg:
        return request_result(100, ret=msg.message)

    try:
        user_base = g.db_session.query(UserBase).filter(UserBase.user_id == payload['user_uuid']).first()
        if user_base is None:
            return request_result(701)

        from authServer.conf.conf import OssHost

        if user_base.logo is None or user_base.logo == '':
            payload['logo'] = OssHost + os.sep + 'repository/default.png'
        else:
            payload['logo'] = OssHost + os.sep + user_base.logo

    except Exception as msg:
        print msg.args
        print msg.message
        return request_result(100, ret=msg.message)


    try:

        print "payload['user_uuid']"
        print payload['user_uuid']

        githuboauths = g.db_session.query(GitHubOauth).filter(GitHubOauth.uid == payload['user_uuid']).all()

        oauth = dict()
        oauth['coding'] = 0
        oauth['github'] = 0
        for githuboauth in githuboauths:
            if githuboauth.src_type == 'coding':
                oauth['coding'] = 1
                oauth['codingname'] = githuboauth.git_name
            elif githuboauth.src_type == 'github':
                oauth['github'] = 1
                oauth['gitname'] = githuboauth.git_name
            else:
                print 'ss'
        payload['oauth'] = oauth

    except Exception as msg:
        print msg.args
        print msg.message
        return request_result(100, ret=msg.message)

    ret = request_result(0, ret=payload)
    return ret




@get_token_from_headers_check
def get_user_base_info(payload):
    """ 获取用户信息 """
    try:
        payload = json.loads(payload)
        print payload
        print type(payload)

        if payload['user_orga'] == payload['user_name']:
            payload['is_user'] = '1'
        else:
            payload['is_user'] = '0'
    except Exception as msg:
        return request_result(100, ret=msg.message)


    user_base = dict()
    user_base['user_uuid'] = payload['user_uuid']
    user_base['orga_uuid'] = payload['orga_uuid']
    user_base['role_uuid'] = payload['role_uuid']
    user_base['user_orga'] = payload['user_orga']
    user_base['user_name'] = payload['user_name']
    user_base['is_user'] = payload['is_user']






    ret = request_result(0, ret=user_base)
    return ret