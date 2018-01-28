# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/02/06

import json
import base64
from flask import request
from flask_restful import Resource
from common.logs import logging as log
from common.code import request_result
from common.time_log import time_log
from common.parameters import context_data
from common.token_ucenterauth import token_auth
from rpcapi.rpc_client import KubernetesRpcClient
from rpcapi.rpc_client import CertifyRpcClient
from rpcapi.rpc_client import AdminServiceRpcClient


class ServicesApi(Resource):
    def __init__(self):
        self.kubernetes = KubernetesRpcClient()

    @time_log
    def post(self):

        try:
            token = request.headers.get('token')
            token_ret = token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return request_result(201)

        try:
            parameters = json.loads(request.get_data())
            log.info('parameters body is: %s' % parameters)
            parameters['token'] = token
            token_rets = token_ret.get('result')
            if 'service_name' in token_rets.keys():
                del token_rets['service_name']
            parameters.update(token_rets)
            log.info('parameters body(1) is:%s' % parameters)
            if parameters.get('service_name') is None:
                return request_result(101)
        except Exception, e:
            log.error("parameters error,reason=%s" % e)
            return request_result(101)

        context = context_data(token, "service_create", "create", source_ip)

        ret = self.kubernetes.create_services(context, parameters)

        return ret

    @time_log
    def get(self):

        try:
            token = request.headers.get('token')
            token_ret = token_auth(token)
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return request_result(201)

        parameters = token_ret.get('result')
        parameters['service_name'] = request.args.get('service_name',)
        parameters['page_size'] = request.args.get('page_size')
        parameters['page_num'] = request.args.get('page_num')

        context = context_data(token, "service_list", "read")

        ret = self.kubernetes.query_service(context, parameters)

        return ret


class ServiceApi(Resource):
    def __init__(self):
        self.kuber = KubernetesRpcClient()

    @time_log
    def get(self, service_uuid):
        try:
            token = request.headers.get('token')
            token_ret = token_auth(token)
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return request_result(201)

        if request.args.get('pod') == 'pod':
            parameters = token_ret.get('result')
            parameters['service_uuid'] = service_uuid
            parameters['rtype'] = 'pods_msg'

            context = context_data(token, service_uuid, "read")

            try:
                ret = self.kuber.pod_msg(context, parameters)
            except Exception, e:
                log.error('get the pods messages error, reason=%s' % e)
                return request_result(504)
            return request_result(0, ret)

        parameters = token_ret.get('result')
        parameters['service_uuid'] = service_uuid

        context = context_data(token, service_uuid, "read")

        ret = self.kuber.detail_service(context, parameters)

        return ret

    @time_log
    def delete(self, service_uuid):
        try:
            token = request.headers.get('token')
            token_ret = token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.error('Token check error,reason=%s' % e)
            return request_result(201)

        parameters = token_ret.get('result')
        parameters['token'] = token
        parameters['service_uuid'] = service_uuid

        context = context_data(token, service_uuid, 'delete', source_ip)

        ret = self.kuber.delete_service(context, parameters)

        return ret

    @time_log
    def put(self, service_uuid):
        try:
            token = request.headers.get('token')
            token_ret = token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.error('Token check error,reason=%s' % e)
            return request_result(201)

        parameters = token_ret.get('result')
        rtype = request.args.get('rtype',)
        parameters['rtype'] = rtype
        parameters['service_uuid'] = service_uuid
        parameters['token'] = token

        try:
            in_data = json.loads(request.get_data())
            if not in_data and rtype == 'container':
                return request_result(101)
            parameters.update(in_data)
        except Exception, e:
            log.error('parameters error, reason is: %s' % e)
            return request_result(101)

        context = context_data(token, service_uuid, "update", source_ip)

        ret = self.kuber.update_service(context, parameters)
        return ret


class ServiceName(Resource):
    def __init__(self):
        self.kuber = KubernetesRpcClient()

    @time_log
    def get(self, service_name):
        try:
            token = request.headers.get('token')
            token_ret = token_auth(token)
        except Exception, e:
            log.error('Token check error,reason=%s' % e)
            return request_result(201)
        rtype = request.args.get('rtype')

        context = token_ret.get('result')
        if rtype == 'service':
            context['service_name'] = service_name
        elif rtype == 'domain':
            context['domain'] = service_name
        else:
            return request_result(101)

        context['rtype'] = rtype
        ret = self.kuber.service_name_get(context)

        return ret


class Certify(Resource):
    def __init__(self):
        self.certify = CertifyRpcClient()

    def post(self):
        try:
            token = request.headers.get('token')
            token_ret = token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return request_result(201)

        try:
            # 暂时数据上传格式:tls.crt在前, 中间关键字',tls.key:',最后key内容
            data = request.get_data().split(',tls.key:')
            crt = data[0]
            key = data[1]
            base64.b64encode(crt)
            base64.b64encode(key)
            parameters = {'content': {'tls.crt': crt,
                                      'tls.key': key}
                          }

            parameters['token'] = token
            token_rets = token_ret.get('result')
            parameters.update(token_rets)
        except Exception, e:
            log.error('parameters error, reason is: %s' % e)
            return request_result(101)

        context = context_data(token, "certify_create", "create", source_ip)

        ret = self.certify.create_certify(context, parameters)

        return ret

    def get(self):
        try:
            token = request.headers.get('token')
            token_ret = token_auth(token)
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return request_result(201)

        parameters = token_ret.get('result')
        context = context_data(token, "certify_list", "read")
        ret = self.certify.query_certify(context, parameters)

        return ret


class CertifyUp(Resource):
    def __init__(self):
        self.certify = CertifyRpcClient()

    def put(self, certify_uuid):
        try:
            token = request.headers.get('token')
            token_ret = token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return request_result(201)
        try:
            data = request.get_data().split(',tls.key:')
            crt = data[0]
            key = data[1]
            parameters = {'content': {'tls.crt': crt,
                                      'tls.key': key}
                          }

            parameters.update(token_ret.get('result'))
            parameters['certify_uuid'] = certify_uuid
        except Exception, e:
            log.error('parameters explain error, reason is: %s' % e)
            return request_result(101)

        context = context_data(token, certify_uuid, "update", source_ip)

        ret = self.certify.update_certify(context, parameters)

        return ret


class AdminService(Resource):
    def __init__(self):
        self.admin_service = AdminServiceRpcClient()

    def get(self):
        try:
            token = request.headers.get('token')
            token_ret = token_auth(token)
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return request_result(201)

        context = context_data(token, "service_list", "read")

        try:
            ret = self.admin_service.get_all_services(context, token_ret)
        except Exception, e:
            log.error('error, reason is: %s' % e)
            return request_result(601)

        return ret
