#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/10/20 15:20
"""


import time
from flask import g

from authServer.models.hub_db_meta import UserBase, AccessToken, OrgsUser

import authServer.pyTools.token.token as TK
from authServer.conf.conf import TOKEN_TIMEOUT, GLOBALS_TOKEN, CONFIRM_EMAIL
from authServer.tools.db_check import is_email

from authServer.pyTools.tools.codeString import request_result

from authServer.common.decorate import request_form_get_tokenid_token, get_token_from_headers
from authServer.common.role import OrgaRole



def get_login_token(username, isuuid=False):
    """ 得到token 用户名/也可能是邮箱 """

    if isuuid:
        userBase = g.db_session.query(UserBase).filter(UserBase.user_id == username).first()
    elif isuuid is False and is_email(username):
        userBase = g.db_session.query(UserBase).filter(UserBase.email == username).first()
    else:
        userBase = g.db_session.query(UserBase).filter(UserBase.username == username).first()

    if userBase is None:
        return request_result(701)

    if CONFIRM_EMAIL and 0 == userBase.is_active:
        return request_result(715, ret='is_active is 0')

    orga = g.db_session.query(OrgsUser).filter(
        OrgsUser.org_id == userBase.user_id, OrgsUser.uid == userBase.user_id).first()

    if orga is None:
        return request_result(100, "no default orga")


    if str(userBase.sysadmin_flag) == '1':
        role_mode = OrgaRole.SystemGod.value
    else:
        role_mode = orga.role

    retdict = GenerateToken(
        user_uuid=userBase.user_id, user_name=userBase.username, email=userBase.email,
        # role_uuid=OrgaRole.OrgaMaster.value,
        role_uuid=role_mode,
        user_orga=userBase.username, orga_uuid=userBase.user_id
    )
    # 对于个人账号  组织id == user.id

    if retdict['status'] != 0:
        return retdict

    try:
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        new_user_profile = AccessToken(
            token=retdict['result']['token'],
            token_uuid=retdict['result']['tokenid'],
            user_id=userBase.user_id,
            user_name= userBase.username,
            org_id=userBase.user_id,
            org_name=userBase.username,  # 个人账号登录
            create_time=now,
            update_time=now,
            expiration=TOKEN_TIMEOUT,  # 过期时间
            deleted='0',
            role_uuid=role_mode,
        )
        g.db_session.add(new_user_profile)
        g.db_session.commit()
    except Exception as msg:
        print msg.message
        retdict = request_result(401, ret={"msg": "get_token insert db is error"})
    finally:
        return retdict


def get_access_token(user_name, email, uid, user_role, user_orag, orga_uuid):
    retdict = GenerateToken(user_uuid=uid, user_name=user_name, email=email,
                            role_uuid=user_role, user_orga=user_orag,
                            orga_uuid=orga_uuid)
    if retdict['status'] != 0:
        return retdict

    try:
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        new_user_profile = AccessToken(
            user_id=uid,
            user_name=user_name,
            org_id=orga_uuid,
            org_name=user_orag,
            token=retdict['result']['token'],
            token_uuid=retdict['result']['tokenid'],
            create_time=now,
            update_time=now,
            expiration=TOKEN_TIMEOUT,
            deleted='0',
            role_uuid=user_role,
        )
        g.db_session.add(new_user_profile)
        g.db_session.commit()
    except Exception as msg:
        retdict = request_result(401, ret={"msg": "get_token insert db is error"})
    finally:
        return retdict




@request_form_get_tokenid_token
def log_out(tokenid, token):
    try:
        GLOBALS_TOKEN.pop(tokenid, None)

        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        g.db_session.query(AccessToken).filter(AccessToken.token_uuid == tokenid).update(
            {"deleted": '1', "update_time": now})
        g.db_session.commit()

        ret = request_result(0)
    except Exception as msg:
        ret = request_result(403, ret={"msg": msg.message})
    finally:
        return ret


@get_token_from_headers
def clear_token(token):
    try:
        visit_tokens = g.db_session.query(AccessToken).filter(AccessToken.token == token).all()

        for visit_t in visit_tokens:
            tokenid = visit_t.tokenid
            GLOBALS_TOKEN.pop(tokenid, None)

            now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            g.db_session.query(AccessToken).filter(AccessToken.token_uuid == tokenid).update(
                {"deleted": '1', "update_time": now})
            g.db_session.commit()

        ret = request_result(0)
    except Exception as msg:
        ret = request_result(403, ret={"msg": msg.message})
    finally:
        return ret

import json
from authServer.common.checktoken import system_check_token
from authServer.pyTools.token.token import get_payload

#严重token
@get_token_from_headers
def check_token_head_token(token):
    ret = get_payload(token=token)
    if ret['status'] != 0:
        return ret
    payload = ret['result']['payload']
    tokenid = json.loads(payload)['tokenid']

    print 'check_token_head_token'
    print token
    return system_check_token(tokenid, token)


def GenerateToken(*args, **kwargs):
    """
    retdict = GenerateToken(username=ret.username, email=ret.email)
    登录时第一次获取token, 不需要tokenid; 只有刷新token是才获取
    """
    if 'user_name' not in kwargs:
        return request_result(707)

    if 'email' not in kwargs:
        return request_result(708)

    if 'user_uuid' not in kwargs:
        return request_result(709)
    else:
        kwargs['uid'] = kwargs['user_uuid']  # 暂时保留  uid

    if 'role_uuid' not in kwargs:
        return request_result(706, ret='GenerateToken no user_role')



    if 'user_orga' not in kwargs:
        return request_result(706, ret='GenerateToken no user_orga')
    else:
        kwargs['user_orag'] = kwargs['user_orga']  # 无效字段, 暂时保留,后期删除


    if 'orga_uuid' not in kwargs:
        return request_result(706, ret='GenerateToken no orga_uuid')

    if 'tokenid' not in kwargs:
        tokenid = TK.GenerateRandomString(randlen=24)
        kwargs['tokenid'] = tokenid
    else:
        tokenid = kwargs['tokenid']

    kwargs['salt'] = TK.GenerateRandomString(randlen=24)


    token = TK.gen_token(key=g.secret_key, data=kwargs, timeout=TOKEN_TIMEOUT)
    GLOBALS_TOKEN[tokenid] = token

    return request_result(0, ret={'token': token, 'tokenid': tokenid})




def token_authentication(func):
    """ 验证 token """
    def _deco(token):
        ret = get_payload(token=token)  # token  合法
        if ret['status'] != 0:
            return ret

        payload = ret['result']['payload']
        tokenid = json.loads(payload)['tokenid']

        rret = system_check_token(token=token, tokenid=tokenid)

        if ret['status'] != 0:
            return ret

        return func(payload=payload)
    return _deco


@request_form_get_tokenid_token
def check_token(tokenid, token):
    return system_check_token(tokenid, token)



