#!/usr/bin/env python

import sys
from time import sleep

sys.path.insert(1, '../..')

from storage.manager import clouddisk_manager


def volume_physical_delete(volume_uuid, token, source_ip):

    disk_manager = clouddisk_manager.CloudDiskManager()

    return disk_manager.volume_physical_delete(
                        volume_uuid, token=token,
                        source_ip=source_ip,
                        resource_uuid=volume_uuid)


if __name__ == '__main__':

    volume_uuid = 'c6f08f21-2948-4f01-be76-05f0b212e909'
    token = '9fa96105-3711-486c-add0-df868a6eaca9'
    source_ip = '10.10.10.11'

    print volume_physical_delete(volume_uuid, token, source_ip)
