#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import uuid

from common.logs import logging as log
from common.code import request_result
from ceph.driver import ceph_driver


class CephOsdManager(object):

    def __init__(self):

        self.ceph_driver = ceph_driver.CephDriver()

    def cephosd_add(self, cluster_info, mon_list,
                    host_ip, rootpwd, storage_nic,
                    jour_disk, data_disk, disk_type, weight):

        host_ssh_conf = self.ceph_driver.host_ssh_conf(
                             host_ip, rootpwd)
        if host_ssh_conf != 0:
            if host_ssh_conf == 1:
                log.warning('host(%s)密码错误' % (host_ip))
                return request_result(523)
            elif host_ssh_conf == 2:
                log.warning('host(%s)连接超时' % (host_ip))
                return request_result(522)
            else:
                log.warning('host(%s)连接错误' % (host_ip))
                return request_result(601)

        host_name = self.ceph_driver.remote_host_name(host_ip)
        if not host_name:
            log.error('无法获取节点(%s)主机名' % (host_ip))
            return request_result(524)

        storage_ip = self.ceph_driver.storage_ip(
                          host_ip, storage_nic)
        if not storage_ip:
            log.error('无法获取节点(%s)存储IP' % (host_ip))
            return request_result(524)

        jour_disk_check = self.ceph_driver.disk_use_check(host_ip, jour_disk)
        if int(jour_disk_check) != 0:
            log.warning('主机%s磁盘分区%s已被使用' %(host_name, jour_disk))
            return request_result(529)

        data_disk_check = self.ceph_driver.disk_use_check(host_ip, data_disk)
        if int(data_disk_check) != 0:
            log.warning('主机%s磁盘分区%s已被使用' %(host_name, data_disk))
            return request_result(529)

        if cluster_info:
            cluster_uuid = cluster_info.get('cluster_uuid')
            cluster_name = cluster_info.get('cluster_name')
            cluster_auth = cluster_info.get('cluster_auth')
            service_auth = cluster_info.get('service_auth')
            client_auth = cluster_info.get('client_auth')
            ceph_pgnum = cluster_info.get('ceph_pgnum')
            ceph_pgpnum = cluster_info.get('ceph_pgpnum')
            public_network = cluster_info.get('public_network')
            cluster_network = cluster_info.get('cluster_network')
            osd_full_ratio = cluster_info.get('osd_full_ratio')
            osd_nearfull_ratio = cluster_info.get('osd_nearfull_ratio')
            journal_size = cluster_info.get('journal_size')
            ntp_server = cluster_info.get('ntp_server')
        else:
            log.warning('Ceph cluster info not exists')
            return request_result(528)

        ntp_conf = self.ceph_driver.host_ntp_conf(
                        host_ip, ntp_server)
        if int(ntp_conf) != 0:
            log.error('Host ntp server conf failure, '
                      'host_ip=%s, ntp_server=%s'
                      % (host_ip, ntp_server))
            return request_result(530)

        self.ceph_driver.ceph_conf_init(
             cluster_uuid, cluster_auth, service_auth, client_auth,
             ceph_pgnum, ceph_pgpnum, public_network, cluster_network,
             osd_full_ratio, osd_nearfull_ratio, journal_size)
        for mon_info in mon_list:
            ceph_mon_id = mon_info[0]
            mon_host_name = mon_info[1]
            mon_storage_ip = mon_info[2]

            self.ceph_driver.mon_conf_update(
                 cluster_uuid, ceph_mon_id[-1],
                 mon_host_name, mon_storage_ip)

        osd_id = self.ceph_driver.osd_id_create()
        self.ceph_driver.osd_conf_add(
             cluster_uuid, host_name, data_disk, osd_id)
        conf_dist = self.ceph_driver.conf_dist(cluster_uuid, host_ip)
        if int(conf_dist) != 0:
            log.error('host(主机名:%s, IP:%s)ceph配置文件分发失败'
                      % (host_name, host_ip))
            return request_result(525)

        osd_add = self.ceph_driver.osd_add(
                       host_ip, host_name, jour_disk, data_disk,
                       disk_type, osd_id, weight)
        if int(osd_add) != 0:
            self.ceph_driver.osd_stop(host_ip, osd_id)
            self.ceph_driver.osd_host_del(host_ip, osd_id)
            self.ceph_driver.osd_out(osd_id)
            self.ceph_driver.osd_crush_out(osd_id)
            log.error('主机(hostname:%s, IP:%s)添加osd节点失败'
                      %(host_name, host_ip))
            return request_result(530)

        control_host_name = self.ceph_driver.local_host_name()
        self.ceph_driver.host_ssh_del(host_ip, control_host_name)

        result = {
                     "osd_id": osd_id,
                     "host_ip": host_ip,
                     "host_name": host_name,
                     "cluster_uuid": cluster_uuid,
                     "storage_nic": storage_nic,
                     "storage_ip": storage_ip,
                     "jour_disk": jour_disk,
                     "data_disk": data_disk,
                     "disk_type": disk_type,
                     "weight": weight
                 }

        return request_result(0, result)

    def cephosd_delete(self, osd_id, host_ip, rootpwd):

        pool_check = self.ceph_driver.pool_disk_check()
        if int(pool_check) > 8:
            ceph_check = self.ceph_driver.ceph_status_check()
            if int(ceph_check) == 0:
                log.warning('ceph存储状态异常，不允许执行osd节点移除操作。')
                return request_result(202)

            pool_used = self.ceph_driver.pool_used()
            if float(pool_used) >= 65:
                log.warning('ceph存储池剩余容量不足，不允许执行osd节点移除操作。')
                return request_result(531)

        host_ssh_conf = self.ceph_driver.host_ssh_conf(
                             host_ip, rootpwd)
        if host_ssh_conf == 0:
            osd_stop = self.ceph_driver.osd_stop(host_ip, osd_id)
            if int(osd_stop) != 0:
                log.error('无法停止存储节点(IP:%s)上osd(%s)服务' %(host_ip, osd_id))
                return request_result(532)

            osd_host_del = self.ceph_driver.osd_host_del(host_ip, osd_id)
            if int(osd_host_del) != 0:
                log.error('无法清除osd(%s)挂载信息和目录' %(osd_id))
                return request_result(532)

            control_host_name = self.ceph_driver.local_host_name()
            self.ceph_driver.host_ssh_del(host_ip, control_host_name)
        elif host_ssh_conf == 1:
            log.warning('host节点(%s)密码错误' % (host_ip))
            return request_result(523)

        osd_out = self.ceph_driver.osd_out(osd_id)
        if int(osd_out) != 0:
            log.error('将osd(%s)移出ceph存储失败'
                      % (osd_id))
            return request_result(532)

        osd_crush_out = self.ceph_driver.osd_crush_out(osd_id)
        if int(osd_crush_out) != 0:
            log.error('将osd(%s)移出ceph存储CRUSH map失败'
                      % (osd_id))
            return request_result(532)

        result = {
                     "host_ip": host_ip,
                     "osd_id": osd_id
                 }

        return request_result(0, result)

    def cephosd_reweight(self, osd_id, weight):

        osd_rewt = self.ceph_driver.osd_reweight(
                        osd_id, weight)
        if int(osd_rewt) != 0:
            log.error('调整ceph存储osd节点(osd.%s)权重失败'
                      % (osd_id))
            return request_result(533)

        result = {
                     "osd_id": osd_id,
                     "weight": weight
                 }

        return request_result(0, result)
