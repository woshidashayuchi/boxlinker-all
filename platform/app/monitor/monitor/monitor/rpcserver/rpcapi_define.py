# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/02/07

import sys
p_path = sys.path[0] + '/..'
sys.path.append(p_path)
from common.logs import logging as log
from manager.monitor_manager import MonitorManager
from manager.broad_manager import BroadManager


class MonitorRpcAPI(object):

    def __init__(self):
        self.monitor_manager = MonitorManager()
        self.broad_manager = BroadManager()

    def monitor_get(self, context, parameters=None):
        return self.monitor_manager.monitor_message_manager(context)

    def broad_get(self, context, parameters=None):
        return self.broad_manager.broad_message_manager(context)
