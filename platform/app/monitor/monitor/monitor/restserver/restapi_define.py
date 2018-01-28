# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/03/01

import json
from flask import request
from common.logs import logging as log
from common.code import request_result
from common.parameters import context_data
from common.token_ucenterauth import token_auth
from rpcapi.rpc_client import MonitorRpcClient

from manager.monitor_manager import MonitorManager


class MonitorClientApi(object):
    def __init__(self):
        pass

    broad = MonitorRpcClient()
    monitor = MonitorManager()

    @classmethod
    def monitor_for(cls, pod_name, rtype):

        try:
            token = request.headers.get('token')
            token_ret = token_auth(token)
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return json.dumps(request_result(201))

        parameters = dict()
        try:
            parameters['time_long'] = request.values.get('time_long', '15m')
            parameters['time_span'] = request.values.get('time_span', '1m')
            parameters['pod_name'] = pod_name
            parameters['type'] = rtype
            parameters.update(token_ret.get('result'))
        except Exception, e:
            log.error("parameters error,reason=%s" % e)
            return json.dumps(request_result(101))

        # context = context_data(token, "service_create", "create")

        # ret = cls.broad.monitor_message_get(parameters)

        ret = cls.monitor.monitor_message_manager(parameters)

        return json.dumps(ret)

    @classmethod
    def broad_for(cls):
        try:
            token = request.headers.get('token')
            token_ret = token_auth(token)
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return json.dumps(request_result(201))

        ret = cls.broad.broad_message_get(token_ret.get('result'))

        return json.dumps(ret)
