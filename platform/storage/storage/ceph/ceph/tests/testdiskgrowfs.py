#!/usr/bin/env python

import sys

sys.path.insert(1, '../..')

from common.logs import logging as log
from common.shellexec import execute
from common.code import request_result


def disk_growfs(image_name):

    cmd = "df -h | grep '%s' | awk '{print $1}'" % (image_name)
    dev_info = execute(cmd, shell=True, run_as_root=True)[0][0].strip('\n')
    print dev_info.split('\n')
    for dev_name in dev_info.split('\n'):
        if dev_name:
            cmd = "xfs_growfs %s" % (dev_name)
            result = execute(cmd, shell=True, run_as_root=True)[1]
            if str(result) != '0':
                log.error('Ceph disk(%s) growfs failure' % (image_name))
                return request_result(513)
            else:
                return request_result(0)

    return


if __name__ == '__main__':

    image_name = 'test01'

    print disk_growfs(image_name)
