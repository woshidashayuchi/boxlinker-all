#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import sys
p_path = sys.path[0] + '/../..'
sys.path.insert(1, p_path)

from time import sleep

from common.logs import logging as log
from appstatus.manager.appstatus_manager import AppStatusManager


def appstatus_service():

    appstatus = AppStatusManager()

    rc_status_cache = {}

    while True:
        try:
            log.debug('rc_status_cache=%s' % (rc_status_cache))
            rc_status_cache = appstatus.rc_status_update(rc_status_cache)
        except Exception, e:
            rc_status_cache = {}
            log.warning('Appstatus Service running error, reason=%s'
                        % e)
        sleep(15)


if __name__ == "__main__":

    appstatus_service()
