#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/9/8 1:29
@数据库操作
"""

from flask import g
from authServer.models.hub_db_meta import GitHubOauth


def git_hub_oauth(uid):
    """ 用户的uid, 获取GitHubOauth数据"""
    ret = g.db_session.query(GitHubOauth).filter(GitHubOauth.uid == str(uid)).first()
    return ret
