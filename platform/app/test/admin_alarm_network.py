# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 17/5/16 下午1:21

import re
import os


# get SNMP-MIB2 of the devices
def get_all_items(host,oid):
        sn1 = os.popen('snmpwalk -v 2c -c public ' + host + ' ' + oid).read().split('\n')[:-1]
        return sn1


# get network device
def get_devices(host):
        device_mib = get_all_items(host, 'RFC1213-MIB::ifDescr')
        device_list = []
        for item in device_mib:
                if re.search('eth', item):
                        device_list.append(item.split(':')[3].strip())
        return device_list


# get network date
def get_date(host, oid):
        date_mib = get_all_items(host, oid)[1:]
        date = []
        for item in date_mib:
                byte = float(item.split(':')[3].strip())
                date.append(str(round(byte/1024, 2)) + ' KB')
        return date

if __name__ == '__main__':
        hosts = ['127.0.0.1']
        for host in hosts:
                device_list = get_devices(host)

                inside = get_date(host, 'IF-MIB::ifInOctets')
                outside = get_date(host, 'IF-MIB::ifOutOctets')

                print '==========' + host + '=========='
                print('--------+++++++%s' % inside)
                print('xxxxxxxx+++++++%s' % device_list)
                print('yyyyyyyy+++++++%s' % outside)
                # for i in range(len(inside)):
                for i in range(len(device_list)):
                        print '%s : RX: %s-15s   TX: %s ' % (device_list[i], inside[i], outside[i])
                print
