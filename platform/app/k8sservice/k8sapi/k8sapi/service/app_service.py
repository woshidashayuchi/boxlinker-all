# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 17/4/10 下午6:26

import sys
p_path = sys.path[0] + '/../..'
p_path1 = sys.path[0] + '/..'
sys.path.append(p_path)
sys.path.append(p_path1)

from common.logs import logging as log
from time import sleep
from manager.check_manager import CheckManager


def check_server():

    manager = CheckManager()
    while True:
        try:
            manager.check_manager()
        except Exception, e:
            log.error('start the service check server error, reason is: %s' % e)

        sleep(3600)

if __name__ == '__main__':
    check_server()
