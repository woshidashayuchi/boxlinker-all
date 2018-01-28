# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/03/01
from driver.monitor_driver import MonitorDriver


class MonitorManager(object):

    def __init__(self):
        self.monitor_driver = MonitorDriver()

    def monitor_message_manager(self, parameters):
        return self.monitor_driver.get_monitor_message(parameters)
