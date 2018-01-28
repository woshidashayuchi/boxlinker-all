# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 17/5/18 下午2:24
import sys
p_path = sys.path[0] + '/../..'
p_path1 = sys.path[0] + '/..'
sys.path.insert(1, p_path)
sys.path.append(p_path1)
from common.logs import logging as log
from manager.device_manager import DeviceManager
from time import sleep


def alarm_server(alarm):
    device_manager = DeviceManager()
    while True:
        try:
            device_manager.cpu_data_to_db()
        except Exception, e:
            log.error('start the service of %s error, reason is: %s' % (alarm, e))

        sleep(3600)

if __name__ == '__main__':
    alarm_server('device')
