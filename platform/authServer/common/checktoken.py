#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/10/21 11:12
"""
from flask import g
from authServer.conf.conf import GLOBALS_TOKEN
from authServer.pyTools.tools.codeString import request_result
from authServer.models.hub_db_meta import UserBase, AccessToken


# 由于相互引用导致,该函数需要单独放在一个文件中
def system_check_token(tokenid, token):
    """
    校验系统token
    """
    # 由于 in 在前可以保证 字典值判断时不会报错
    if tokenid in GLOBALS_TOKEN and GLOBALS_TOKEN[tokenid] == token:  # 此时系统token符合
        ret = request_result(0, ret={"msg": "token in service"})
        return ret

    if tokenid not in GLOBALS_TOKEN:

        ret = g.db_session.query(AccessToken).filter(AccessToken.token_uuid == tokenid, AccessToken.deleted == '0').first()
        if ret is not None and ret.token == token:
            ret = request_result(0, ret={"msg": "token in db"})
            GLOBALS_TOKEN[tokenid] = token
            return ret

    return request_result(202)
    # 当前系统没有该token, 需要去数据库中查找