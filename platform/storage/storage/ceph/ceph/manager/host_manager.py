#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

from common.logs import logging as log
from common.code import request_result
from ceph.driver import ceph_driver


class HostManager(object):

    def __init__(self):

        self.ceph_driver = ceph_driver.CephDriver()

    def host_info(self, host_ip, rootpwd):

        host_ssh_conf = self.ceph_driver.host_ssh_conf(
                             host_ip, rootpwd)
        if host_ssh_conf != 0:
            if host_ssh_conf == 1:
                log.warning('Host(IP:%s)密码错误' % (host_ip))
                return request_result(523)
            elif host_ssh_conf == 2:
                log.warning('Host(IP:%s)连接超时' % (host_ip))
                return request_result(522)
            else:
                log.warning('Host(IP:%s)连接错误' % (host_ip))
                return request_result(601)

        host_name = self.ceph_driver.remote_host_name(host_ip)
        if not host_name:
            log.error('无法获取host(IP:%s)主机名' % (host_ip))
            return request_result(524)

        host_cpu = self.ceph_driver.remote_host_cpu(host_ip)
        if not host_cpu:
            log.error('无法获取host(IP:%s)CPU信息' % (host_ip))
            return request_result(524)

        host_mem = self.ceph_driver.remote_host_mem(host_ip)
        if not host_mem:
            log.error('无法获取host(IP:%s)内存信息' % (host_ip))
            return request_result(524)

        disk_list = self.ceph_driver.remote_host_disk(host_ip)
        if not disk_list:
            log.error('无法获取host(IP:%s)磁盘信息' % (host_ip))
            return request_result(524)

        disk_list = disk_list.split('\n')
        host_disk = []
        for disk_info in disk_list:
            disk_info = disk_info.split(' ')
            disk_name = disk_info[0]
            disk_size = disk_info[1]
            disk_size = round((float(disk_size)/1024)/1024, 2)
            disk_info = {"disk_name": disk_name, "disk_size": disk_size}
            host_disk.append(disk_info)

        nic_list = self.ceph_driver.remote_host_nic_name(host_ip)
        if not nic_list:
            log.error('无法获取host(IP:%s)网卡信息' % (host_ip))
            return request_result(524)

        nic_list = nic_list.split('\n')
        host_nic = []
        for nic_name in nic_list:
            nic_info = self.ceph_driver.remote_host_nic_info(host_ip, nic_name)
            nic_info = nic_info.split('\n')
            nic_mac = nic_info[0]
            if len(nic_info) == 2:
                nic_ip = nic_info[1]
            else:
                nic_ip = None

            nic_info = {
                           "nic_name": nic_name,
                           "nic_mac": nic_mac,
                           "nic_ip": nic_ip
                       }
            host_nic.append(nic_info)

        control_host_name = self.ceph_driver.local_host_name()
        self.ceph_driver.host_ssh_del(host_ip, control_host_name)

        result = {
                     "host_name": host_name,
                     "host_cpu": host_cpu,
                     "host_mem": host_mem,
                     "host_disk": host_disk,
                     "host_nic": host_nic
                 }

        return request_result(0, result)
