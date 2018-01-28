# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

from conf import conf
from common.logs import logging as log
from common.code import request_result
from common.acl import acl_check
from common.parameters import parameter_check
from common.token_ucenterauth import token_auth

from storage.manager import cephcluster_manager
from storage.manager import host_manager
from storage.manager import cephmon_manager
from storage.manager import cephosd_manager
from storage.manager import cephpool_manager
from storage.manager import clouddisk_manager


class StorageRpcManager(object):

    def __init__(self):

        self.billing_check = conf.billing
        self.cephcluster_manager = cephcluster_manager.CephClusterManager()
        self.host_manager = host_manager.HostManager()
        self.cephmon_manager = cephmon_manager.CephMonManager()
        self.cephosd_manager = cephosd_manager.CephOsdManager()
        self.cephpool_manager = cephpool_manager.CephPoolManager()
        self.clouddisk_manager = clouddisk_manager.CloudDiskManager()

    @acl_check
    def cephcluster_create(self, context, parameters):

        try:
            token = context['token']
            source_ip = context.get('source_ip')

            cluster_name = parameters.get('cluster_name')
            cluster_uuid = parameters.get('cluster_uuid')
            cluster_auth = parameters.get('cluster_auth')
            service_auth = parameters.get('service_auth')
            client_auth = parameters.get('client_auth')
            ceph_pgnum = parameters.get('ceph_pgnum')
            ceph_pgpnum = parameters.get('ceph_pgpnum')
            public_network = parameters.get('public_network')
            cluster_network = parameters.get('cluster_network')
            osd_full_ratio = parameters.get('osd_full_ratio')
            osd_nearfull_ratio = parameters.get('osd_nearfull_ratio')
            journal_size = parameters.get('journal_size')
            ntp_server = parameters.get('ntp_server')

            source_ip = parameter_check(source_ip, ptype='pnip',
                                        exist='no')
            cluster_name = parameter_check(cluster_name, ptype='pnam')
            cluster_uuid = parameter_check(cluster_uuid, ptype='pstr',
                                           exist='no')
            cluster_auth = parameter_check(cluster_auth, ptype='pnam',
                                           exist='no')
            service_auth = parameter_check(service_auth, ptype='pnam',
                                           exist='no')
            client_auth = parameter_check(client_auth, ptype='pnam',
                                          exist='no')
            ceph_pgnum = parameter_check(ceph_pgnum, ptype='pint',
                                         exist='no')
            ceph_pgpnum = parameter_check(ceph_pgpnum, ptype='pint',
                                          exist='no')
            public_network = parameter_check(public_network, ptype='pstr',
                                             exist='no')
            cluster_network = parameter_check(cluster_network, ptype='pstr',
                                              exist='no')
            osd_full_ratio = parameter_check(osd_full_ratio, ptype='pflt',
                                             exist='no')
            osd_nearfull_ratio = parameter_check(osd_nearfull_ratio,
                                                 ptype='pflt',
                                                 exist='no')
            journal_size = parameter_check(journal_size, ptype='pint')
            if int(journal_size) < 1000:
                raise(Exception('Parameter cost error, '
                                'journal_size must greater than 1000'))
            try:
                ntp_server = parameter_check(ntp_server, ptype='pnip')
            except Exception:
                ntp_server = parameter_check(ntp_server, ptype='pdmn')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cephcluster_manager.cephcluster_create(
                    cluster_name, cluster_uuid, cluster_auth,
                    service_auth, client_auth, ceph_pgnum,
                    ceph_pgpnum, public_network, cluster_network,
                    osd_full_ratio, osd_nearfull_ratio,
                    journal_size, ntp_server,
                    token=token, source_ip=source_ip,
                    resource_name=cluster_name)

    @acl_check
    def cephcluster_info(self, context, parameters):

        try:
            cluster_uuid = parameters.get('cluster_uuid')

            cluster_uuid = parameter_check(cluster_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cephcluster_manager.cephcluster_info(cluster_uuid)

    @acl_check
    def cephcluster_list(self, context, parameters):

        return self.cephcluster_manager.cephcluster_list()

    @acl_check
    def cephcluster_mount(self, context, parameters):

        try:
            token = context['token']
            source_ip = context.get('source_ip')

            cluster_uuid = parameters.get('cluster_uuid')
            host_ip = parameters.get('host_ip')
            password = parameters.get('password')
            host_type = parameters.get('host_type')

            cluster_uuid = parameter_check(cluster_uuid, ptype='pstr')
            host_ip = parameter_check(host_ip, ptype='pnip')
            password = parameter_check(password, ptype='ppwd')
            if host_type not in ('kvm', 'k8s'):
                raise(Exception('Parameter host_type error'))
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cephcluster_manager.cephcluster_mount(
                    cluster_uuid, host_ip, password, host_type,
                    token=token, source_ip=source_ip,
                    resource_uuid=cluster_uuid)

    @acl_check
    def host_create(self, context, parameters):

        try:
            token = context['token']
            source_ip = context.get('source_ip')

            host_ip = parameters.get('host_ip')
            password = parameters.get('password')

            host_ip = parameter_check(host_ip, ptype='pnip')
            password = parameter_check(password, ptype='ppwd')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.host_manager.host_create(
                    host_ip, password,
                    token=token, source_ip=source_ip,
                    resource_name=None)

    @acl_check
    def host_delete(self, context, parameters):

        try:
            token = context['token']
            source_ip = context.get('source_ip')

            host_uuid = parameters.get('host_uuid')

            host_uuid = parameter_check(host_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.host_manager.host_delete(
                    host_uuid,
                    token=token, source_ip=source_ip,
                    resource_uuid=host_uuid)

    @acl_check
    def host_info(self, context, parameters):

        try:
            host_uuid = parameters.get('host_uuid')

            host_uuid = parameter_check(host_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.host_manager.host_info(host_uuid)

    @acl_check
    def host_list(self, context, parameters):

        try:
            page_size = parameters.get('page_size')
            page_num = parameters.get('page_num')

            page_size = parameter_check(page_size, ptype='pint')
            page_num = parameter_check(page_num, ptype='pint')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.host_manager.host_list(
                    page_size, page_num)

    @acl_check
    def cephmon_init(self, context, parameters):

        try:
            token = context['token']
            source_ip = context.get('source_ip')

            cluster_uuid = parameters.get('cluster_uuid')
            mon01_hostuuid = parameters.get('mon01_hostuuid')
            mon01_hostip = parameters.get('mon01_hostip')
            mon01_rootpwd = parameters.get('mon01_rootpwd')
            mon01_snic = parameters.get('mon01_snic')
            mon02_hostuuid = parameters.get('mon02_hostuuid')
            mon02_hostip = parameters.get('mon02_hostip')
            mon02_rootpwd = parameters.get('mon02_rootpwd')
            mon02_snic = parameters.get('mon02_snic')

            cluster_uuid = parameter_check(cluster_uuid, ptype='pstr')
            mon01_hostuuid = parameter_check(mon01_hostuuid, ptype='pstr')
            mon01_hostip = parameter_check(mon01_hostip, ptype='pnip')
            mon01_rootpwd = parameter_check(mon01_rootpwd, ptype='ppwd')
            mon01_snic = parameter_check(mon01_snic, ptype='psnm')
            mon02_hostuuid = parameter_check(mon02_hostuuid, ptype='pstr')
            mon02_hostip = parameter_check(mon02_hostip, ptype='pnip')
            mon02_rootpwd = parameter_check(mon02_rootpwd, ptype='ppwd')
            mon02_snic = parameter_check(mon02_snic, ptype='psnm')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cephmon_manager.cephmon_init(
                    cluster_uuid, mon01_hostuuid,
                    mon01_hostip, mon01_rootpwd, mon01_snic,
                    mon02_hostuuid, mon02_hostip,
                    mon02_rootpwd, mon02_snic,
                    token=token, source_ip=source_ip,
                    resource_name=None)

    @acl_check
    def cephmon_add(self, context, parameters):

        try:
            token = context['token']
            source_ip = context.get('source_ip')

            cluster_uuid = parameters.get('cluster_uuid')
            host_uuid = parameters.get('host_uuid')
            host_ip = parameters.get('host_ip')
            rootpwd = parameters.get('rootpwd')
            storage_nic = parameters.get('storage_nic')

            cluster_uuid = parameter_check(cluster_uuid, ptype='pstr')
            host_uuid = parameter_check(host_uuid, ptype='pstr')
            host_ip = parameter_check(host_ip, ptype='pnip')
            rootpwd = parameter_check(rootpwd, ptype='ppwd')
            storage_nic = parameter_check(storage_nic, ptype='psnm')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cephmon_manager.cephmon_add(
                    cluster_uuid, host_uuid,
                    host_ip, rootpwd, storage_nic,
                    token=token, source_ip=source_ip,
                    resource_name=None)

    @acl_check
    def cephmon_info(self, context, parameters):

        try:
            mon_uuid = parameters.get('mon_uuid')

            mon_uuid = parameter_check(mon_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cephmon_manager.cephmon_info(mon_uuid)

    @acl_check
    def cephmon_list(self, context, parameters):

        try:
            cluster_uuid = parameters.get('cluster_uuid')

            cluster_uuid = parameter_check(cluster_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cephmon_manager.cephmon_list(cluster_uuid)

    @acl_check
    def cephosd_add(self, context, parameters):

        try:
            token = context['token']
            source_ip = context.get('source_ip')

            cluster_uuid = parameters.get('cluster_uuid')
            host_uuid = parameters.get('host_uuid')
            host_ip = parameters.get('host_ip')
            rootpwd = parameters.get('rootpwd')
            storage_nic = parameters.get('storage_nic')
            jour_disk = parameters.get('jour_disk')
            data_disk = parameters.get('data_disk')
            disk_type = parameters.get('disk_type')
            weight = parameters.get('weight')

            cluster_uuid = parameter_check(cluster_uuid, ptype='pstr')
            host_uuid = parameter_check(host_uuid, ptype='pstr')
            host_ip = parameter_check(host_ip, ptype='pnip')
            rootpwd = parameter_check(rootpwd, ptype='ppwd')
            storage_nic = parameter_check(storage_nic, ptype='psnm')
            jour_disk = parameter_check(jour_disk, ptype='pdsk')
            data_disk = parameter_check(data_disk, ptype='pdsk')
            weight = parameter_check(weight, ptype='pflt')
            if disk_type not in ('hdd', 'ssd'):
                raise(Exception('Parameter disk_type error'))
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cephosd_manager.cephosd_add(
                    cluster_uuid, host_uuid,
                    host_ip, rootpwd, storage_nic,
                    jour_disk, data_disk, disk_type, weight,
                    token=token, source_ip=source_ip,
                    resource_name=None)

    @acl_check
    def cephosd_delete(self, context, parameters):

        try:
            token = context['token']
            source_ip = context.get('source_ip')

            cluster_uuid = parameters.get('cluster_uuid')
            osd_uuid = parameters.get('osd_uuid')
            rootpwd = parameters.get('rootpwd')

            cluster_uuid = parameter_check(cluster_uuid, ptype='pstr')
            osd_uuid = parameter_check(osd_uuid, ptype='pstr')
            rootpwd = parameter_check(rootpwd, ptype='ppwd')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cephosd_manager.cephosd_delete(
                    cluster_uuid, osd_uuid, rootpwd,
                    token=token, source_ip=source_ip,
                    resource_uuid=osd_uuid)

    @acl_check
    def cephosd_reweight(self, context, parameters):

        try:
            token = context['token']
            source_ip = context.get('source_ip')

            cluster_uuid = parameters.get('cluster_uuid')
            osd_uuid = parameters.get('osd_uuid')
            weight = parameters.get('weight')

            cluster_uuid = parameter_check(cluster_uuid, ptype='pstr')
            osd_uuid = parameter_check(osd_uuid, ptype='pstr')
            weight = parameter_check(weight, ptype='pflt')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cephosd_manager.cephosd_reweight(
                    cluster_uuid, osd_uuid, weight,
                    token=token, source_ip=source_ip,
                    resource_uuid=osd_uuid)

    @acl_check
    def cephosd_info(self, context, parameters):

        try:
            osd_uuid = parameters.get('osd_uuid')

            osd_uuid = parameter_check(osd_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cephosd_manager.cephosd_info(osd_uuid)

    @acl_check
    def cephosd_list(self, context, parameters):

        try:
            cluster_uuid = parameters.get('cluster_uuid')
            page_size = parameters.get('page_size')
            page_num = parameters.get('page_num')

            cluster_uuid = parameter_check(cluster_uuid, ptype='pstr')
            page_size = parameter_check(page_size, ptype='pint')
            page_num = parameter_check(page_num, ptype='pint')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cephosd_manager.cephosd_list(
                    cluster_uuid, page_size, page_num)

    @acl_check
    def cephpool_create(self, context, parameters):

        try:
            token = context['token']
            source_ip = context.get('source_ip')

            cluster_uuid = parameters.get('cluster_uuid')
            pool_type = parameters.get('pool_type')

            cluster_uuid = parameter_check(cluster_uuid, ptype='pstr')
            if pool_type not in ('hdd', 'ssd'):
                raise(Exception('Parameter pool_type error'))
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cephpool_manager.cephpool_create(
                    cluster_uuid, pool_type,
                    token=token, source_ip=source_ip,
                    resource_name=None)

    @acl_check
    def cephpool_info(self, context, parameters):

        try:
            pool_uuid = parameters.get('pool_uuid')

            pool_uuid = parameter_check(pool_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cephpool_manager.cephpool_info(pool_uuid)

    @acl_check
    def cephpool_list(self, context, parameters):

        try:
            cluster_uuid = parameters.get('cluster_uuid')

            cluster_uuid = parameter_check(cluster_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cephpool_manager.cephpool_list(cluster_uuid)

    @acl_check
    def volume_create(self, context, parameters):

        try:
            token = context['token']
            source_ip = context.get('source_ip')
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')
            team_uuid = user_info.get('team_uuid')
            project_uuid = user_info.get('project_uuid')

            cluster_uuid = parameters.get('cluster_uuid')
            volume_name = parameters.get('volume_name')
            volume_size = parameters.get('volume_size')
            volume_type = parameters.get('volume_type')
            fs_type = parameters.get('fs_type')
            cost = parameters.get('cost')

            cluster_uuid = parameter_check(cluster_uuid, ptype='pstr')
            source_ip = parameter_check(source_ip, ptype='pnip', exist='no')
            volume_name = parameter_check(volume_name, ptype='pnam')
            volume_size = parameter_check(volume_size, ptype='pint')
            if volume_type not in ('hdd', 'ssd'):
                raise(Exception('Parameter volume_type error'))
            if self.billing_check is True:
                cost = parameter_check(cost, ptype='pflt')
                if float(cost) < 0:
                    raise(Exception('Parameter cost error, '
                                    'cost must greater than 0'))
            else:
                cost = parameter_check(cost, ptype='pflt', exist='no')
            if fs_type not in ('xfs', 'ext4'):
                raise(Exception('Parameter fs_type error'))
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.clouddisk_manager.volume_create(
                    team_uuid, project_uuid, user_uuid,
                    cluster_uuid, volume_name, volume_size,
                    volume_type, fs_type, cost,
                    token=token, source_ip=source_ip,
                    resource_name=volume_name)

    @acl_check
    def volume_delete(self, context, parameters):

        try:
            token = context['token']
            volume_uuid = context['resource_uuid']
            source_ip = context.get('source_ip')

            volume_uuid = parameter_check(volume_uuid, ptype='pstr')
            source_ip = parameter_check(source_ip, ptype='pnip', exist='no')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.clouddisk_manager.volume_logical_delete(
                    volume_uuid, token=token, source_ip=source_ip,
                    resource_uuid=volume_uuid)

    @acl_check
    def volume_info(self, context, parameters):

        try:
            volume_uuid = context['resource_uuid']

            volume_uuid = parameter_check(volume_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.clouddisk_manager.volume_info(volume_uuid)

    @acl_check
    def volume_list(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')
            team_uuid = user_info.get('team_uuid')
            team_priv = user_info.get('team_priv')
            project_uuid = user_info.get('project_uuid')
            project_priv = user_info.get('project_priv')

            cluster_uuid = parameters.get('cluster_uuid')
            page_size = parameters.get('page_size')
            page_num = parameters.get('page_num')

            cluster_uuid = parameter_check(cluster_uuid, ptype='pstr')
            page_size = parameter_check(page_size, ptype='pint')
            page_num = parameter_check(page_num, ptype='pint')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.clouddisk_manager.volume_list(
                    user_uuid, team_uuid, team_priv,
                    project_uuid, project_priv,
                    cluster_uuid, page_size, page_num)

    @acl_check
    def volume_update(self, context, parameters):

        try:
            token = context['token']
            volume_uuid = context['resource_uuid']
            source_ip = context.get('source_ip')

            update = parameters.get('update')
            volume_size = parameters.get('volume_size')
            volume_status = parameters.get('volume_status')

            token = parameter_check(token, ptype='pstr')
            volume_uuid = parameter_check(volume_uuid, ptype='pstr')
            source_ip = parameter_check(source_ip, ptype='pnip', exist='no')
            if update == 'size':
                volume_size = parameter_check(volume_size, ptype='pint')
            elif update == 'status':
                if (volume_status != 'using') and (volume_status != 'unused'):
                    raise
            else:
                raise
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.clouddisk_manager.volume_update(
                    volume_uuid, update, volume_size,
                    volume_status, token=token,
                    source_ip=source_ip, resource_uuid=volume_uuid)

    @acl_check
    def volume_reclaim_list(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')
            team_uuid = user_info.get('team_uuid')
            team_priv = user_info.get('team_priv')
            project_uuid = user_info.get('project_uuid')
            project_priv = user_info.get('project_priv')

            page_size = parameters.get('page_size')
            page_num = parameters.get('page_num')

            page_size = parameter_check(page_size, ptype='pint')
            page_num = parameter_check(page_num, ptype='pint')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.clouddisk_manager.volume_reclaim_list(
                    user_uuid, team_uuid, team_priv,
                    project_uuid, project_priv,
                    page_size, page_num)

    @acl_check
    def volume_reclaim_recovery(self, context, parameters):

        try:
            token = context['token']
            volume_uuid = context['resource_uuid']
            source_ip = context.get('source_ip')

            volume_uuid = parameter_check(volume_uuid, ptype='pstr')
            source_ip = parameter_check(source_ip, ptype='pnip', exist='no')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.clouddisk_manager.volume_reclaim_recovery(
                    volume_uuid, token=token, source_ip=source_ip,
                    resource_uuid=volume_uuid)
