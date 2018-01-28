# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import uuid
import json

from conf import conf
from common.logs import logging as log
from common.code import request_result
from common.json_encode import CJsonEncoder
from common.operation_record import operation_record

from storage.db import storage_db
from storage.driver import storage_driver


class HostManager(object):

    def __init__(self):

        self.storage_db = storage_db.StorageDB()
        self.storage_driver = storage_driver.StorageDriver()

    @operation_record(resource_type='host', action='create')
    def host_create(self, host_ip, rootpwd,
                    token, source_ip, resource_name):

        req_result = self.storage_driver.host_info(
                          token, host_ip, rootpwd)
        status_code = req_result.get('status')
        if int(status_code) != 0:
            log.error('Get host info failure, host_ip=%s'
                      % (host_ip))
            return request_result(status_code)

        host_name = req_result.get('result').get('host_name')
        host_cpu = req_result.get('result').get('host_cpu')
        host_mem = req_result.get('result').get('host_mem')
        host_disk = req_result.get('result').get('host_disk')
        host_nic = req_result.get('result').get('host_nic')

        try:
            host_check = self.storage_db.host_check(host_ip)[0][0]
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        if host_check == 0:
            try:
                host_uuid = str(uuid.uuid4())
                self.storage_db.host_create(
                     host_uuid, host_name, host_ip,
                     host_cpu, host_mem, host_disk, host_nic)
            except Exception, e:
                log.error('Database insert error, reason=%s' % (e))
                return request_result(401)
        else:
            try:
                self.storage_db.host_update(
                     host_name, host_ip,
                     host_cpu, host_mem, host_disk, host_nic)
            except Exception, e:
                log.error('Database insert error, reason=%s' % (e))
                return request_result(401)

            try:
                host_uuid = self.storage_db.host_uuid(host_ip)[0][0]
            except Exception, e:
                log.error('Database select error, reason=%s' % (e))
                return request_result(404)

        result = {
                     "host_uuid": host_uuid,
                     "host_name": host_name,
                     "host_ip": host_ip,
                     "host_cpu": host_cpu,
                     "host_mem": host_mem,
                     "host_disk": host_disk,
                     "host_nic": host_nic,
                     "resource_uuid": host_uuid,
                     "resource_name": host_name
                 }

        return request_result(0, result)

    @operation_record(resource_type='host', action='delete')
    def host_delete(self, host_uuid,
                    token, source_ip, resource_uuid):

        try:
            self.storage_db.host_delete(host_uuid)
        except Exception, e:
            log.error('Database delete error, reason=%s' % (e))
            return request_result(402)

        return request_result(0)

    def host_info(self, host_uuid):

        try:
            host_info = self.storage_db.host_info(host_uuid)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        host_name = host_info[0][0]
        host_ip = host_info[0][1]
        host_cpu = host_info[0][2]
        host_mem = host_info[0][3]
        host_disk = host_info[0][4]
        host_nic = host_info[0][5]
        host_status = host_info[0][6]
        create_time = host_info[0][7]
        update_time = host_info[0][8]

        host_disk = [json.loads(x) for x in host_disk.split(";")]
        host_nic = [json.loads(x) for x in host_nic.split(";")]

        v_result = {
                       "host_uuid": host_uuid,
                       "host_name": host_name,
                       "host_ip": host_ip,
                       "host_cpu": host_cpu,
                       "host_mem": host_mem,
                       "host_disk": host_disk,
                       "host_nic": host_nic,
                       "host_status": host_status,
                       "create_time": create_time,
                       "update_time": update_time,
                       "resource_name": host_name
                   }

        v_result = json.dumps(v_result, cls=CJsonEncoder)
        result = json.loads(v_result)

        return request_result(0, result)

    def host_list(self, page_size, page_num):

        try:
            host_list_info = self.storage_db.host_list(
                             page_size, page_num)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        host_list = host_list_info.get('host_list')
        count = host_list_info.get('count')

        result_list = []
        for host_info in host_list:
            host_uuid = host_info[0]
            host_name = host_info[1]
            host_ip = host_info[2]
            host_cpu = host_info[3]
            host_mem = host_info[4]
            host_disk = host_info[5]
            host_nic = host_info[6]
            host_status = host_info[7]
            create_time = host_info[8]
            update_time = host_info[9]

            host_disk = [json.loads(x) for x in host_disk.split(";")]
            host_nic = [json.loads(x) for x in host_nic.split(";")]

            v_result = {
                           "host_uuid": host_uuid,
                           "host_name": host_name,
                           "host_ip": host_ip,
                           "host_cpu": host_cpu,
                           "host_mem": host_mem,
                           "host_disk": host_disk,
                           "host_nic": host_nic,
                           "host_status": host_status,
                           "create_time": create_time,
                           "update_time": update_time
                       }

            v_result = json.dumps(v_result, cls=CJsonEncoder)
            v_result = json.loads(v_result)
            result_list.append(v_result)

        result = {"host_list": result_list}
        result['count'] = count

        return request_result(0, result)
