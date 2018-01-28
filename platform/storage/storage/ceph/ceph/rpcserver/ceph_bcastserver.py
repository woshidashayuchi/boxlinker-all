#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import sys
from time import sleep
from multiprocessing import Pool

p_path = sys.path[0] + '/../..'
sys.path.insert(1, p_path)

import rpcapi_register

from conf import conf
from common.logs import logging as log
from common.rabbitmq_server import RabbitmqServer

reload(sys)
sys.setdefaultencoding('utf8')


def server_start(n):

    exchange_name = conf.ceph_exchange_name

    while True:

        try:
            log.critical('Starting RPC Bcast API Server, exchange=%s'
                         % (exchange_name))
            rbtmq = RabbitmqServer(60)
            rbtmq.broadcast_server(exchange_name, rpcapi_register)
        except Exception, e:
            log.error('RPC Bcast API Server running error, '
                      'exchange=%s, reason=%s'
                      % (exchange_name, e))
        sleep(10)


def service_start(workers=1):

    pool = Pool(workers)
    pool.map(server_start, range(workers))


if __name__ == "__main__":

    service_start()
