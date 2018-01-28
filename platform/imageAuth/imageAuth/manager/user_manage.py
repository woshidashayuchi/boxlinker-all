#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 17/2/10 16:07
"""

import json

from common.code import request_result
from common.logs import logging as log
from common.json_encode import CJsonEncoder


import imageAuth.manager.userTools as UserTools

from common.local_cache import LocalCache

import time
from pyTools.token.token import get_md5

caches = LocalCache(100)
class UcenterManager(object):
    def __init__(self):
        log.info('UcenterManager __init__')

    # 获取一个用户下对应组织的token
    def username_password_authentication(self, user_name, password):
        md1 = get_md5(user_name)
        md2 = get_md5(password)

        key = md1 + md2

        tokeninfo = caches.get(key=key)
        if tokeninfo != caches.notFound:
            log.info('username_password_authentication get caches token : %s' % (tokeninfo['token']))
            return True, tokeninfo['token']

        retbool, token = UserTools.username_password_authentication(username=user_name, password=password)
        if retbool is False:
            return False, None

        log.info('get username_password_authentication token : %s' % (token))

        expire = int(time.time()) + 300
        caches.set(key=key, value={"token": token, "expire": expire})
        return True, token


    def username_password_teams_token(self, user_name, password, team_name):
        """ 获取一个用户对应组织的token """
        md1 = get_md5(user_name)
        md2 = get_md5(password)
        md3 = get_md5(team_name)
        key = md1 + md2 + md3

        tokeninfo = caches.get(key=key)
        if tokeninfo != caches.notFound:
            log.info('username_password_teams_token get caches token : %s' % (tokeninfo['token']))
            return True, tokeninfo['token']

        retbool, token = UserTools.username_password_teams_token(username=user_name, password=password, team_name=team_name)
        if retbool is False:
            return False, None

        log.info('get username_password_authentication token : %s' % (token))

        expire = int(time.time()) + 300
        caches.set(key=key, value={"token": token, "expire": expire})
        return True, token

    def get_team_uuid(self, token, team_name):
        md1 = get_md5(token)
        md2 = get_md5(team_name)
        key = md1 + md2

        tokeninfo = caches.get(key=key)
        if tokeninfo != caches.notFound:
            log.info('get_team_uuid get caches team_info: %s' % (tokeninfo['team_info']))
            return True, tokeninfo['team_info']

        retbool, team_info = UserTools.get_team_uuid(token=token, team_name=team_name)
        if retbool is False:
            return False, None

        log.info('get username_password_authentication team_info : %s' % (team_info))

        expire = int(time.time()) + 300
        caches.set(key=key, value={"team_info": team_info, "expire": expire})
        return True, team_info





if __name__ == '__main__':
    uc = UcenterManager()

    for i in xrange(3):
        print i
        uc.username_password_teams_token(user_name='liuzhangpei', password='QAZwsx123', team_name='liuzhangpei')








