# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/02/06

import json
from flask import request
from flask_restful import Resource
from common.logs import logging as log
from common.code import request_result
from common.parameters import context_data
from common.token_ucenterauth import token_auth
from rpcapi.rpc_client import KubernetesRpcClient


class RestApiDefine(Resource):
    def __init__(self):
        self.kuber = KubernetesRpcClient()

    def post(self):
        try:
            token = request.headers.get('token')
            token_ret = token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return json.dumps(request_result(201))

        try:
            parameters = json.loads(request.get_data())
            parameters.update(token_ret.get('result'))
            parameters['token'] = token
        except Exception, e:
            log.error('explain the parameters error, reason is: %s' % e)
            return json.dumps(request_result(101))

        context = context_data(token, "service_create", "create", source_ip)
        ret = self.kuber.create_services(context, parameters)

        return ret

    def get(self):
        parameters = dict()
        try:
            token = request.headers.get('token')
            token_ret = token_auth(token)
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return json.dumps(request_result(201))

        token_rets = token_ret.get('result')
        parameters.update(token_rets)
        parameters['page_size'] = request.args.get('page_size')
        parameters['page_num'] = request.args.get('page_num')

        context = context_data(token, "service_list", "read")
        ret = self.kuber.query_service(context, parameters)

        return ret

    def delete(self):
        try:
            token = request.headers.get('token')
            token_ret = token_auth(token)
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return json.dumps(request_result(201))
        try:
            datas = json.loads(request.get_data())
            service_uuids = datas.get('service_uuid')
        except Exception, e:
            log.error('parameters error, reason is: %s' % e)
            return request_result(101)

        ret = {}
        for i in service_uuids:
            parameters = i
            context = context_data(token, i, 'delete')
            try:
                ret = self.kuber.delete_service(context, parameters)
            except Exception, e:
                log.error('get error, reason is: %s' % e)
                return request_result(402)

        return ret
