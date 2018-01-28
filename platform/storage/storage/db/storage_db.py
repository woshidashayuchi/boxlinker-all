# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import json

from common.mysql_base import MysqlInit
from common.logs import logging as log


class StorageDB(MysqlInit):

    def __init__(self):

        super(StorageDB, self).__init__()

    def cluster_name_check(self, cluster_name):

        sql = "select count(*) from ceph_clusters where cluster_name='%s'" \
               % (cluster_name)

        return super(StorageDB, self).exec_select_sql(sql)

    def ceph_cluster_create(self, cluster_uuid, cluster_name,
                            cluster_auth, service_auth, client_auth,
                            ceph_pgnum, ceph_pgpnum,
                            public_network, cluster_network,
                            osd_full_ratio, osd_nearfull_ratio,
                            journal_size, ntp_server):

        sql = "insert into ceph_clusters(cluster_uuid, cluster_name, \
               cluster_auth, service_auth, client_auth, ceph_pgnum, \
               ceph_pgpnum, public_network, cluster_network, \
               osd_full_ratio, osd_nearfull_ratio, journal_size, \
               ntp_server, create_time, update_time) \
               values('%s', '%s', '%s', '%s', '%s', '%s', '%s', \
               '%s', '%s', '%s', '%s', '%s', '%s', now(), now())" \
              % (cluster_uuid, cluster_name, cluster_auth or 'none',
                 service_auth or 'none', client_auth or 'none',
                 ceph_pgnum or 300, ceph_pgpnum or 300,
                 public_network or '192.168.1.0/24',
                 cluster_network or '10.10.1.0/24',
                 osd_full_ratio or '.85', osd_nearfull_ratio or '.70',
                 journal_size, ntp_server)

        return super(StorageDB, self).exec_update_sql(sql)

    def ceph_cluster_info(self, cluster_uuid):

        sql = "select cluster_uuid, cluster_name, cluster_auth, \
               service_auth, client_auth, ceph_pgnum, ceph_pgpnum, \
               public_network, cluster_network, osd_full_ratio, \
               osd_nearfull_ratio, journal_size, ntp_server, \
               create_time, update_time \
               from ceph_clusters where cluster_uuid='%s'" \
              % (cluster_uuid)

        return super(StorageDB, self).exec_select_sql(sql)

    def ceph_cluster_list(self):

        sql = "select cluster_uuid, cluster_name, cluster_auth, \
               service_auth, client_auth, ceph_pgnum, ceph_pgpnum, \
               public_network, cluster_network, osd_full_ratio, \
               osd_nearfull_ratio, journal_size, ntp_server, \
               create_time, update_time \
               from ceph_clusters"

        return super(StorageDB, self).exec_select_sql(sql)

    def host_check(self, host_ip):

        sql = "select count(*) from ceph_hosts where host_ip='%s'" \
              % (host_ip)

        return super(StorageDB, self).exec_select_sql(sql)

    def ceph_host_check(self, host_ip):

        sql = "select count(*) from ceph_hosts a join ceph_osds b \
               where a.host_uuid=b.host_uuid and a.host_ip='%s'" \
              % (host_ip)

        return super(StorageDB, self).exec_select_sql(sql)

    def host_create(self, host_uuid, host_name, host_ip,
                    host_cpu, host_mem, host_disk, host_nic):

        host_disk = ";".join([json.dumps(x) for x in host_disk])
        host_nic = ";".join([json.dumps(x) for x in host_nic])

        sql = "insert into ceph_hosts(host_uuid, host_name, host_ip, \
               host_cpu, host_mem, host_disk, host_nic, host_status, \
               create_time, update_time) \
               values('%s', '%s', '%s', '%s', '%s', '%s', '%s', \
               'on', now(), now())" \
              % (host_uuid, host_name, host_ip,
                 host_cpu, host_mem, host_disk, host_nic)

        return super(StorageDB, self).exec_update_sql(sql)

    def host_update(self, host_name, host_ip,
                    host_cpu, host_mem, host_disk, host_nic):

        host_disk = ";".join([json.dumps(x) for x in host_disk])
        host_nic = ";".join([json.dumps(x) for x in host_nic])

        sql = "update ceph_hosts set host_name='%s', \
               host_cpu='%s', host_mem='%s', \
               host_disk='%s', host_nic='%s', \
               host_status='on', update_time=now() \
               where host_ip='%s'" \
              % (host_name, host_cpu, host_mem,
                 host_disk, host_nic, host_ip)

        return super(StorageDB, self).exec_update_sql(sql)

    def host_uuid(self, host_ip):

        sql = "select host_uuid from ceph_hosts where host_ip='%s'" \
              % (host_ip)

        return super(StorageDB, self).exec_select_sql(sql)

    def host_delete(self, host_uuid):

        sql = "delete from ceph_hosts where host_uuid='%s'" % (host_uuid)

        return super(StorageDB, self).exec_update_sql(sql)

    def host_info(self, host_uuid):

        sql = "select host_name, host_ip, host_cpu, host_mem, \
               host_disk, host_nic, host_status, \
               create_time, update_time from ceph_hosts \
               where host_uuid='%s'" \
              % (host_uuid)

        return super(StorageDB, self).exec_select_sql(sql)

    def host_list(self, page_size, page_num):

        page_size = int(page_size)
        page_num = int(page_num)
        start_position = (page_num - 1) * page_size

        sql_01 = "select host_uuid, host_name, host_ip, \
                  host_cpu, host_mem, host_disk, host_nic, \
                  host_status, create_time, update_time \
                  from ceph_hosts limit %d,%d" \
                 % (start_position, page_size)

        sql_02 = "select count(*) from ceph_hosts"

        db_host_list = super(StorageDB, self).exec_select_sql(sql_01)
        count = super(StorageDB, self).exec_select_sql(sql_02)[0][0]

        return {
                   "host_list": db_host_list,
                   "count": count
               }

    def cephmon_check(self, host_uuid):

        sql = "select count(*) from ceph_mons where host_uuid='%s'" \
              % (host_uuid)

        return super(StorageDB, self).exec_select_sql(sql)

    def cephmon_init(self, cluster_uuid,
                     mon01_hostuuid, mon02_hostuuid,
                     mon01_uuid, mon01_id, mon01_storage_ip,
                     mon02_uuid, mon02_id, mon02_storage_ip):

        sql_01 = "insert into ceph_mons(mon_uuid, cluster_uuid, \
                  mon_id, host_uuid, storage_ip, status, \
                  create_time, update_time) \
                  values('%s', '%s', '%s', '%s', '%s', \
                  'on', now(), now())" \
                 % (mon01_uuid, cluster_uuid, mon01_id,
                    mon01_hostuuid, mon01_storage_ip)

        sql_02 = "insert into ceph_mons(mon_uuid, cluster_uuid, \
                  mon_id, host_uuid, storage_ip, status, \
                  create_time, update_time) \
                  values('%s', '%s', '%s', '%s', '%s', \
                  'on', now(), now())" \
                 % (mon02_uuid, cluster_uuid, mon02_id,
                    mon02_hostuuid, mon02_storage_ip)

        return super(StorageDB, self).exec_update_sql(sql_01, sql_02)

    def cephmon_add(self, cluster_uuid, host_uuid,
                    mon_uuid, mon_id, storage_ip):

        sql = "insert into ceph_mons(mon_uuid, cluster_uuid, \
               mon_id, host_uuid, storage_ip, status, \
               create_time, update_time) \
               values('%s', '%s', '%s', '%s', '%s', \
               'on', now(), now())" \
              % (mon_uuid, cluster_uuid, mon_id,
                 host_uuid, storage_ip)

        return super(StorageDB, self).exec_update_sql(sql)

    def mon_count(self, cluster_uuid):

        sql = "select count(*) from ceph_mons where cluster_uuid='%s'" \
              % (cluster_uuid)

        return super(StorageDB, self).exec_select_sql(sql)

    def mon_list(self, cluster_uuid):

        sql = "select a.mon_id, b.host_name, a.storage_ip \
               from ceph_mons a join ceph_hosts b \
               where a.host_uuid=b.host_uuid \
               and a.cluster_uuid='%s'" \
              % (cluster_uuid)

        return super(StorageDB, self).exec_select_sql(sql)

    def ceph_mon_info(self, mon_uuid):

        sql = "select a.cluster_uuid, a.mon_id, a.host_uuid, \
               a.storage_ip, a.status, a.create_time, a.update_time, \
               b.cluster_name, c.host_name, c.host_ip \
               from ceph_mons a join ceph_clusters b join ceph_hosts c \
               where a.cluster_uuid=b.cluster_uuid \
               and a.host_uuid=c.host_uuid \
               and a.mon_uuid='%s'" \
              % (mon_uuid)

        return super(StorageDB, self).exec_select_sql(sql)

    def ceph_mon_list(self, cluster_uuid):

        sql = "select a.mon_uuid, a.cluster_uuid, a.mon_id, a.host_uuid, \
               a.storage_ip, a.status, a.create_time, a.update_time, \
               b.cluster_name, c.host_name \
               from ceph_mons a join ceph_clusters b join ceph_hosts c \
               where a.cluster_uuid=b.cluster_uuid \
               and a.host_uuid=c.host_uuid \
               and a.cluster_uuid='%s'" \
              % (cluster_uuid)

        return super(StorageDB, self).exec_select_sql(sql)

    def cephosd_add(self, osd_uuid, cluster_uuid,
                    osd_id, host_uuid, storage_ip,
                    jour_disk, data_disk, disk_type, weight):

        sql = "insert into ceph_osds(osd_uuid, cluster_uuid, \
               osd_id, host_uuid, storage_ip, jour_disk, \
               data_disk, disk_type, weight, status, \
               create_time, update_time) \
               values('%s', '%s', '%s', '%s', '%s', '%s', \
               '%s', '%s', '%s', 'on', now(), now())" \
              % (osd_uuid, cluster_uuid, osd_id,
                 host_uuid, storage_ip, jour_disk,
                 data_disk, disk_type, weight)

        return super(StorageDB, self).exec_update_sql(sql)

    def cephosd_delete(self, osd_uuid):

        sql = "delete from ceph_osds where osd_uuid='%s'" % (osd_uuid)

        return super(StorageDB, self).exec_update_sql(sql)

    def cephosd_reweight(self, osd_uuid, weight):

        sql = "update ceph_osds set weight='%s' where osd_uuid='%s'" \
              % (weight, osd_uuid)

        return super(StorageDB, self).exec_update_sql(sql)

    def cephosd_info(self, osd_uuid):

        sql = "select a.cluster_uuid, a.osd_id, a.host_uuid, \
               a.storage_ip, a.jour_disk, a.data_disk, \
               a.disk_type, a.weight, a.status, \
               a.create_time, a.update_time, \
               b.cluster_name, c.host_name, c.host_ip \
               from ceph_osds a join ceph_clusters b join ceph_hosts c \
               where a.cluster_uuid=b.cluster_uuid \
               and a.host_uuid=c.host_uuid \
               and a.osd_uuid='%s'" \
              % (osd_uuid)

        return super(StorageDB, self).exec_select_sql(sql)

    def cephosd_list(self, cluster_uuid, page_size, page_num):

        page_size = int(page_size)
        page_num = int(page_num)
        start_position = (page_num - 1) * page_size

        sql_01 = "select a.osd_uuid, a.osd_id, a.host_uuid, a.storage_ip, \
                  a.jour_disk, a.data_disk, a.disk_type, a.weight, \
                  a.status, a.create_time, a.update_time, \
                  b.cluster_name, c.host_name, c.host_ip \
                  from ceph_osds a join ceph_clusters b join ceph_hosts c \
                  where a.cluster_uuid=b.cluster_uuid \
                  and a.host_uuid=c.host_uuid \
                  and a.cluster_uuid='%s' limit %d,%d" \
                 % (cluster_uuid, start_position, page_size)

        sql_02 = "select count(*) from ceph_osds where cluster_uuid='%s'" \
                 % (cluster_uuid)

        db_osd_list = super(StorageDB, self).exec_select_sql(sql_01)
        count = super(StorageDB, self).exec_select_sql(sql_02)[0][0]

        return {
                   "osd_list": db_osd_list,
                   "count": count
               }

    def cephpool_info(self, pool_uuid):

        sql = "select a.cluster_uuid, a.pool_name, a.pool_size, \
               a.used, a.avail, a.used_rate, a.pool_type, \
               a.create_time, a.update_time, b.cluster_name \
               from ceph_pools a join ceph_clusters b \
               where a.cluster_uuid=b.cluster_uuid \
               and a.pool_uuid='%s'" \
              % (pool_uuid)

        return super(StorageDB, self).exec_select_sql(sql)

    def cephpool_list(self, cluster_uuid):

        sql = "select a.pool_uuid, a.pool_name, a.pool_size, \
               a.used, a.avail, a.used_rate, a.pool_type, \
               a.create_time, a.update_time, b.cluster_name \
               from ceph_pools a join ceph_clusters b \
               where a.cluster_uuid=b.cluster_uuid \
               and a.cluster_uuid='%s'" \
              % (cluster_uuid)

        return super(StorageDB, self).exec_select_sql(sql)

    def osdnode_check(self, cluster_uuid, pool_type):

        sql = "select count(distinct host_uuid) from ceph_osds \
               where cluster_uuid='%s' and disk_type='%s'" \
              % (cluster_uuid, pool_type)

        return super(StorageDB, self).exec_select_sql(sql)

    def cephpool_create(self, pool_uuid, cluster_uuid,
                        pool_name, pool_size, used,
                        avail, used_rate, pool_type):

        sql = "insert into ceph_pools(pool_uuid, cluster_uuid, \
               pool_name, pool_size, used, avail, used_rate, \
               pool_type, create_time, update_time) \
               values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', \
               now(), now())" \
              % (pool_uuid, cluster_uuid, pool_name, pool_size,
                 used, avail, used_rate, pool_type)

        return super(StorageDB, self).exec_update_sql(sql)

    def cephpool_update(self, cluster_uuid, pool_size,
                        used, avail, used_rate):

        sql = "update ceph_pools set pool_size='%s', used='%s', \
               avail='%s', used_rate='%s', update_time=now() \
               where cluster_uuid='%s'" \
              % (pool_size, used, avail, used_rate, cluster_uuid)

        return super(StorageDB, self).exec_update_sql(sql)

    def name_duplicate_check(self, volume_name,
                             project_uuid, cluster_uuid):

        sql = "select count(*) from volumes a join resources_acl b \
               where a.volume_uuid=b.resource_uuid \
               and a.volume_name='%s' and a.cluster_uuid='%s' \
               and b.project_uuid='%s'" \
               % (volume_name, cluster_uuid, project_uuid)

        return super(StorageDB, self).exec_select_sql(sql)

    def volume_name(self, volume_uuid):

        sql = "select volume_name from volumes where volume_uuid='%s'" \
              % (volume_uuid)

        return super(StorageDB, self).exec_select_sql(sql)

    def volume_create(self, volume_uuid, cluster_uuid,
                      pool_name, volume_name, volume_size,
                      volume_type, disk_name, fs_type,
                      team_uuid, project_uuid, user_uuid):

        sql_01 = "insert into resources_acl(resource_uuid, resource_type, \
                  admin_uuid, team_uuid, project_uuid, user_uuid, \
                  create_time, update_time) \
                  values('%s', 'volume', '0', '%s', '%s', '%s', now(), now())" \
                  % (volume_uuid, team_uuid, project_uuid, user_uuid)

        sql_02 = "insert into volumes(volume_uuid, cluster_uuid, \
                  volume_name, volume_size, volume_type, volume_status, \
                  disk_name, fs_type, mount_point, pool_name, \
                  create_time, update_time) \
                  values('%s', '%s', '%s', '%d', '%s', 'unused', '%s', \
                  '%s', 'None', '%s', now(), now())" \
                  % (volume_uuid, cluster_uuid, volume_name,
                     int(volume_size), volume_type,
                     disk_name, fs_type, pool_name)

        return super(StorageDB, self).exec_update_sql(sql_01, sql_02)

    def volume_logical_delete(self, volume_uuid):

        sql = "update volumes set volume_status='delete', update_time=now() \
               where volume_uuid='%s' and volume_status!='delete'" \
              % (volume_uuid)

        return super(StorageDB, self).exec_update_sql(sql)

    def volume_physical_delete(self, volume_uuid):

        sql_01 = "delete from resources_acl where resource_uuid='%s'" \
                 % (volume_uuid)
        sql_02 = "delete from volumes where volume_uuid='%s'" \
                 % (volume_uuid)

        return super(StorageDB, self).exec_update_sql(sql_01, sql_02)

    def volume_resize(self, volume_uuid, volume_size):

        sql = "update volumes set volume_size='%d', update_time=now() \
               where volume_uuid='%s'" \
               % (int(volume_size), volume_uuid)

        return super(StorageDB, self).exec_update_sql(sql)

    def volume_status(self, volume_uuid, volume_status):

        sql = "update volumes set volume_status='%s', update_time=now() \
               where volume_uuid='%s'" \
               % (volume_status, volume_uuid)

        return super(StorageDB, self).exec_update_sql(sql)

    def volume_info(self, volume_uuid):

        sql = "select cluster_uuid, pool_name, volume_name, \
               volume_size, volume_type, volume_status, disk_name, \
               fs_type, mount_point, create_time, update_time \
               from volumes where volume_uuid='%s'" \
               % (volume_uuid)

        return super(StorageDB, self).exec_select_sql(sql)

    def volume_recovery(self, volume_uuid):

        sql = "update volumes set volume_status='unused', update_time=now() \
               where volume_uuid='%s' and volume_status='delete'" \
              % (volume_uuid)

        return super(StorageDB, self).exec_update_sql(sql)

    def volume_list_dead(self):

        sql = "select volume_uuid from volumes \
               where volume_status='delete' \
               and update_time<date_sub(now(), interval 30 day)"

        return super(StorageDB, self).exec_select_sql(sql)

    def volume_list_team(self, team_uuid):

        sql = "select a.volume_uuid from volumes a join resources_acl b \
               where a.volume_uuid=b.resource_uuid \
               and a.volume_status!='delete' \
               and b.team_uuid='%s'" \
              % (team_uuid)

        return super(StorageDB, self).exec_select_sql(sql)

    def volume_list_project(self, team_uuid, project_uuid,
                            cluster_uuid, page_size, page_num):

        page_size = int(page_size)
        page_num = int(page_num)
        start_position = (page_num - 1) * page_size

        sql_01 = "select a.volume_uuid, a.cluster_uuid, a.pool_name, \
                  a.volume_name, a.volume_size, a.volume_type, \
                  a.volume_status, a.disk_name, a.fs_type, a.mount_point, \
                  a.create_time, a.update_time \
                  from volumes a join resources_acl b \
                  where a.volume_uuid=b.resource_uuid \
                  and a.volume_status!='delete' \
                  and a.cluster_uuid='%s' \
                  and b.team_uuid='%s' and b.project_uuid='%s' \
                  limit %d,%d" \
                 % (cluster_uuid, team_uuid, project_uuid,
                    start_position, page_size)

        sql_02 = "select count(*) from volumes a join resources_acl b \
                  where a.volume_uuid=b.resource_uuid \
                  and a.volume_status!='delete' \
                  and a.cluster_uuid='%s' \
                  and b.team_uuid='%s' and b.project_uuid='%s'" \
                 % (cluster_uuid, team_uuid, project_uuid)

        volumes_list = super(StorageDB, self).exec_select_sql(sql_01)
        count = super(StorageDB, self).exec_select_sql(sql_02)[0][0]

        return {
                   "volumes_list": volumes_list,
                   "count": count
               }

    def volume_list_user(self, team_uuid, project_uuid,
                         user_uuid, cluster_uuid,
                         page_size, page_num):

        page_size = int(page_size)
        page_num = int(page_num)
        start_position = (page_num - 1) * page_size

        sql_01 = "select a.volume_uuid, a.cluster_uuid, a.pool_name, \
                  a.volume_name, a.volume_size, a.volume_type, \
                  a.volume_status, a.disk_name, a.fs_type, a.mount_point, \
                  a.create_time, a.update_time \
                  from volumes a join resources_acl b \
                  where a.volume_uuid=b.resource_uuid \
                  and a.volume_status!='delete' \
                  and a.cluster_uuid='%s' \
                  and b.team_uuid='%s' and b.project_uuid='%s' \
                  and b.user_uuid='%s' \
                  limit %d,%d" \
                 % (cluster_uuid, team_uuid, project_uuid,
                    user_uuid, start_position, page_size)

        sql_02 = "select count(*) from volumes a join resources_acl b \
                  where a.volume_uuid=b.resource_uuid \
                  and a.volume_status!='delete' \
                  and a.cluster_uuid='%s' \
                  and b.team_uuid='%s' and b.project_uuid='%s' \
                  and b.user_uuid='%s'" \
                 % (cluster_uuid, team_uuid, project_uuid, user_uuid)

        volumes_list = super(StorageDB, self).exec_select_sql(sql_01)
        count = super(StorageDB, self).exec_select_sql(sql_02)[0][0]

        return {
                   "volumes_list": volumes_list,
                   "count": count
               }

    def volume_reclaim_list_project(self, team_uuid, project_uuid,
                                    page_size, page_num):

        page_size = int(page_size)
        page_num = int(page_num)
        start_position = (page_num - 1) * page_size

        sql_01 = "select a.volume_uuid, a.cluster_uuid, a.pool_name, \
                  a.volume_name, a.volume_size, a.volume_type, \
                  a.volume_status, a.disk_name, a.fs_type, a.mount_point, \
                  a.create_time, a.update_time, c.cluster_name \
                  from volumes a join resources_acl b join ceph_clusters c \
                  where a.volume_uuid=b.resource_uuid \
                  and a.cluster_uuid=c.cluster_uuid \
                  and a.volume_status='delete' \
                  and b.team_uuid='%s' and b.project_uuid='%s' \
                  limit %d,%d" \
                 % (team_uuid, project_uuid,
                    start_position, page_size)

        sql_02 = "select count(*) from volumes a join resources_acl b \
                  where a.volume_uuid=b.resource_uuid \
                  and a.volume_status='delete' \
                  and b.team_uuid='%s' and b.project_uuid='%s'" \
                 % (team_uuid, project_uuid)

        volumes_list = super(StorageDB, self).exec_select_sql(sql_01)
        count = super(StorageDB, self).exec_select_sql(sql_02)[0][0]

        return {
                   "volumes_list": volumes_list,
                   "count": count
               }

    def volume_reclaim_list_user(self, team_uuid, project_uuid,
                                 user_uuid, page_size, page_num):

        page_size = int(page_size)
        page_num = int(page_num)
        start_position = (page_num - 1) * page_size

        sql_01 = "select a.volume_uuid, a.cluster_uuid, a.pool_name, \
                  a.volume_name, a.volume_size, a.volume_type, \
                  a.volume_status, a.disk_name, a.fs_type, a.mount_point, \
                  a.create_time, a.update_time, c.cluster_name \
                  from volumes a join resources_acl b join ceph_clusters c \
                  where a.volume_uuid=b.resource_uuid \
                  and a.cluster_uuid=c.cluster_uuid \
                  and a.volume_status='delete' \
                  and b.team_uuid='%s' and b.project_uuid='%s' \
                  and b.user_uuid='%s' \
                  limit %d,%d" \
                 % (team_uuid, project_uuid, user_uuid,
                    start_position, page_size)

        sql_02 = "select count(*) from volumes a join resources_acl b \
                  where a.volume_uuid=b.resource_uuid \
                  and a.volume_status='delete' \
                  and b.team_uuid='%s' and b.project_uuid='%s' \
                  and b.user_uuid='%s'" \
                 % (team_uuid, project_uuid, user_uuid)

        volumes_list = super(StorageDB, self).exec_select_sql(sql_01)
        count = super(StorageDB, self).exec_select_sql(sql_02)[0][0]

        return {
                   "volumes_list": volumes_list,
                   "count": count
               }

    def volume_add_list(self):

        sql = "select a.volume_uuid, a.volume_name, a.volume_size, \
               a.volume_status, b.resource_type, b.team_uuid, \
               b.project_uuid, b.user_uuid from volumes a \
               join resources_acl b where a.volume_uuid=b.resource_uuid \
               and a.create_time>=date_sub(now(), interval 24 hour)"

        return super(StorageDB, self).exec_select_sql(sql)

    def volume_delete_list(self):

        sql = "select volume_uuid from volumes \
               where volume_status='delete' \
               and update_time>=date_sub(now(), interval 24 hour)"

        return super(StorageDB, self).exec_select_sql(sql)

    def volume_update_list(self):

        sql = "select a.volume_uuid, a.volume_name, a.volume_size, \
               a.volume_status, b.resource_type, b.team_uuid, \
               b.project_uuid, b.user_uuid from volumes a \
               join resources_acl b where a.volume_uuid=b.resource_uuid \
               and a.volume_status!='delete' \
               and  a.update_time>=date_sub(now(), interval 24 hour)"

        return super(StorageDB, self).exec_select_sql(sql)
