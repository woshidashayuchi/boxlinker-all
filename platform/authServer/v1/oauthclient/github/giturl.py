#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/10/26 17:30
"""


from flask import g
import time
from authServer.pyTools.token.token import gen_token

import authServer.conf.openOauth as openOauth


def create_oauth_url(uid):
    """ 生成带有用户信息的url认证地址, state 码 """
    state_msg = {
        'uid': str(uid),     # 用户uid
        'expires': time.time() + 30 * 24 * 60 * 60
    }
    state_ret = gen_token(key=g.secret_key, data=state_msg)
    return openOauth.user_oauth_url.format(state_ret)