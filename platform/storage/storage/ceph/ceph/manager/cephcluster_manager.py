#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

from common.logs import logging as log
from common.code import request_result
from ceph.driver import ceph_driver


class CephClusterManager(object):

    def __init__(self):

        self.ceph_driver = ceph_driver.CephDriver()

    def cephcluster_mount(self, cluster_info,
                          mon_list, host_ip,
                          rootpwd, host_type):

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

        if host_type == 'kvm':
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

            conf_dist = self.ceph_driver.conf_dist(cluster_uuid, host_ip)
            if int(conf_dist) != 0:
                log.error('host(IP:%s)ceph配置文件分发失败'
                          % (host_ip))
                return request_result(525)
        elif host_type == 'k8s':
            ceph_install = self.ceph_driver.ceph_growfs_install(
                                cluster_uuid, host_ip)
            if int(ceph_install) != 0:
                log.error('host(IP:%s)ceph服务安装失败'
                          % (host_ip))
                return request_result(535)

        control_host_name = self.ceph_driver.local_host_name()
        self.ceph_driver.host_ssh_del(host_ip, control_host_name)

        result = {
                     "host_ip": host_ip,
                     "host_type": host_type
                 }

        return request_result(0, result)
