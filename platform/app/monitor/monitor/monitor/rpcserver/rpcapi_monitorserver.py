# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/02/07

import sys
from time import sleep
from multiprocessing import Pool

p_path = sys.path[0] + '/../..'
sys.path.insert(1, p_path)

import rpcapi_register

from conf import conf
from common.logs import logging as log
from common.rabbitmq_server import RabbitmqServer


def server_start(n):

    queue = 'monitorcall_monitor'

    while True:

        try:
            log.info('Starting RPC Call API Server, topic=%s' % queue)

            rbtmq = RabbitmqServer(60)
            rbtmq.rpc_call_server(queue, rpcapi_register)

        except Exception, e:
            log.error('RPC Call API Server running error, queue=%s, reason=%s' % (queue, e))

        sleep(10)


def service_start(workers=4):

    pool = Pool(workers)
    pool.map(server_start, range(workers))


if __name__ == "__main__":

    service_start()

