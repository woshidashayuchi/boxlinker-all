#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 17/2/6 17:02
"""


import time

from common.logs import logging as log
from common.code import request_result
from common.local_cache import LocalCache
from common.parameters import rpc_data
from common.rabbitmq_client import RabbitmqClient

from conf.conf import queue, github_queue

caches = LocalCache(1000)

class ImageRepoClient(object):

    def __init__(self):
        self.rbtmq = RabbitmqClient()
        self.queue = queue
        self.timeout = 60

    # 所用的都调用该接口
    def RunImageRepoClient(self, api, context, parameters=None):
        """
        :param api: 对应rpc服务的接口名,不能为空
        :param context:
        :param parameters:
        :return:
        """
        try:
            rpc_body = rpc_data(api, context, parameters)
            return self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)


class GithubOauthClient(object):
    def __init__(self):
        self.rbtmq = RabbitmqClient()
        self.queue = github_queue
        self.timeout = 60
    # 所用的都调用该接口
    def RunImageRepoClient(self, api, context, parameters=None):
        """
        :param api: 对应rpc服务的接口名,不能为空
        :param context:
        :param parameters:
        :return:
        """
        try:
            rpc_body = rpc_data(api, context, parameters)
            return self.rbtmq.rpc_call_client(self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)