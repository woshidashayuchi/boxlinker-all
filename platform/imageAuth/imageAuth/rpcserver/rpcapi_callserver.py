#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 17/2/7 10:22
"""

import sys
from time import sleep
from multiprocessing import Pool

import rpcapi_register

from common.logs import logging as log
from common.rabbitmq_server import RabbitmqServer

from conf.conf import queue
#


def server_start(n):

    while True:
        try:
            log.info('Starting RPC Call API Server, topic=%s' % queue)
            rbtmq = RabbitmqServer(60)
            rbtmq.rpc_call_server(queue, rpcapi_register)
        except Exception, e:
            log.warning('RPC Call API Server running error, queue=%s, reason=%s' % (queue, e))
        sleep(10)


def service_start(workers=1):
    pool = Pool(workers)
    pool.map(server_start, range(workers))

if __name__ == '__main__':
    # service_start()
    server_start(10)
    log.error('rpcapi_callserver is exit')
