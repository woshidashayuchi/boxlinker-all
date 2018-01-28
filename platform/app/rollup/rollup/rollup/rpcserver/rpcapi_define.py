# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/02/07

import sys
p_path = sys.path[0] + '/..'
sys.path.append(p_path)

from manager.roll_manager import RollManager


class KubernetesRpcAPI(object):

    def __init__(self):
        self.roll = RollManager()

    def service_create(self, context, parameters=None):

        return self.roll.roll_manager(context)
