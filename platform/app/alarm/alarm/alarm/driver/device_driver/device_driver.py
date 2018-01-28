# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 17/5/18 下午2:32

from common.logs import logging as log
from conf import conf
import os
import re


class CpuDriver(object):

    def __init__(self):
        self.device_ip = [x for x in conf.device_ip.split(',')]

    @staticmethod
    def get_all_items(host, oid):
        sn1 = os.popen('snmpwalk -v 2c -c public ' + host + ' ' + oid + '|grep Raw|grep Cpu|grep -v Kernel').read().split('\n')[:-1]
        return sn1

    def get_data(self, host):
        items = self.get_all_items(host, '.1.3.6.1.4.1.2021.11')

        date = []
        rate = []
        cpu_total = 0

        for item in items:
            float_item = float(item.split(' ')[3])
            cpu_total += float_item
            if item == items[0]:
                date.append(float(item.split(' ')[3]) + float(items[1].split(' ')[3]))
            elif item == item[2]:
                date.append(float(item.split(' ')[3] + items[5].split(' ')[3] + items[6].split(' ')[3]))
            else:
                date.append(float_item)

        for item in date:
            rate.append((item/cpu_total)*100)

        # mean = ['%us', '%ni', '%sy', '%id', '%wa', '%cpu_irq', '%cpu_sIRQ']
        mean = ['%us', '%sy', '%wa']
        result = map(None, rate, mean)
        return result

    def output_cpu(self):
        result = []
        for host in self.device_ip:
            try:
                cpu_data = self.get_data(host)
            except Exception, e:
                log.error('get the device cpu monitor message error, reason is: %s' % e)
                raise Exception('get the device cpu monitor message happen exception')

            log.info('get the cpu data is: %s' % cpu_data)
            add_result = {'ip': host, 'cpu_used': round((cpu_data[0][0]+cpu_data[1][0]), 2),
                          'cpu_wa': round(cpu_data[2][0], 2)}

            result.append(add_result)

        return result


class MemoryDriver(object):

    def __init__(self):
        self.device_ip = [x for x in conf.device_ip.split(',')]

    @staticmethod
    def get_all_items(host, oid):
        sn1 = os.popen('snmpwalk -v 2c -c public ' + host + ' ' + oid).read().split('\n')[:-1]
        return sn1

    def get_swap_total(self, host):
            swap_total = self.get_all_items(host, 'UCD-SNMP-MIB::memTotalSwap.0')[0].split(' ')[3]
            return swap_total

    def get_swap_used(self, host):
            swap_avail = self.get_all_items(host, 'UCD-SNMP-MIB::memAvailSwap.0')[0].split(' ')[3]
            swap_total = self.get_swap_total(host)
            swap_used = str(round(((float(swap_total)-float(swap_avail))/float(swap_total))*100, 2)) + '%'
            return swap_used

    def get_mem_total(self, host):
            mem_total = self.get_all_items(host, 'UCD-SNMP-MIB::memTotalReal.0')[0].split(' ')[3]
            return mem_total

    def get_mem_used(self, host):
            mem_total = self.get_mem_total(host)
            mem_avail = self.get_all_items(host, 'UCD-SNMP-MIB::memAvailReal.0')[0].split(' ')[3]
            mem_used = str(round(((float(mem_total)-float(mem_avail))/float(mem_total))*100, 2)) + '%'
            return mem_used

    def output_memory(self):
        result = []
        for host in self.device_ip:
            try:
                mem_used = self.get_mem_used(host)
            except Exception, e:
                log.error('get the device memory monitor message error, reason is: %s' % e)
                raise Exception('get the device memory monitor message happen exception')
            # swap_used = self.get_swap_used(host)
            add_result = {'ip': host, 'mem_used': mem_used}
            result.append(add_result)

            log.info('get the memory data is: %s' % mem_used)

        return result


class NetWork(object):
    def __init__(self):
        self.device_ip = [x for x in conf.device_ip.split(',')]

    @staticmethod
    def get_all_items(host, oid):
        sn1 = os.popen('snmpwalk -v 2c -c public ' + host + ' ' + oid).read().split('\n')[:-1]
        return sn1

    # get network device
    def get_devices(self, host):
            device_mib = self.get_all_items(host, 'RFC1213-MIB::ifDescr')
            device_list = []
            for item in device_mib:
                    if re.search('eth', item):
                            device_list.append(item.split(':')[3].strip())
            return device_list

    # get network date
    def get_date(self, host, oid):
            date_mib = self.get_all_items(host, oid)[1:]
            date = []
            for item in date_mib:
                    byte = float(item.split(':')[3].strip())
                    date.append(str(round(byte/1024, 2)) + ' KB')
            return date

    def output_network(self):
        result = []
        network = []
        for host in self.device_ip:
            try:
                device_list = self.get_devices(host)
                inside = self.get_date(host, 'IF-MIB::ifInOctets')
                outside = self.get_date(host, 'IF-MIB::ifOutOctets')
            except Exception, e:
                log.error('get the device network monitor message error, reason is: %s' % e)
                raise Exception('get the device network monitor message happen exception')

            # for i in range(len(inside)):
            for i in range(len(device_list)):
                if device_list[i] not in ['eth0', 'eth1', 'eth2']:
                    continue

                network.append({'net_device': device_list[i], 'RX': inside[i], 'TX': outside[i]})

                # add_result = {'ip': host, 'network': {'net_device': device_list[i], 'RX': inside[i],
                #                                       'TX': outside[i]}}
            add_result = {'ip': host, 'network': network}
            result.append(add_result)

            network = []

            log.info('get the network data is: %s' % add_result)

        return result


