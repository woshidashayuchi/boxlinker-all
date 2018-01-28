# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import json
import time

from conf import conf
from common.logs import logging as log
from common.code import request_result
from common.json_encode import CJsonEncoder
from common.limit import limit_check

from security.db import security_db


class OperationManager(object):

    def __init__(self):

        self.security_db = security_db.SecurityDB()

    def operation_create(self, record_uuid, user_uuid,
                         user_name, source_ip, resource_uuid,
                         resource_name, resource_type, action):

        try:
            self.security_db.operation_create(
                 record_uuid, user_uuid, user_name, source_ip,
                 resource_uuid, resource_name, resource_type,
                 action)
        except Exception, e:
            log.error('Database insert error, reason=%s' % (e))
            return request_result(401)

        return request_result(0)

    def operation_list(self, start_time, end_time,
                       page_size, page_num):

        try:
            start_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                       time.localtime(float(start_time)))
            end_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                     time.localtime(float(end_time)))
            operations_list_info = self.security_db.operation_list(
                                        start_time, end_time,
                                        page_size, page_num)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        records_list = operations_list_info.get('operations_list')
        count = operations_list_info.get('count')

        operations_list = []
        for record_info in records_list:
            user_uuid = record_info[0]
            user_name = record_info[1]
            source_ip = record_info[2]
            resource_uuid = record_info[3]
            resource_name = record_info[4]
            resource_type = record_info[5]
            action = record_info[6]
            return_code = record_info[7]
            return_msg = record_info[8]
            start_time = record_info[9]
            end_time = record_info[10]

            v_list_info = {
                              "user_uuid": user_uuid,
                              "user_name": user_name,
                              "source_ip": source_ip,
                              "resource_uuid": resource_uuid,
                              "resource_name": resource_name,
                              "resource_type": resource_type,
                              "action": action,
                              "return_code": return_code,
                              "return_msg": return_msg,
                              "start_time": start_time,
                              "end_time": end_time
                          }
            v_list_info = json.dumps(v_list_info, cls=CJsonEncoder)
            v_list_info = json.loads(v_list_info)

            operations_list.append(v_list_info)

        result = {"operations_list": operations_list}
        result['count'] = count

        return request_result(0, result)

    def operation_info(self, user_uuid, start_time, end_time):

        try:
            start_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                       time.localtime(float(start_time)))
            end_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                     time.localtime(float(end_time)))
            records_list = self.security_db.operation_info(
                                user_uuid, start_time, end_time)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        operations_list = []
        for record_info in records_list:
            user_name = record_info[0]
            source_ip = record_info[1]
            resource_uuid = record_info[2]
            resource_name = record_info[3]
            resource_type = record_info[4]
            action = record_info[5]
            return_code = record_info[6]
            return_msg = record_info[7]
            start_time = record_info[8]
            end_time = record_info[9]

            v_list_info = {
                              "user_uuid": user_uuid,
                              "user_name": user_name,
                              "source_ip": source_ip,
                              "resource_uuid": resource_uuid,
                              "resource_name": resource_name,
                              "resource_type": resource_type,
                              "action": action,
                              "return_code": return_code,
                              "return_msg": return_msg,
                              "start_time": start_time,
                              "end_time": end_time
                          }
            v_list_info = json.dumps(v_list_info, cls=CJsonEncoder)
            v_list_info = json.loads(v_list_info)

            operations_list.append(v_list_info)

        result = {"operations_list": operations_list}

        return request_result(0, result)

    def operation_update(self, record_uuid,
                         return_code, return_msg,
                         resource_uuid=None,
                         resource_name=None):

        try:
            self.security_db.operation_update(
                 record_uuid, return_code, return_msg,
                 resource_uuid, resource_name)
        except Exception, e:
            log.error('Database update error, reason=%s' % (e))
            return request_result(403)

        return request_result(0)
