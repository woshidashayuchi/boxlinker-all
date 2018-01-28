#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/10/19 10:12
"""

from flask import g

from authServer.models.hub_db_meta import OrgsBase


def org_name_exist(org_name):   # 组织名是否存在
    org_base = g.db_session.query(OrgsBase).filter(OrgsBase.org_name == org_name).first()
    if org_base is None:
        return False
    return True