# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/02/06

import json
from flask import request
from common.logs import logging as log
from common.code import request_result
from flask_restful import Resource
from rpcapi.rpc_client import KubernetesRpcClient


class RollClientApi(Resource):
    def __init__(self):
        self.kuber = KubernetesRpcClient()

    def post(self):

        try:
            context = json.loads(request.get_data())
            log.info('parameters body is: %s' % context)
        except Exception, e:
            log.error("parameters error,reason=%s" % e)
            return json.dumps(request_result(101))
        ret = self.kuber.create_services(context)

        return json.dumps(ret)
