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


class CephOsdManager(object):

    def __init__(self):

        self.storage_db = storage_db.StorageDB()
        self.storage_driver = storage_driver.StorageDriver()

    @operation_record(resource_type='cephosd', action='create')
    def cephosd_add(self, cluster_uuid, host_uuid,
                    host_ip, rootpwd, storage_nic,
                    jour_disk, data_disk, disk_type, weight,
                    token, source_ip, resource_name):

        try:
            cluster_info = self.storage_db.ceph_cluster_info(
                                cluster_uuid)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        cluster_uuid = cluster_info[0][0]
        cluster_name = cluster_info[0][1]
        cluster_auth = cluster_info[0][2]
        service_auth = cluster_info[0][3]
        client_auth = cluster_info[0][4]
        ceph_pgnum = cluster_info[0][5]
        ceph_pgpnum = cluster_info[0][6]
        public_network = cluster_info[0][7]
        cluster_network = cluster_info[0][8]
        osd_full_ratio = cluster_info[0][9]
        osd_nearfull_ratio = cluster_info[0][10]
        journal_size = cluster_info[0][11]
        ntp_server = cluster_info[0][12]

        cluster_info = {
                           "cluster_uuid": cluster_uuid,
                           "cluster_name": cluster_name,
                           "cluster_auth": cluster_auth,
                           "service_auth": service_auth,
                           "client_auth": client_auth,
                           "ceph_pgnum": ceph_pgnum,
                           "ceph_pgpnum": ceph_pgpnum,
                           "public_network": public_network,
                           "cluster_network": cluster_network,
                           "osd_full_ratio": osd_full_ratio,
                           "osd_nearfull_ratio": osd_nearfull_ratio,
                           "journal_size": journal_size,
                           "ntp_server": ntp_server
                       }

        try:
            mon_list = self.storage_db.mon_list(cluster_uuid)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        osd_add_result = self.storage_driver.cephosd_add(
                              token, cluster_uuid, cluster_info,
                              mon_list, host_ip, rootpwd,
                              storage_nic, jour_disk, data_disk,
                              disk_type, weight)
        status_code = osd_add_result.get('status')
        if int(status_code) != 0:
            log.error('Ceph osd add failure, host_ip=%s, storage_nic=%s'
                      % (host_ip, storage_nic))
            return request_result(status_code)

        host_name = osd_add_result.get('result').get('host_name')
        storage_ip = osd_add_result.get('result').get('storage_ip')
        osd_id = osd_add_result.get('result').get('osd_id')
        osd_uuid = str(uuid.uuid4())

        try:
            self.storage_db.cephosd_add(
                 osd_uuid, cluster_uuid, osd_id,
                 host_uuid, storage_ip, jour_disk,
                 data_disk, disk_type, weight)
        except Exception, e:
            log.error('Database insert error, reason=%s' % (e))
            return request_result(401)

        result = {
                     "osd_uuid": osd_uuid,
                     "cluster_uuid": cluster_uuid,
                     "osd_id": osd_id,
                     "host_uuid": host_uuid,
                     "host_name": host_name,
                     "host_ip": host_ip,
                     "storage_ip": storage_ip,
                     "jour_disk": jour_disk,
                     "data_disk": data_disk,
                     "disk_type": disk_type,
                     "weight": weight,
                     "resource_uuid": osd_uuid,
                     "resource_name": osd_id
                 }

        return request_result(0, result)

    @operation_record(resource_type='cephosd', action='delete')
    def cephosd_delete(self, cluster_uuid, osd_uuid, rootpwd,
                       token, source_ip, resource_uuid):

        try:
            osd_info = self.storage_db.cephosd_info(osd_uuid)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        osd_id = osd_info[0][1]
        host_ip = osd_info[0][13]

        osd_del_result = self.storage_driver.cephosd_delete(
                              token, cluster_uuid, osd_id,
                              host_ip, rootpwd)
        status_code = osd_del_result.get('status')
        if int(status_code) != 0:
            log.error('Ceph osd delete failure, osd_id=%s, host_ip=%s'
                      % (osd_id, host_ip))
            return request_result(status_code)

        try:
            self.storage_db.cephosd_delete(osd_uuid)
        except Exception, e:
            log.error('Database delete error, reason=%s' % (e))
            return request_result(402)

        result = {
                     "cluster_uuid": cluster_uuid,
                     "osd_uuid": osd_uuid,
                     "osd_id": osd_id,
                     "resource_name": osd_id
                 }

        return request_result(0, result)

    @operation_record(resource_type='cephosd', action='update')
    def cephosd_reweight(self, cluster_uuid, osd_uuid, weight,
                         token, source_ip, resource_uuid):

        try:
            osd_info = self.storage_db.cephosd_info(osd_uuid)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        osd_id = osd_info[0][1]

        osd_reweight = self.storage_driver.cephosd_reweight(
                            token, cluster_uuid, osd_id, weight)
        status_code = osd_reweight.get('status')
        if int(status_code) != 0:
            log.error('Ceph osd reweight failure, osd_id=%s'
                      % (osd_id))
            return request_result(status_code)

        try:
            self.storage_db.cephosd_reweight(osd_uuid, weight)
        except Exception, e:
            log.error('Database update error, reason=%s' % (e))
            return request_result(403)

        result = {
                     "cluster_uuid": cluster_uuid,
                     "osd_uuid": osd_uuid,
                     "osd_id": osd_id,
                     "weight": weight,
                     "resource_name": osd_id
                 }

        return request_result(0, result)

    def cephosd_info(self, osd_uuid):

        try:
            osd_info = self.storage_db.cephosd_info(osd_uuid)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        cluster_uuid = osd_info[0][0]
        osd_id = osd_info[0][1]
        host_uuid = osd_info[0][2]
        storage_ip = osd_info[0][3]
        jour_disk = osd_info[0][4]
        data_disk = osd_info[0][5]
        disk_type = osd_info[0][6]
        weight = osd_info[0][7]
        status = osd_info[0][8]
        create_time = osd_info[0][9]
        update_time = osd_info[0][10]
        cluster_name = osd_info[0][11]
        host_name = osd_info[0][12]
        host_ip = osd_info[0][13]

        v_result = {
                       "osd_uuid": osd_uuid,
                       "cluster_uuid": cluster_uuid,
                       "cluster_name": cluster_name,
                       "osd_id": osd_id,
                       "host_uuid": host_uuid,
                       "host_name": host_name,
                       "host_ip": host_ip,
                       "storage_ip": storage_ip,
                       "jour_disk": jour_disk,
                       "data_disk": data_disk,
                       "disk_type": disk_type,
                       "weight": weight,
                       "status": status,
                       "create_time": create_time,
                       "update_time": update_time
                   }

        v_result = json.dumps(v_result, cls=CJsonEncoder)
        result = json.loads(v_result)

        return request_result(0, result)

    def cephosd_list(self, cluster_uuid, page_size, page_num):

        try:
            osd_list_info = self.storage_db.cephosd_list(
                                 cluster_uuid, page_size, page_num)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        osd_list = osd_list_info.get('osd_list')
        count = osd_list_info.get('count')

        result_list = []
        for osd_info in osd_list:
            osd_uuid = osd_info[0]
            osd_id = osd_info[1]
            host_uuid = osd_info[2]
            storage_ip = osd_info[3]
            jour_disk = osd_info[4]
            data_disk = osd_info[5]
            disk_type = osd_info[6]
            weight = osd_info[7]
            status = osd_info[8]
            create_time = osd_info[9]
            update_time = osd_info[10]
            cluster_name = osd_info[11]
            host_name = osd_info[12]
            host_ip = osd_info[13]

            v_result = {
                           "osd_uuid": osd_uuid,
                           "cluster_uuid": cluster_uuid,
                           "cluster_name": cluster_name,
                           "osd_id": osd_id,
                           "host_uuid": host_uuid,
                           "host_name": host_name,
                           "host_ip": host_ip,
                           "storage_ip": storage_ip,
                           "jour_disk": jour_disk,
                           "data_disk": data_disk,
                           "disk_type": disk_type,
                           "weight": weight,
                           "status": status,
                           "create_time": create_time,
                           "update_time": update_time
                       }

            v_result = json.dumps(v_result, cls=CJsonEncoder)
            v_result = json.loads(v_result)
            result_list.append(v_result)

        result = {"osd_list": result_list}
        result['count'] = count

        return request_result(0, result)
