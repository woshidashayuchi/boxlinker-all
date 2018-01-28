# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/02/27

from alarm_db import AlarmDB
from common.logs import logging as log


class DataInit(object):
    service_db = AlarmDB()
    try:
        ret = service_db.init_insert()
    except Exception, e:
        log.error('init alarm api(insert into database) error, reason=%s' % e)
