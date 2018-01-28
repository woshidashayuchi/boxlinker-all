# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 17/4/14 上午10:30

from common.logs import logging as log
import uuid


class ElementExplain(object):
    def __init__(self):
        pass

    @staticmethod
    def insert_alarm_ex(dict_data):
        a_uuid = uuid.uuid4()
        user_uuid = dict_data.get('user_uuid')
        service_uuid = dict_data.get('service_uuid')
        wise = dict_data.get('wise')
        if wise is None:
            wise = 0
        else:
            wise = 1
        cpu_unit = dict_data.get('cpu_unit')
        cpu_value = dict_data.get('cpu_value')
        memory_unit = dict_data.get('memory_unit')
        memory_value = dict_data.get('memory_value')
        network_unit = dict_data.get('network_unit')
        network_value = dict_data.get('network_value')
        storage_unit = dict_data.get('storage_unit')
        storage_value = dict_data.get('storage_value')
        time_span = dict_data.get('time_span')
        alarm_time = dict_data.get('alarm_time')
        email = dict_data.get('email')
        phone = dict_data.get('phone')

        return a_uuid, user_uuid, service_uuid, wise, cpu_unit, cpu_value, memory_unit, memory_value, network_unit, \
            network_value, storage_unit, storage_value, time_span, alarm_time, email, phone

