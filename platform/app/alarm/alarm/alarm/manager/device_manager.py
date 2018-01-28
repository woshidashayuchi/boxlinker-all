# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 17/5/18 下午2:24

from common.logs import logging as log
from db.alarm_db import DeviceDB
from driver.device_driver.device_driver import CpuDriver, MemoryDriver, NetWork, DiskDriver, LbDriver


class DeviceManager(object):
    def __init__(self):
        self.cpu_driver = CpuDriver()
        self.mem_driver = MemoryDriver()
        self.network_driver = NetWork()
        self.disk_driver = DiskDriver()
        self.lb_driver = LbDriver()
        self.device_db = DeviceDB()

    @staticmethod
    def metal_work(all_cpu_data, all_memory_data, all_lb_data):
        [q.update(w) for q in all_cpu_data for w in all_memory_data if q.get('ip') == w.get('ip')]
        [q.update(w) for q in all_cpu_data for w in all_lb_data if q.get('ip') == w.get('ip')]

        return all_cpu_data

    def cpu_data_to_db(self):
        to_db_data = []

        try:
            all_cpu_data = self.cpu_driver.output_cpu()
            all_memory_data = self.mem_driver.output_memory()
            all_network_data = self.network_driver.output_network()
            all_disk_data = self.disk_driver.output_disk()
            all_lb_data = self.lb_driver.output_lb()
        except Exception, e:
            log.error('get the nodes monitor message error, reason is: %s' % e)
            return

        log.info('get all the nodes cpu message is: %s' % all_cpu_data)
        log.info('get all the nodes memory message is: %s' % all_memory_data)
        log.info('get all the nodes network message is: %s' % all_network_data)
        log.info('get all the nodes disk message is: %s' % all_disk_data)
        log.info('get all the nodes lb message is: %s' % all_lb_data)

        try:
            to_data = self.metal_work(all_cpu_data, all_memory_data, all_lb_data)

            for i in to_data:
                for j in all_network_data:
                    if i.get('ip') == j.get('ip'):
                        i['network'] = j.get('network')

                for m in all_disk_data:
                    if i.get('ip') == m.get('ip'):
                        i['disk_device'] = m.get('disk_device')

                to_db_data.append(i)

            log.info('to db data is: %s' % to_db_data)
        except Exception, e:
            log.error('group the data error, reason is: %s' % e)
            return

        try:
            self.device_db.catch_message(to_db_data)
        except Exception, e:
            log.error('insert the data to database error, reason is: %s' % e)
            return

        return
