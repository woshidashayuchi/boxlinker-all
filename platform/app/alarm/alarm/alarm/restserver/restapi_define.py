# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 17/4/14 上午11:02

from common.logs import logging as log
from flask import request
from flask_restful import Resource
from common.token_ucenterauth import token_auth
from common.code import request_result
from common.parameters import context_data
from rpcapi.rpc_client import AlarmRpcClient
import json


class RestApiDefine(Resource):
    def __init__(self):
        self.alarm = AlarmRpcClient()

    # def post(self):
    #     try:
    #         token = request.headers.get('token')
    #         token_ret = token_auth(token)
    #     except Exception, e:
    #         log.error('Token check error, reason=%s' % e)
    #         return request_result(201)
    #     try:
    #         parameters = json.loads(request.get_data())
    #         parameters.update(token_ret.get('result'))
    #     except Exception, e:
    #         log.error('explain the parameters error, reason is: %s' % e)
    #         return request_result(101)
    #
    #     context = context_data(token, "service_create", "create")
    #     ret = self.alarm.create_service_alarm(context, parameters)
    #
    #     return ret

    # 获取与某个service绑定的alarm的详细信息
    # def get(self, alarm_uuid):
    #     try:
    #         token = request.headers.get('token')
    #         token_ret = token_auth(token)
    #     except Exception, e:
    #         log.error('Token check error, reason=%s' % e)
    #         return request_result(201)
    #
    #     context = context_data(token, "alarm_list", "read")
    #     parameters = token_ret.get('result')
    #     parameters['alarm_uuid'] = alarm_uuid
    #     ret = self.alarm.query_alarm(context, parameters)
    #
    #     return ret

    def post(self, alarm_uuid):
        try:
            token = request.headers.get('token')
            token_ret = token_auth(token)
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return request_result(201)

        parameters = token_ret.get('result')
        try:
            parameters.update(json.loads(request.get_data()))
            parameters['alarm_uuid'] = alarm_uuid
        except Exception, e:
            log.error('parameters error, reason is: %s' % e)
            return request_result(101)

        context = context_data(token, alarm_uuid, "update")
        ret = self.alarm.create_service_alarm(context, parameters)

        return ret

    # 解绑service与alarm的关系
    def delete(self, alarm_uuid):
        try:
            token = request.headers.get('token')
            token_ret = token_auth(token)
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return request_result(201)
        parameters = token_ret.get('result')

        try:
            parameters['alarm_uuid'] = alarm_uuid

            # 参数形式: {"service_uuid": ["",""]}
            parameters.update(json.loads(request.get_data()))
        except Exception, e:
            log.error('parameters error, reason is: %s' % e)
            return request_result(101)

        context = context_data(token, alarm_uuid, "update")
        ret = self.alarm.delete_alarm_svc(context, parameters)

        return ret

    # 更改service与alarm的绑定关系
    # 即修改service对应的alarm规则
    def put(self, alarm_uuid):
        try:
            token = request.headers.get('token')
            token_ret = token_auth(token)
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return request_result(201)
        parameters = token_ret.get('result')
        try:
            parameters['alarm_uuid'] = alarm_uuid

            # 参数形式: {"service_uuid": ""}
            parameters.update(json.loads(request.get_data()))
        except Exception, e:
            log.error('parameters error, reason is: %s' % e)
            return request_result(101)

        context = context_data(token, alarm_uuid, "update")
        ret = self.alarm.update_service_alarm(context, parameters)

        return ret


class UpApiDefine(Resource):
    def __init__(self):
        self.alarm = AlarmRpcClient()

    def get(self, alarm_uuid):
        try:
            token = request.headers.get('token')
            token_ret = token_auth(token)
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return request_result(201)

        parameters = {'alarm_uuid': alarm_uuid}
        parameters.update(token_ret.get('result'))
        context = context_data(token, alarm_uuid, "read")
        ret = self.alarm.only_detail_alarm(context, parameters)

        return ret

    def put(self, alarm_uuid):
        log.info('111111111----')
        try:
            token = request.headers.get('token')
            token_ret = token_auth(token)
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return request_result(201)
        try:
            parameters = json.loads(request.get_data())
            parameters['alarm_uuid'] = alarm_uuid
            parameters.update(token_ret.get('result'))
        except Exception, e:
            log.error('parameters explain error, reason is: %s' % e)
            return request_result(101)

        context = context_data(token, alarm_uuid, "update")
        ret = self.alarm.only_update_alarm(context, parameters)

        return ret

    def delete(self, alarm_uuid):
        try:
            token = request.headers.get('token')
            token_ret = token_auth(token)
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return request_result(201)

        parameters = token_ret.get('result')
        parameters['alarm_uuid'] = alarm_uuid
        context = context_data(token, alarm_uuid, 'delete')

        ret = self.alarm.only_delete_alarm(context, parameters)

        return ret


class AlarmApiDefine(Resource):
    def __init__(self):
        self.alarm = AlarmRpcClient()

    def post(self):
        try:
            token = request.headers.get('token')
            token_ret = token_auth(token)
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return request_result(201)

        try:
            parameters = json.loads(request.get_data())
            parameters.update(token_ret.get('result'))
        except Exception, e:
            log.error('explain the parameters error, reason is: %s' % e)
            return request_result(101)

        context = context_data(token, "alarm_create", "create")
        ret = self.alarm.create_alarm(context, parameters)

        return ret

    def get(self):
        try:
            token = request.headers.get('token')
            token_ret = token_auth(token)
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return request_result(201)

        parameters = token_ret.get('result')
        context = context_data(token, "alarm_list", "read")

        ret = self.alarm.only_query_alarm(context, parameters)
        return ret

    def delete(self):
        pass


class AdminResourceDefine(Resource):

    def __init__(self):
        pass

    def get(self):
        try:
            token = request.headers.get('token')
            token_ret = token_auth(token)
            log.info('admin token check result is: %s' % token_ret)
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return request_result(201)
