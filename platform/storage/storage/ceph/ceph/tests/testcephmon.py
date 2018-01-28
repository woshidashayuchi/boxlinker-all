#!/usr/bin/env python

import sys
from time import sleep

sys.path.insert(1, '../..')

from ceph.manager import cephmon_manager


def test_mon_init(cluster_info,
                  mon01_hostip, mon01_rootpwd, mon01_snic,
                  mon02_hostip, mon02_rootpwd, mon02_snic):

    mon_manager = cephmon_manager.CephMonManager()

    return mon_manager.cephmon_init(
                       cluster_info,
                       mon01_hostip, mon01_rootpwd, mon01_snic,
                       mon02_hostip, mon02_rootpwd, mon02_snic)

def test_mon_add(cluster_info, mon_id, host_ip,
                 rootpwd, storage_nic, mon_list):

    mon_manager = cephmon_manager.CephMonManager()

    return mon_manager.cephmon_add(
                       cluster_info, mon_id,
                       host_ip, rootpwd,
                       storage_nic, mon_list)


if __name__ == '__main__':

    action = sys.argv[1]

    if action == 'mon_init':

        cluster_info = None
        mon01_hostip = '10.10.10.21'
        mon01_rootpwd = 'kvmcenter'
        mon01_snic = 'eno33554960'
        mon02_hostip = '10.10.10.22'
        mon02_rootpwd = 'kvmcenter'
        mon02_snic = 'eno33554960'

        print test_mon_init(cluster_info, mon01_hostip,
                            mon01_rootpwd, mon01_snic,
                            mon02_hostip, mon02_rootpwd,
                            mon02_snic)

    elif action == 'mon_add':

        cluster_info = {
                           "cluster_uuid": 'xxx',
                           "cluster_auth": 'none',
                           "service_auth": 'none',
                           "client_auth": 'none',
                           "ceph_pgnum": 300,
                           "ceph_pgpnum": 300,
                           "public_network": '192.168.1.0/24',
                           "cluster_network": '10.10.1.0/24',
                           "osd_full_ratio": '.85',
                           "osd_nearfull_ratio": '.70',
                           "journal_size": 5000
                       }

        mon_id = 'mon.3'
        host_ip = '10.10.10.23'
        rootpwd = 'kvmcenter'
        storage_nic = 'eno33554960'

        print test_mon_add(cluster_info, mon_id,
                           host_ip, rootpwd, storage_nic,
                           mon_list=None)
