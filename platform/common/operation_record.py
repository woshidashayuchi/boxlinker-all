# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import inspect
import uuid

from common.logs import logging as log
from common.code import request_result
from common.parameters import context_data
from common.security_rpcapi import SecurityRpcApi


security_rpcapi = SecurityRpcApi()


def operation_record(resource_type, action):

    def _retinfo(func):

        def __retinfo(*args, **kwargs):

            # security_rpcapi = SecurityRpcApi()

            record_uuid = str(uuid.uuid4())

            func_args = inspect.getcallargs(func, *args, **kwargs)
            token = func_args.get('token')
            source_ip = func_args.get('source_ip')
            resource_uuid = func_args.get('resource_uuid')
            resource_name = func_args.get('resource_name')

            if token is None:
                context = func_args.get('kwargs')
                token = context.get('token')
                source_ip = context.get('source_ip')
                resource_uuid = context.get('resource_uuid')
                resource_name = context.get('resource_name')

            context = context_data(token, "sec_sec_usr_com", "create")
            parameters = {
                             "record_uuid": record_uuid,
                             "source_ip": source_ip,
                             "resource_uuid": resource_uuid,
                             "resource_name": resource_name,
                             "resource_type": resource_type,
                             "action": action
                         }

            security_rpcapi.operation_create(context, parameters)

            try:
                result = func(*args, **kwargs)
            except Exception, e:
                log.error('function(%s) exec error, reason=%s'
                          % (func.__name__, e))
                result = request_result(601)

            context = context_data(token, "sec_sec_usr_com", "update")
            resource_uuid = result.get('result').get('resource_uuid')
            resource_name = result.get('result').get('resource_name')

            parameters = {
                             "record_uuid": record_uuid,
                             "return_code": result.get('status'),
                             "return_msg": result.get('msg'),
                             "resource_uuid": resource_uuid,
                             "resource_name": resource_name
                         }

            security_rpcapi.operation_update(context, parameters)

            return result

        return __retinfo

    return _retinfo
