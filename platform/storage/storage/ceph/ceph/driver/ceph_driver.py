#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import os

from common.logs import logging as log
from common.shellexec import execute
from common.code import request_result
from common.ssh_key_conf import ssh_key_conf


class CephDriver(object):

    def __init__(self):

        self.ceph_conf_path = '/tmp/ceph/conf'
        self.ceph_conf_file = '/etc/ceph/ceph.conf'
        self.ceph_dirname = os.path.dirname(
                                os.path.dirname(
                                    os.path.dirname(
                                        os.path.dirname(
                                            os.path.abspath(__file__)))))

    def host_ping_check(self, host_ip):

        cmd = "ping -c 3 -w 3 '%s' | grep -w 'ttl' | wc -l" \
              % (host_ip)

        return execute(cmd, shell=True, run_as_root=True)[0][0].strip('\n')

    def host_ssh_conf(self, host_ip, password, user_name='root'):

        return ssh_key_conf(host_ip, user_name, password)

    def host_ssh_del(self, host_ip, control_host_name):

        cmd = ("ssh -o StrictHostKeyChecking=no root@'%s' "
               "'sed -i '/%s/d' /root/.ssh/authorized_keys'"
               % (host_ip, control_host_name))

        return execute(cmd, shell=True, run_as_root=True)[1]

    def remote_host_name(self, host_ip):

        cmd = "ssh -o StrictHostKeyChecking=no root@'%s' 'hostname'" \
              % (host_ip)

        return execute(cmd, shell=True, run_as_root=True)[0][0].strip('\n')

    def remote_host_cpu(self, host_ip):

        cmd = ("ssh -o StrictHostKeyChecking=no root@'%s' "
               "'cat '/proc/cpuinfo' | grep -w 'processor' | wc -l'"
               % (host_ip))

        return execute(cmd, shell=True, run_as_root=True)[0][0].strip('\n')

    def remote_host_mem(self, host_ip):

        cmd = ("ssh -o StrictHostKeyChecking=no root@'%s' "
               "'free -m' | grep -w 'Mem' | awk '{print $2/1024}'"
               % (host_ip))

        return execute(cmd, shell=True, run_as_root=True)[0][0].strip('\n')

    def remote_host_disk(self, host_ip):

        cmd = ("ssh -o StrictHostKeyChecking=no root@'%s' "
               "'fdisk -l' | egrep '^/dev/(sd|vd)' "
               "| grep -v '*' | awk '{print $1, $4}'"
               % (host_ip))

        return execute(cmd, shell=True, run_as_root=True)[0][0].strip('\n')

    def remote_host_nic_name(self, host_ip):

        cmd = ("ssh -o StrictHostKeyChecking=no root@'%s' "
               "'ip addr' | grep -w 'mtu' | grep -v 'br' "
               "| grep -v 'lo' | grep -v 'vlan' | awk -F: '{print $2}'"
               % (host_ip))

        return execute(cmd, shell=True, run_as_root=True)[0][0].strip('\n')

    def remote_host_nic_info(self, host_ip, nic_name):

        cmd = ("ssh -o StrictHostKeyChecking=no root@'%s' "
               "'ip addr show '%s'' | egrep -w '(ether|inet)' "
               "| awk '{print $2}'"
               % (host_ip, nic_name))

        return execute(cmd, shell=True, run_as_root=True)[0][0].strip('\n')

    def local_host_name(self):

        cmd = "hostname"

        return execute(cmd, shell=True, run_as_root=True)[0][0].strip('\n')

    def storage_ip(self, host_ip, storage_nic):

        cmd = ("ssh -o StrictHostKeyChecking=no root@'%s'"
               " 'ip addr | grep %s' | grep -w 'inet' "
               "| awk '{print $2}' | awk -F/ '{print $1}'"
               % (host_ip, storage_nic))

        return execute(cmd, shell=True, run_as_root=True)[0][0].strip('\n')

    def ceph_conf_init(self, cluster_uuid, cluster_auth,
                       service_auth, client_auth, ceph_pgnum,
                       ceph_pgpnum, public_network, cluster_network,
                       osd_full_ratio, osd_nearfull_ratio, journal_size):

        data = ["[global]\n",
                "\n",
                "auth cluster required = %s\n" % (cluster_auth),
                "auth service required = %s\n" % (service_auth),
                "auth client required = %s\n" % (client_auth),
                "\n",
                "fsid = %s\n" % (cluster_uuid),
                "\n",
                "log file = /var/log/ceph/$name.log\n",
                "pid file = /var/run/ceph/$name.pid\n",
                "\n",
                "osd pool default size = 3\n",
                "osd pool default min size = 2\n",
                "osd pool default pg num = %s\n" % (ceph_pgnum),
                "osd pool default pgp num = %s\n" % (ceph_pgpnum),
                "\n",
                "#    public network = %s\n" % (public_network),
                "#    cluster network = %s\n" % (cluster_network),
                "\n",
                "mon osd full ratio = %s\n" % (osd_full_ratio),
                "mon osd nearfull ratio = %s\n" % (osd_nearfull_ratio),
                "\n",
                "[mon]\n",
                "mon data = /ceph/mondata/mon$host\n",
                "\n",
                "#[mon.1]\n",
                "\n",
                "#[mon.2]\n",
                "\n",
                "#[mon.3]\n",
                "\n",
                "#[mon.4]\n",
                "\n",
                "#[mon.5]\n",
                "\n",
                "#[mds.1]\n",
                "\n",
                "#[mds.2]\n",
                "\n",
                "#[mds.3]\n"
                "\n",
                "#[mds.4]\n",
                "\n",
                "#[mds.5]\n",
                "\n",
                "[osd]\n",
                "osd data = /data/osd$id\n",
                "osd journal = /ceph/journal/osd$id/journal\n",
                "osd journal size = %s\n" % (journal_size),
                "osd mkfs type = xfs\n",
                "osd mkfs options xfs = -f\n",
                "osd mount options xfs = rw,noatime\n",
                "\n"]

        cmd = "mkdir -p %s" % (self.ceph_conf_path)
        execute(cmd, shell=True, run_as_root=True)

        self.ceph_conf = "%s/%s.conf" % (self.ceph_conf_path, cluster_uuid)
        with open(self.ceph_conf, 'w') as f:
            f.writelines(data)

    def ceph_conf_check(self, cluster_uuid):

        self.ceph_conf = "%s/%s.conf" % (self.ceph_conf_path, cluster_uuid)
        if os.path.isfile(self.ceph_conf):
            return True
        else:
            return False

    def mon_conf_update(self, cluster_uuid, cephmon_id,
                        mon_host_name, mon_storage_ip):

        self.ceph_conf = "%s/%s.conf" % (self.ceph_conf_path, cluster_uuid)

        mon_id = 'mon.%s' % (cephmon_id)
        mds_id = 'mds.%s' % (cephmon_id)

        cmd_01 = "sed -i '/%s/d' %s" % (mon_host_name, self.ceph_conf)
        cmd_02 = "sed -i '/%s/d' %s" % (mon_storage_ip, self.ceph_conf)
        execute(cmd_01, shell=True, run_as_root=True)
        execute(cmd_02, shell=True, run_as_root=True)

        cmd = "cat %s | grep -n '%s' | awk -F: '{print $1}'" \
              % (self.ceph_conf, mon_id)
        mon_line = execute(cmd, shell=True, run_as_root=True)[0][0].strip('\n')
        edit_line = int(mon_line) + 1

        cmd_01 = "sed -i '%si\    mon addr = %s:5000' %s" \
                 % (edit_line, mon_storage_ip, self.ceph_conf)
        cmd_02 = "sed -i '%si\    host = %s' %s" \
                 % (edit_line, mon_host_name, self.ceph_conf)
        cmd_03 = "sed -i '%si\[mon.%s]' %s" \
                 % (edit_line, mon_host_name, self.ceph_conf)

        execute(cmd_01, shell=True, run_as_root=True)
        execute(cmd_02, shell=True, run_as_root=True)
        execute(cmd_03, shell=True, run_as_root=True)

        cmd = "cat %s | grep -n '%s' | awk -F: '{print $1}'" \
              % (self.ceph_conf, mds_id)
        mds_line = execute(cmd, shell=True, run_as_root=True)[0][0].strip('\n')
        edit_line = int(mds_line) + 1

        cmd_01 = "sed -i '%si\    host = %s' %s" \
                 % (edit_line, mon_host_name, self.ceph_conf)
        cmd_02 = "sed -i '%si\[mds.%s]' %s" \
                 % (edit_line, mon_host_name, self.ceph_conf)

        execute(cmd_01, shell=True, run_as_root=True)
        execute(cmd_02, shell=True, run_as_root=True)

    def conf_dist(self, cluster_uuid, host_ip):

        self.ceph_conf = "%s/%s.conf" % (self.ceph_conf_path, cluster_uuid)

        cmd = "scp %s root@'%s':%s &> /dev/null" \
              % (self.ceph_conf, host_ip, self.ceph_conf_file)

        return execute(cmd, shell=True, run_as_root=True)[1]

    def monmap_init(self, mon01_hostname, mon01_storage_ip,
                    mon02_hostname, mon02_storage_ip,
                    mon01_hostip, cluster_uuid):

        cmd = ("ssh -o StrictHostKeyChecking=no root@'%s' "
               "'rm -rf /tmp/monmap; "
               "monmaptool --create --add %s %s:5000 "
               "--add %s %s:5000 --fsid %s /tmp/monmap'"
               % (mon01_hostip, mon01_hostname, mon01_storage_ip,
                  mon02_hostname, mon02_storage_ip, cluster_uuid))

        return execute(cmd, shell=True, run_as_root=True)[1]

    def monmap_sync(self, source_ip, dest_ip):

        cmd_01 = "scp root@'%s':/tmp/monmap /tmp/" % (source_ip)
        cmd_02 = "scp /tmp/monmap root@'%s':/tmp/" % (dest_ip)

        result01 = execute(cmd_01, shell=True, run_as_root=True)[1]
        result02 = execute(cmd_02, shell=True, run_as_root=True)[1]
        if (int(result01) == 0) and (int(result02) == 0):
            return 0
        else:
            return 1

    def host_ntp_conf(self, host_ip, ntp_server):

        cmd = ("sed -i '/ntpdate/d' /etc/crontab; "
               "echo '0 * * * * root /usr/sbin/ntpdate %s &> /dev/null' >> /etc/crontab; "
               "scp /etc/crontab root@'%s':/etc/"
               % (ntp_server, host_ip))

        return execute(cmd, shell=True, run_as_root=True)[1]

    def mon_host_init(self, mon_host_name, mon_host_ip):

        cmd = ("ssh -o StrictHostKeyChecking=no root@'%s' "
               "'mkdir -p /ceph/mondata; "
               "ceph-mon --mkfs -i %s --monmap /tmp/monmap; "
               "systemctl stop firewalld.service; "
               "systemctl disable firewalld.service; "
               "chkconfig ceph on; service ceph start'"
               % (mon_host_ip, mon_host_name))

        return execute(cmd, shell=True, run_as_root=True)[1]

    def crush_ssd_add(self, mon_hostip):

        cmd = "ssh -o StrictHostKeyChecking=no root@'%s' \
               'ceph osd crush add-bucket ssd root'" \
              % (mon_hostip)

        return execute(cmd, shell=True, run_as_root=True)[1]

    def mon_host_add(self, mon_host_name, mon_host_ip, storage_ip):

        cmd = ("ssh -o StrictHostKeyChecking=no root@'%s' "
               "'mkdir -p /ceph/mondata; "
               "mkdir -p /tmp/ceph; "
               "ceph mon getmap -o /tmp/ceph/monmap; "
               "ceph-mon --mkfs -i %s --monmap /tmp/ceph/monmap; "
               "ceph mon add %s %s:5000; "
               "systemctl stop firewalld.service; "
               "systemctl disable firewalld.service; "
               "chkconfig ceph on; service ceph start'"
               % (mon_host_ip, mon_host_name,
                  mon_host_name, storage_ip))

        return execute(cmd, shell=True, run_as_root=True)[1]

    def ceph_service_install(self, mon_host_ip, cluster_uuid):

        cmd_01 = "scp -r %s/ceph root@'%s':/" \
                 % (self.ceph_dirname, mon_host_ip)

        cmd_02 = ("cp %s/ceph/conf/conf.py /tmp/%s_conf.py; "
                  "sed -i 's/ceph_call_queue = .*/ceph_call_queue = \"%s\"/g' /tmp/%s_conf.py; "
                  "scp /tmp/%s_conf.py root@'%s':/ceph/conf/conf.py"
                  % (self.ceph_dirname, cluster_uuid,
                     cluster_uuid, cluster_uuid,
                     cluster_uuid, mon_host_ip))

        cmd_03 = ("ssh -o StrictHostKeyChecking=no root@'%s' "
                  "'cp /ceph/ceph_service /etc/init.d/; "
                  "chmod 755 /etc/init.d/ceph_service; "
                  "chkconfig ceph_service on; service ceph_service start'"
                  % (mon_host_ip))

        result01 = execute(cmd_01, shell=True, run_as_root=True)[1]
        result02 = execute(cmd_02, shell=True, run_as_root=True)[1]
        result03 = execute(cmd_03, shell=True, run_as_root=True)[1]
        if (int(result01) == 0) and (int(result02) == 0) \
           and (int(result03) == 0):
            return 0
        else:
            return 1

    def ceph_growfs_install(self, cluster_uuid, host_ip):

        cmd_01 = "scp -r %s/ceph root@'%s':/" \
                 % (self.ceph_dirname, host_ip)

        cmd_02 = ("cp %s/ceph/conf/conf.py /tmp/%s_conf.py; "
                  "sed -i 's/ceph_exchange_name = .*/ceph_exchange_name = \"%s\"/g' /tmp/%s_conf.py; "
                  "scp /tmp/%s_conf.py root@'%s':/ceph/conf/conf.py"
                  % (self.ceph_dirname, cluster_uuid,
                     cluster_uuid, cluster_uuid,
                     cluster_uuid, host_ip))

        cmd_03 = ("ssh -o StrictHostKeyChecking=no root@'%s' "
                  "'cp /ceph/ceph_bcast /etc/init.d/; "
                  "chmod 755 /etc/init.d/ceph_bcast; "
                  "chkconfig ceph_bcast on; service ceph_bcast start'"
                  % (host_ip))

        result01 = execute(cmd_01, shell=True, run_as_root=True)[1]
        result02 = execute(cmd_02, shell=True, run_as_root=True)[1]
        result03 = execute(cmd_03, shell=True, run_as_root=True)[1]
        if (int(result01) == 0) and (int(result02) == 0) \
           and (int(result03) == 0):
            return 0
        else:
            return 1

    def pool_check(self, pool_name):

        cmd = "ceph df | grep %s | wc -l" % (pool_name)

        return execute(cmd, shell=True, run_as_root=True)[0][0].strip('\n')

    def ceph_status_check(self):

        cmd = "ceph -s | grep 'HEALTH_OK' | wc -l"

        return execute(cmd, shell=True, run_as_root=True)[0][0].strip('\n')

    def pool_disk_check(self):

        cmd = "ceph df | wc -l"

        return execute(cmd, shell=True, run_as_root=True)[0][0].strip('\n')

    def pool_ssd_create(self, pool_name):

        cmd_01 = "ceph osd crush rule create-simple ssd ssd host"
        cmd_02 = "ceph osd crush rule dump ssd | grep 'ruleset' | awk '{print $2}' | awk -F, '{print $1}'"

        result01 = execute(cmd_01, shell=True, run_as_root=True)[1]
        rule = execute(cmd_02, shell=True, run_as_root=True)[0][0].strip('\n')

        cmd_03 = "rados mkpool %s 6 %s" % (pool_name, rule)

        result02 = execute(cmd_03, shell=True, run_as_root=True)[1]
        if (int(result01) == 0) and (int(result02) == 0):
            return 0
        else:
            return 1

    def pool_hdd_create(self, pool_name):

        cmd = "rados mkpool %s" % (pool_name)

        return execute(cmd, shell=True, run_as_root=True)[1]

    def pool_info_get(self):

        cmd = "ceph df | awk 'NR==3 {print $1, $2, $3, $4}'"

        return execute(cmd, shell=True, run_as_root=True)[0][0].strip('\n')

    def pool_used(self):

        cmd = "ceph df | awk 'NR==3 {print $4}'"

        return execute(cmd, shell=True, run_as_root=True)[0][0].strip('\n')

    def osd_add(self, host_ip, host_name, jour_disk,
                data_disk, disk_type, osd_id, weight):

        cmd = ("ssh -o StrictHostKeyChecking=no root@'%s' "
               "'if [ ! -b %s ] || [ ! -b %s ]; then exit 1; fi; "
               "mkdir -p /ceph/journal/osd%s; "
               "mkdir -p /data/osd%s; "
               "mkfs.xfs -f %s; "
               "mkfs.xfs -f %s; "
               "mount %s /ceph/journal/osd%s; "
               "mount %s /data/osd%s; "
               "echo '%s               /ceph/journal/osd%s           xfs     defaults   0 0' >> /etc/fstab; "
               "systemctl stop firewalld.service; "
               "systemctl disable firewalld.service; "
               "ceph-osd -i %s --mkfs --mkkey; "
               "ceph auth add osd.%s osd 'allow *' mon 'allow rwx' -i /data/osd%s/keyring; "
               "ceph osd crush add osd.%s %s root=%s; "
               "chkconfig ceph on; service ceph start; "
               "ceph osd crush move %s root=%s; "
               "ceph osd crush reweight osd.%s %s'"
               % (host_ip, jour_disk, data_disk,
                  osd_id, osd_id, jour_disk, data_disk,
                  jour_disk, osd_id, data_disk, osd_id,
                  jour_disk, osd_id, osd_id, osd_id, osd_id,
                  osd_id, weight, disk_type, host_name,
                  disk_type, osd_id, weight))

        return execute(cmd, shell=True, run_as_root=True)[1]

    def osd_reweight(self, osd_id, weight):

        cmd = "ceph osd crush reweight osd.%s %s" % (osd_id, weight)

        return execute(cmd, shell=True, run_as_root=True)[1]

    def osd_in(self, host_ip, osd_id):

        cmd = "ssh -o StrictHostKeyChecking=no root@'%s' 'ceph osd in %s'" \
              % (host_ip, osd_id)

        return execute(cmd, shell=True, run_as_root=True)[1]

    def osd_out(self, osd_id):

        cmd = "ceph osd out %s" % (osd_id)

        return execute(cmd, shell=True, run_as_root=True)[1]

    def osd_stop(self, host_ip, osd_id):

        cmd = ("ssh -o StrictHostKeyChecking=no root@'%s' "
               "'/etc/init.d/ceph stop osd.%s'"
               % (host_ip, osd_id))

        return execute(cmd, shell=True, run_as_root=True)[1]

    def osd_crush_out(self, osd_id):

        cmd = ("ceph osd crush remove osd.%s; "
               "ceph auth del osd.%s; "
               "ceph osd rm %s"
               % (osd_id, osd_id, osd_id))

        return execute(cmd, shell=True, run_as_root=True)[1]

    def osd_host_del(self, host_ip, osd_id):

        cmd = ("ssh -o StrictHostKeyChecking=no root@'%s' "
               "'sed -i '/osd%s/d' /etc/fstab; "
               "umount /ceph/journal/osd%s; "
               "umount /data/osd%s; "
               "rm -rf /ceph/journal/osd%s; "
               "rm -rf /data/osd%s'"
               % (host_ip, osd_id, osd_id, osd_id, osd_id, osd_id))

        return execute(cmd, shell=True, run_as_root=True)[1]

    def osd_conf_add(self, cluster_uuid,
                     host_name, data_disk, osd_id):

        self.ceph_conf = "%s/%s.conf" % (self.ceph_conf_path, cluster_uuid)
        cmd_01 = "echo '[osd.%s]' >> %s" % (osd_id, self.ceph_conf)
        cmd_02 = "echo '    host = %s' >> %s" % (host_name, self.ceph_conf)
        cmd_03 = "echo '    devs = %s' >> %s" % (data_disk, self.ceph_conf)

        execute(cmd_01, shell=True, run_as_root=True)
        execute(cmd_02, shell=True, run_as_root=True)
        execute(cmd_03, shell=True, run_as_root=True)

    def disk_use_check(self, host_ip, disk_name):

        cmd = ("ssh -o StrictHostKeyChecking=no root@'%s' "
               "'df -h | grep '%s' | wc -l'"
               % (host_ip, disk_name))

        return execute(cmd, shell=True, run_as_root=True)[0][0].strip('\n')

    def osd_id_create(self):

        cmd = "ceph osd create"

        return execute(cmd, shell=True, run_as_root=True)[0][0].strip('\n')

    def disk_create(self, pool_name, disk_name, disk_size):

        cmd = "rbd create %s/%s --image-format 2 --size %s" \
              % (pool_name, disk_name, disk_size)

        result = execute(cmd, shell=True, run_as_root=True)[1]
        if str(result) != '0':
            log.error('Ceph disk(%s) create failure' % (disk_name))
            return request_result(511)
        else:
            return request_result(0)

    def disk_delete(self, pool_name, disk_name):

        cmd = "rbd rm %s/%s" % (pool_name, disk_name)

        result = execute(cmd, shell=True, run_as_root=True)[1]
        if str(result) != '0':
            log.error('Ceph disk(%s) delete failure' % (disk_name))
            return request_result(512)
        else:
            return request_result(0)

    def disk_resize(self, pool_name, disk_name, disk_size):

        cmd = "rbd resize --size %s %s/%s" \
              % (disk_size, pool_name, disk_name)

        result = execute(cmd, shell=True, run_as_root=True)[1]
        if str(result) != '0':
            log.error('Ceph disk(%s) resize failure' % (disk_name))
            return request_result(513)
        else:
            return request_result(0)

    def disk_growfs(self, image_name, fs_type):

        cmd = "df -h | grep '%s' | awk '{print $1}'" % (image_name)
        dev_info = execute(cmd, shell=True, run_as_root=True)[0][0].strip('\n')
        for dev_name in dev_info.split('\n'):
            if dev_name:
                if fs_type == 'xfs':
                    cmd = "xfs_growfs %s" % (dev_name)
                elif fs_type == 'ext4':
                    cmd = "resize2fs %s" % (dev_name)
                else:
                    return request_result(101)

                result = execute(cmd, shell=True, run_as_root=True)[1]
                if str(result) != '0':
                    log.error('Ceph disk(%s) growfs failure' % (image_name))
                    return request_result(513)
                else:
                    return request_result(0)

        return request_result(0)