class DiskDriver(object):

    def __init__(self):
        self.device_ip = [x for x in conf.device_ip.split(',')]

    @staticmethod
    def get_all_items(host, oid):
        sn1 = os.popen('snmpwalk -v 2c -c public ' + host + ' ' + oid).read().split('\n')[:-1]
        return sn1

    @staticmethod
    def get_date(source, newitem):
        for item in source[5:]:
            newitem.append(item.split(':')[3].strip())
        return newitem

    @staticmethod
    def get_real_date(item1, item2, listname):
        for i in range(len(item1)):
            listname.append(int(item1[i])*int(item2[i])/1024)
        return listname

    def caculate_disk_used_rate(self, host):
        hrStorageDescr = self.get_all_items(host, 'HOST-RESOURCES-MIB::hrStorageDescr')
        hrStorageUsed = self.get_all_items(host, 'HOST-RESOURCES-MIB::hrStorageUsed')
        hrStorageSize = self.get_all_items(host, 'HOST-RESOURCES-MIB::hrStorageSize')
        hrStorageAllocationUnits = self.get_all_items(host, 'HOST-RESOURCES-MIB::hrStorageAllocationUnits')

        disk_list = []
        hrsused = []
        hrsize = []
        hrsaunits = []

        #get disk_list
        for item in hrStorageDescr:
            if re.search('/', item):
                disk_list.append(item.split(':')[3])

        self.get_date(hrStorageUsed, hrsused)
        self.get_date(hrStorageSize, hrsize)

        for item in hrStorageAllocationUnits[5:]:
            hrsaunits.append(item.split(':')[3].strip().split(' ')[0])

        # disk_used = hrStorageUsed * hrStorageAllocationUnits /1024 (KB)
        disk_used = []
        total_size = []
        disk_used = self.get_real_date(hrsused, hrsaunits, disk_used)
        total_size = self.get_real_date(hrsize, hrsaunits, total_size)

        diskused_rate = []
        for i in range(len(disk_used)):
                diskused_rate.append(str(round((float(disk_used[i])/float(total_size[i])*100), 2)) + '%')

        return diskused_rate, disk_list

    def output_disk(self):
        result = []
        disk_device = []
        for host in self.device_ip:
            try:
                ca = self.caculate_disk_used_rate(host)
                diskused_rate = ca[0]
                partition = ca[1]
            except Exception, e:
                log.error('get the device network monitor message error, reason is: %s' % e)
                raise Exception('get the device network monitor message happen exception')

            # for i in range(len(diskused_rate)):
            for i in range(len(partition)):
                if 'var/lib/kubelet/pods' in partition[i] or 'var/lib/docker/containers' in partition[i]:
                    continue
                add_ret = {'disk_device': {'partition': partition[i], 'diskused_rate': diskused_rate[i]}}

                disk_device.append(add_ret)
                # add_result = {'ip': host, 'disk_device': {'partition': partition[i],
                #                                           'diskused_rate': diskused_rate[i]}}
                # print '%-20s used: %s' % (partition[i], diskused_rate[i])

            result.append({'ip': host, 'disk_device': disk_device})

            disk_device = []

        return result


class LbDriver(object):

    def __init__(self):
        self.device_ip = [x for x in conf.device_ip.split(',')]

    @staticmethod
    def get_all_items(host, oid):
        sn1 = os.popen('snmpwalk -v 2c -c public ' + host + ' ' + oid).read().split('\n')
        return sn1

    def get_load(self, host, loid):
        load_oids = '1.3.6.1.4.1.2021.10.1.3.' + str(loid)
        return self.get_all_items(host, load_oids)[0].split(':')[3]

    def output_lb(self):
        result = []
        for host in self.device_ip:
            load1 = self.get_load(host, 1)
            load10 = self.get_load(host, 2)
            load15 = self.get_load(host, 3)

            add_result = {'ip': host, 'lb': {'load1': load1, 'load10': load10, 'load15': load15}}
            # print '%s load(1min): %s ,load(10min): %s ,load(15min): %s' % (host, load1, load10, load15)
            log.info('get the lb data is: %s' % add_result)

            result.append(add_result)

        return result
