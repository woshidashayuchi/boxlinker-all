# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/02/06
import sys
p_path = sys.path[0] + '/../..'
p_path1 = sys.path[0] + '/..'
sys.path.append(p_path)
sys.path.append(p_path1)
from common.logs import logging as log
from time import sleep
from restapi_register1 import rest_app_run


def server_start(service_name):

    while True:
        try:
            log.info('Starting %s Restful API Server' % (service_name))
            rest_app_run()
        except Exception, e:
            log.warning('%s RESTful API Server running error, reason=%s'
                        % (service_name, e))
        sleep(10)


if __name__ == "__main__":

    server_start('roll_update')
