#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pexpect

from common.logs import logging as log
from common.shellexec import execute


def remote_sshexec_cmd(remote_ip, user_name, password, cmd):

    try:
        ssh = pexpect.spawn('ssh -o StrictHostKeyChecking=no %s@%s "%s"'
                            % (user_name, remote_ip, cmd))
        i = ssh.expect(['password: '], timeout=5)
        if i == 0:
            ssh.sendline(password)
            ii = ssh.expect(['password: '])
            if ii == 0:
                ssh.close()
                return 3
        ssh.close()
        return 0
    except pexpect.EOF:
        ssh.close()
        return 1
    except pexpect.TIMEOUT:
        ssh.close()
        return 2
    except Exception, e:
        return 5


def ssh_key_create():

    cmd = "ssh-keygen -t dsa -P '' -f /root/.ssh/id_dsa &> /dev/null"

    result = execute(cmd, shell=True, run_as_root=True)[1]
    if str(result) != '0':
        log.error('SSH key create failure')
        return 1
    else:
        return 0


def ssh_key_conf(remote_ip, user_name, password):

    # 生成ssh-key文件
    if not os.path.isfile('/root/.ssh/id_dsa.pub'):
        key_create = ssh_key_create()
        if key_create != 0:
            return 5

    # 将id_dsa.pub拷贝到远程主机
    try:
        ssh = pexpect.spawn('ssh-copy-id -i /root/.ssh/id_dsa.pub'
                            ' -o StrictHostKeyChecking=no %s@%s'
                            % (user_name, remote_ip))
        i = ssh.expect(['password: '], timeout=5)
        if i == 0:
            ssh.sendline(password)
            ii = ssh.expect(['password: '])
            if ii == 0:
                log.error('SSH key conf failure, password incorrect.')
                ssh.close()
                return 1
        ssh.close()
        return 0
    except pexpect.EOF:
        ssh.close()
        return 0
    except pexpect.TIMEOUT:
        ssh.close()
        log.error('SSH key conf failure, connect timeout.')
        return 2
    except Exception, e:
        log.error('SSH key conf failure, reason=%s' % (e))
        return 5


if __name__ == '__main__':

    user_name = 'root'
    remote_ip = sys.argv[1]
    password = sys.argv[2]

    print ssh_key_conf(remote_ip, user_name, password)
