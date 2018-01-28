# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

from common.logs import logging as log
from common.code import request_result
from common.parameters import parameter_check
from common.token_ucenterauth import token_check

from ceph.manager import host_manager
from ceph.manager import cephmon_manager
from ceph.manager import cephosd_manager
from ceph.manager import cephpool_manager
from ceph.manager import cephdisk_manager
from ceph.manager import cephcluster_manager


class CephRpcManager(object):

    def __init__(self):

        self.host_manager = host_manager.HostManager()
        self.cephmon_manager = cephmon_manager.CephMonManager()
        self.cephosd_manager = cephosd_manager.CephOsdManager()
        self.cephpool_manager = cephpool_manager.CephPoolManager()
        self.cephdisk_manager = cephdisk_manager.CephDiskManager()
        self.cephcluster_manager = cephcluster_manager.CephClusterManager()

    @token_check
    def host_info(self, context, parameters):

        try:
            host_ip = parameters.get('host_ip')
            password = parameters.get('password')

            host_ip = parameter_check(host_ip, ptype='pnip')
            password = parameter_check(password, ptype='ppwd')
        except Exception, e:
            log.warning('parameters error, parameters=%s, reason=%s'
                        % (parameters, e))
            return request_result(101)

        return self.host_manager.host_info(host_ip, password)

    @token_check
    def cephmon_init(self, context, parameters):

        try:
            cluster_info = parameters.get('cluster_info')
            mon01_hostip = parameters.get('mon01_hostip')
            mon01_rootpwd = parameters.get('mon01_rootpwd')
            mon01_snic = parameters.get('mon01_snic')
            mon02_hostip = parameters.get('mon02_hostip')
            mon02_rootpwd = parameters.get('mon02_rootpwd')
            mon02_snic = parameters.get('mon02_snic')

            mon01_hostip = parameter_check(mon01_hostip, ptype='pnip')
            mon01_rootpwd = parameter_check(mon01_rootpwd, ptype='ppwd')
            mon01_snic = parameter_check(mon01_snic, ptype='psnm')
            mon02_hostip = parameter_check(mon02_hostip, ptype='pnip')
            mon02_rootpwd = parameter_check(mon02_rootpwd, ptype='ppwd')
            mon02_snic = parameter_check(mon02_snic, ptype='psnm')
        except Exception, e:
            log.warning('parameters error, parameters=%s, reason=%s'
                        % (parameters, e))
            return request_result(101)

        return self.cephmon_manager.cephmon_init(
                    cluster_info,
                    mon01_hostip, mon01_rootpwd, mon01_snic,
                    mon02_hostip, mon02_rootpwd, mon02_snic)

    @token_check
    def cephmon_add(self, context, parameters):

        try:
            cluster_info = parameters.get('cluster_info')
            mon_id = parameters.get('mon_id')
            host_ip = parameters.get('host_ip')
            rootpwd = parameters.get('rootpwd')
            storage_nic = parameters.get('storage_nic')
            mon_list = parameters.get('mon_list')

            host_ip = parameter_check(host_ip, ptype='pnip')
            rootpwd = parameter_check(rootpwd, ptype='ppwd')
            storage_nic = parameter_check(storage_nic, ptype='psnm')
        except Exception, e:
            log.warning('parameters error, parameters=%s, reason=%s'
                        % (parameters, e))
            return request_result(101)

        return self.cephmon_manager.cephmon_add(
                    cluster_info, mon_id, host_ip,
                    rootpwd, storage_nic, mon_list)

    @token_check
    def cephcluster_mount(self, context, parameters):

        try:
            cluster_info = parameters.get('cluster_info')
            mon_list = parameters.get('mon_list')
            host_ip = parameters.get('host_ip')
            rootpwd = parameters.get('rootpwd')
            host_type = parameters.get('host_type')

            host_ip = parameter_check(host_ip, ptype='pnip')
            rootpwd = parameter_check(rootpwd, ptype='ppwd')
            if host_type not in ('kvm', 'k8s'):
                raise(Exception('Parameter host_type error'))
        except Exception, e:
            log.warning('parameters error, parameters=%s, reason=%s'
                        % (parameters, e))
            return request_result(101)

        return self.cephcluster_manager.cephcluster_mount(
                    cluster_info, mon_list, host_ip,
                    rootpwd, host_type)

    @token_check
    def cephosd_add(self, context, parameters):

        try:
            cluster_info = parameters.get('cluster_info')
            mon_list = parameters.get('mon_list')
            host_ip = parameters.get('host_ip')
            rootpwd = parameters.get('rootpwd')
            storage_nic = parameters.get('storage_nic')
            jour_disk = parameters.get('jour_disk')
            data_disk = parameters.get('data_disk')
            disk_type = parameters.get('disk_type')
            weight = parameters.get('weight')

            host_ip = parameter_check(host_ip, ptype='pnip')
            rootpwd = parameter_check(rootpwd, ptype='ppwd')
            storage_nic = parameter_check(storage_nic, ptype='psnm')
            jour_disk = parameter_check(jour_disk, ptype='pdsk')
            data_disk = parameter_check(data_disk, ptype='pdsk')
            weight = parameter_check(weight, ptype='pflt')
            if disk_type not in ('hdd', 'ssd'):
                raise(Exception('Parameter disk_type error'))
        except Exception, e:
            log.warning('parameters error, parameters=%s, reason=%s'
                        % (parameters, e))
            return request_result(101)

        return self.cephosd_manager.cephosd_add(
                    cluster_info, mon_list,
                    host_ip, rootpwd, storage_nic,
                    jour_disk, data_disk, disk_type, weight)

    @token_check
    def cephosd_delete(self, context, parameters):

        try:
            osd_id = parameters.get('osd_id')
            host_ip = parameters.get('host_ip')
            rootpwd = parameters.get('rootpwd')

            osd_id = parameter_check(osd_id, ptype='pint')
            host_ip = parameter_check(host_ip, ptype='pnip')
            rootpwd = parameter_check(rootpwd, ptype='ppwd')
        except Exception, e:
            log.warning('parameters error, parameters=%s, reason=%s'
                        % (parameters, e))
            return request_result(101)

        return self.cephosd_manager.cephosd_delete(
                    osd_id, host_ip, rootpwd)

    @token_check
    def cephosd_reweight(self, context, parameters):

        try:
            osd_id = parameters.get('osd_id')
            weight = parameters.get('weight')

            osd_id = parameter_check(osd_id, ptype='pint')
            weight = parameter_check(weight, ptype='pflt')
        except Exception, e:
            log.warning('parameters error, parameters=%s, reason=%s'
                        % (parameters, e))
            return request_result(101)

        return self.cephosd_manager.cephosd_reweight(
                    osd_id, weight)

    @token_check
    def cephpool_create(self, context, parameters):

        try:
            pool_type = parameters.get('pool_type')
            pool_name = parameters.get('pool_name')

            pool_name = parameter_check(pool_name, ptype='pnam')
            if pool_type not in ('hdd', 'ssd'):
                raise(Exception('Parameter pool_type error'))
        except Exception, e:
            log.warning('parameters error, parameters=%s, reason=%s'
                        % (parameters, e))
            return request_result(101)

        return self.cephpool_manager.cephpool_create(
                    pool_type, pool_name)

    @token_check
    def cephpool_info(self, context, parameters):

        return self.cephpool_manager.cephpool_info()

    @token_check
    def disk_create(self, context, parameters):

        try:
            pool_name = parameters['pool_name']
            disk_name = parameters['disk_name']
            disk_size = parameters['disk_size']

            pool_name = parameter_check(pool_name, ptype='pnam')
            disk_name = parameter_check(disk_name, ptype='pstr')
            disk_size = parameter_check(disk_size, ptype='pint')
        except Exception, e:
            log.warning('parameters error, parameters=%s, reason=%s'
                        % (parameters, e))
            return request_result(101)

        return self.cephdisk_manager.disk_create(
                    pool_name, disk_name, disk_size)

    @token_check
    def disk_delete(self, context, parameters):

        try:
            pool_name = parameters['pool_name']
            disk_name = parameters['disk_name']

            pool_name = parameter_check(pool_name, ptype='pnam')
            disk_name = parameter_check(disk_name, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, parameters=%s, reason=%s'
                        % (parameters, e))
            return request_result(101)

        return self.cephdisk_manager.disk_delete(
                    pool_name, disk_name)

    @token_check
    def disk_resize(self, context, parameters):

        try:
            pool_name = parameters['pool_name']
            disk_name = parameters['disk_name']
            disk_size = parameters['disk_size']

            pool_name = parameter_check(pool_name, ptype='pnam')
            disk_name = parameter_check(disk_name, ptype='pstr')
            disk_size = parameter_check(disk_size, ptype='pint')
        except Exception, e:
            log.warning('parameters error, parameters=%s, reason=%s'
                        % (parameters, e))
            return request_result(101)

        return self.cephdisk_manager.disk_resize(
                    pool_name, disk_name, disk_size)

    @token_check
    def rbd_growfs(self, context, parameters):

        try:
            image_name = parameters['image_name']
            fs_type = parameters['fs_type']

            image_name = parameter_check(image_name, ptype='pstr')
            if fs_type not in ('xfs', 'ext4'):
                raise(Exception('Parameter fs_type error'))
        except Exception, e:
            log.warning('parameters error, parameters=%s, reason=%s'
                        % (parameters, e))
            return request_result(101)

        return self.cephdisk_manager.disk_growfs(
                    image_name, fs_type)
