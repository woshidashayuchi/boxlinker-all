#!/usr/bin/env python

import sys
from time import sleep

sys.path.insert(1, '../..')

from ceph.manager import host_manager


def test_host_info(host_ip, rootpwd):

    node_manager = host_manager.HostManager()

    return node_manager.host_info(host_ip, rootpwd)


if __name__ == '__main__':

    host_ip = '192.168.1.9'
    rootpwd = 'boxlinker'

    print test_host_info(host_ip, rootpwd)
