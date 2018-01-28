#! /usr/bin python
# -*- coding:utf8 -*-
# Date:2016/12/27
# Author:wang-xf

import sys
p_path = sys.path[0] + '/..'
sys.path.append(p_path)
from data import DataOrm
from common.logs import logging as log
from data_controller import LogicModel


def get_uuid(json_list):

    uid_font = ""

    try:
        get_sql = DataOrm.get_uid_font(json_list)
    except Exception, e:
        log.error("get the uid sql create error,reason=%s" % e)

    logicmodel = LogicModel()
    conn, cur = logicmodel.connection()

    try:
        resu = logicmodel.exeQuery(cur, get_sql)
        for i in resu:
            uid_font = i.get("uid_font")
    except Exception, e:
        log.error("exec the sql for uuid error, reason=%s" % e)

    logicmodel.connClose(conn, cur)

    return uid_font
