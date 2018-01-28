# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/03/02
from driver.broad_driver import BroadDriver


class BroadManager(object):

    def __init__(self):
        self.broad_driver = BroadDriver()

    def broad_message_manager(self, parameters):
        return self.broad_driver.get_broad_message(parameters)