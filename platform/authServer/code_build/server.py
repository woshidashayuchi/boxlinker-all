#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import sys
p_path = sys.path[0] + '/..'
sys.path.append(p_path)

from time import sleep

from authServer.code_build.common.rabbitmq_server import RabbitmqServer
from authServer.conf.conf import queue_name, exchange_name


if __name__ == "__main__":

    while True:
        try:
            rbtmq = RabbitmqServer(600)

            # rbtmq.rpc_cast_server(queue_name)  # 单播模式
            rbtmq.broadcast_server(exchange_name)  # 广播模式

        except Exception, e:
            print e.message
            print 'ssss'
            #log.warning('RPC Server queue = %s running error, reason=%s' % (queue, e))
        sleep(10)

