# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import uuid
import json

from common.logs import logging as log
from common.code import request_result
from common.json_encode import CJsonEncoder
from common.operation_record import operation_record

from storage.db import storage_db
from storage.driver import storage_driver


class CephClusterManager(object):

    def __init__(self):

        self.storage_db = storage_db.StorageDB()
        self.storage_driver = storage_driver.StorageDriver()

    @operation_record(resource_type='cephcluster', action='create')
    def cephcluster_create(self, cluster_name, cluster_uuid,
                           cluster_auth, service_auth, client_auth,
                           ceph_pgnum, ceph_pgpnum, public_network,
                           cluster_network, osd_full_ratio,
                           osd_nearfull_ratio, journal_size, ntp_server,
                           token, source_ip, resource_name):

        cluster_uuid = cluster_uuid or str(uuid.uuid4())
        cluster_auth = cluster_auth or 'none'
        service_auth = service_auth or 'none'
        client_auth = client_auth or 'none'
        ceph_pgnum = ceph_pgnum or 300
        ceph_pgpnum = ceph_pgpnum or 300
        public_network = public_network or '192.168.1.0/24'
        cluster_network = cluster_network or '10.10.1.0/24'
        osd_full_ratio = osd_full_ratio or '.85'
        osd_nearfull_ratio = osd_nearfull_ratio or '.70'

        try:
            name_check = self.storage_db.cluster_name_check(
                              cluster_name)[0][0]
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        if name_check != 0:
            log.warning('Ceph cluster name(%s) already exists'
                        % (cluster_name))
            return request_result(301)

        try:
            self.storage_db.ceph_cluster_create(
                 cluster_uuid, cluster_name, cluster_auth,
                 service_auth, client_auth, ceph_pgnum,
                 ceph_pgpnum, public_network, cluster_network,
                 osd_full_ratio, osd_nearfull_ratio,
                 journal_size, ntp_server)
        except Exception, e:
            log.error('Database insert error, reason=%s' % (e))
            return request_result(401)

        result = {
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
                     "ntp_server": ntp_server,
                     "resource_uuid": cluster_uuid
                 }

        return request_result(0, result)

    def cephcluster_info(self, cluster_uuid):

        try:
            cluster_info = self.storage_db.ceph_cluster_info(
                                cluster_uuid)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

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
        create_time = cluster_info[0][13]
        update_time = cluster_info[0][14]

        v_result = {
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
                       "ntp_server": ntp_server,
                       "create_time": create_time,
                       "update_time": update_time
                   }

        v_result = json.dumps(v_result, cls=CJsonEncoder)
        result = json.loads(v_result)

        return request_result(0, result)

    def cephcluster_list(self):

        try:
            cluster_list = self.storage_db.ceph_cluster_list()
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        result_list = []
        for cluster_info in cluster_list:
            cluster_uuid = cluster_info[0]
            cluster_name = cluster_info[1]
            cluster_auth = cluster_info[2]
            service_auth = cluster_info[3]
            client_auth = cluster_info[4]
            ceph_pgnum = cluster_info[5]
            ceph_pgpnum = cluster_info[6]
            public_network = cluster_info[7]
            cluster_network = cluster_info[8]
            osd_full_ratio = cluster_info[9]
            osd_nearfull_ratio = cluster_info[10]
            journal_size = cluster_info[11]
            ntp_server = cluster_info[12]
            create_time = cluster_info[13]
            update_time = cluster_info[14]

            v_result = {
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
                           "ntp_server": ntp_server,
                           "create_time": create_time,
                           "update_time": update_time
                       }

            v_result = json.dumps(v_result, cls=CJsonEncoder)
            v_result = json.loads(v_result)
            result_list.append(v_result)

        result = {"cluster_list": result_list}

        return request_result(0, result)

    @operation_record(resource_type='cephcluster', action='update')
    def cephcluster_mount(self, cluster_uuid,
                          host_ip, password, host_type,
                          token, source_ip, resource_uuid):

        try:
            host_check = self.storage_db.ceph_host_check(
                              host_ip)[0][0]
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        if (host_check != 0) and (host_type == 'kvm'):
            log.info('Host(%s) already in ceph cluster' % (host_ip))
            return request_result(0)

        req_result = self.cephcluster_info(cluster_uuid)
        status_code = req_result.get('status')
        if int(status_code) != 0:
            log.error('Get cluster info failure, cluster_uuid=%s'
                      % (cluster_uuid))
            return request_result(status_code)

        cluster_info = req_result.get('result')
        cluster_name = cluster_info.get('cluster_name')

        try:
            mon_list = self.storage_db.mon_list(cluster_uuid)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        req_result = self.storage_driver.cephcluster_mount(
                          token, cluster_uuid, cluster_info,
                          mon_list, host_ip, password, host_type)
        status_code = req_result.get('status')
        if int(status_code) != 0:
            log.error('Cephcluster mount failure, '
                      'cluster_uuid=%s, host_ip=%s'
                      % (cluster_uuid, host_ip))
            return request_result(status_code)

        result = {
                     "cluster_uuid": cluster_uuid,
                     "host_ip": host_ip,
                     "host_type": host_type,
                     "resource_name": cluster_name
                 }

        return request_result(0, result)
