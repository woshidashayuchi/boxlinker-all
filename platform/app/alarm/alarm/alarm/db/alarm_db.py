# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 17/4/12 下午1:12

import uuid
from common.logs import logging as log
from common.mysql_base import MysqlInit
from element_explain import ElementExplain
import json


class AlarmDB(MysqlInit):

    def __init__(self):
        super(AlarmDB, self).__init__()
        self.element_ex = ElementExplain()

    def init_insert(self):

        sql_create_api = "insert into resources_acl(resource_uuid, resource_type, admin_uuid, " \
                         "team_uuid, project_uuid, user_uuid) VALUES('%s', '%s', '%s', '%s', '%s'," \
                         "'%s')" % ('alarm_create', 'api', 'global', 'global', 'global', '0')

        sql_list_api = "insert into resources_acl(resource_uuid, resource_type, admin_uuid, " \
                       "team_uuid, project_uuid, user_uuid) VALUES('%s', '%s', '%s', '%s', '%s'," \
                       "'%s')" % ('alarm_list', 'api', 'global', 'global', 'global', 'global')

        return super(AlarmDB, self).exec_update_sql(sql_create_api, sql_list_api)

    @staticmethod
    def element_explain(team_list):
        try:
            sql = '('
            for i in team_list:
                sql = sql+"'"+i+"'"+','
            sql = sql[:-1] + ')'
        except Exception, e:
            log.error('explain the element for database error, reason is: %s' % e)
            raise Exception('explain the element for database error')
        return sql

    def insert_alarm(self, dict_data):
        service_uuid = dict_data.get('service_uuid')
        alarm_uuid = dict_data.get('alarm_uuid')
        for i in service_uuid:
            rule_uuid = str(uuid.uuid4())
            # sql = "update alarm_service_rules set alarm_uuid='%s' WHERE service_uuid='%s'" % (alarm_uuid, i)
            sql = "insert INTO alarm_service_rules(uuid, alarm_uuid, service_uuid) VALUES ('%s'," \
                  "'%s','%s')" % (rule_uuid, alarm_uuid, i)
            log.info('update the alarm_service_rules sql is: %s' % sql)

            super(AlarmDB, self).exec_update_sql(sql)

    def get_alarm(self, dict_data):

        project_uuid = dict_data.get('project_uuid')
        user_uuid = dict_data.get('user_uuid')
        alarm_uuid = dict_data.get('alarm_uuid')

        sql = "select a.wise,a.cpu_value,a.memory_value,a.network_value," \
              "a.storage_value,a.time_span,a.alarm_time,b.service_uuid from alarming a," \
              "alarm_service_rules b " \
              "WHERE b.service_uuid IN (SELECT uuid from font_service WHERE user_uuid='%s' " \
              "AND project_uuid='%s') AND a.uuid=b.alarm_uuid AND a.uuid=%s" % (user_uuid, project_uuid, alarm_uuid)

        return super(AlarmDB, self).exec_select_sql(sql)

    def get_alarm_svc(self):

        sql = "select c.service_uuid,a.cpu_value,a.memory_value," \
              "a.network_value,a.storage_value,a.time_span,a.alarm_time FROM " \
              "alarming a,alarm_service_rules c WHERE a.uuid=c.alarm_uuid"
        log.info('query the alarm message sql is: %s' % sql)

        return super(AlarmDB, self).exec_select_sql(sql)

    def delete_alarm_svc(self, dict_data):
        service_uuid = dict_data.get('service_uuid')
        id_list = self.element_explain(service_uuid)
        # alarm_uuid = dict_data.get('alarm_uuid')

        sql = "delete from alarm_service_rules WHERE service_uuid in %s" % id_list
        log.info('delete the service and alarm rules sql is: %s' % sql)

        return super(AlarmDB, self).exec_update_sql(sql)

    def update_alarm_svc(self, dict_data):
        service_uuid = dict_data.get('service_uuid')
        alarm_uuid = dict_data.get('alarm_uuid')

        sql = "update alarm_service_rules set alarm_uuid='%s' WHERE service_uuid='%s'" % (alarm_uuid, service_uuid)

        return super(AlarmDB, self).exec_update_sql(sql)

    def get_default(self, dict_data):
        service_uuid = dict_data.get('service_uuid')
        sql = "select uuid FROM alarming WHERE uuid=(SELECT alarm_uuid from alarm_service_rules WHERE " \
              "service_uuid='%s') AND uuid != 'default'" % service_uuid

        return super(AlarmDB, self).exec_select_sql(sql)

    def get_detail(self, dict_data):
        service_uuid = dict_data.get('service_uuid')

        sql = "select a.uuid,a.wise,a.cpu_unit,a.cpu_value,a.memory_unit,a.memory_value," \
              "a.network_unit,a.network_value,a.storage_unit,a.storage_value,a.time_span,a.alarm_time " \
              "b.email, b.phone FROM " \
              "alarming a,alarm_service_rules b" \
              "WHERE b.service_uuid='%s' AND a.uuid=b.alarm_uuid" % service_uuid

        return super(AlarmDB, self).exec_select_sql(sql)

    def update_alarm(self, dict_data):
        sql_alarming = ""
        service_uuid = dict_data.get('service_uuid')
        email = dict_data.get('email')
        phone = dict_data.get('phone')
        up_or_in = dict_data.get('up_or_in')
        a_uuid, user_uuid, service_uuide, wise, cpu_unit, cpu_value, memory_unit, memory_value, network_unit, \
            network_value, storage_unit, storage_value, time_span, \
            alarm_time, alarm_uuid = self.element_ex.insert_alarm_ex(dict_data)

        if up_or_in == 'insert':
            sql_alarming = "insert INTO alarming(uuid,wise,cpu_unit,cpu_value,memory_unit,memory_value," \
                           "network_unit,network_value,storage_unit,storage_value,time_span,alarm_time)" \
                           "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'," \
                           "'%s'" % (a_uuid, wise, cpu_unit, cpu_value, memory_unit, memory_value,
                                     network_unit, network_value, storage_unit, storage_value, time_span, alarm_time)
        elif up_or_in == 'update':
            sql_alarming = "update alarming SET wise=0,cpu_unit='%s',cpu_value='%s',memory_unit='%s'," \
                           "memory_value='%s',network_unit='%s',network_value='%s',storage_unit='%s'," \
                           "storage_value='%s',time_span='%s',alarm_time='%s' WHERE uuid=(SELECT " \
                           "alarm_uuid from alarm_service_rules WHERE " \
                           "service_uuid='%s')" % (cpu_unit, cpu_value, memory_unit, memory_value,
                                                   network_unit, network_value, storage_unit, storage_value,
                                                   time_span, alarm_time, service_uuid)

        sql_rules = "update alarm_service_rules set email='%s' AND phone='%s' ,alarm_uuid='%s'" \
                    "WHERE service_uuid = '%s'" % (email, phone, a_uuid, service_uuid)

        log.info("update the rules sql is: %s,,,,,,and update the alarming sql is: "
                 "%s" % (sql_rules, sql_alarming))

        return super(AlarmDB, self).exec_update(sql_rules, sql_alarming)

    def update_alarm_more(self, dict_data):
        service_uuid = dict_data.get('service_uuid')
        email = dict_data.get('email')

        sql = "update alarm_service_rules SET email= '%s' WHERE service_uuid='%s'" % (email, service_uuid)

        return super(AlarmDB, self).exec_update_sql(sql)

    def get_email_phone(self, service_uuid):
        sql = "select email from alarm_service_rules WHERE service_uuid='%s'" % service_uuid
        # sql = "select email,phone from alarm_service_rules WHERE service_uuid='%s'" % service_uuid

        return super(AlarmDB, self).exec_select_sql(sql)

##########################

    def only_alarm_create(self, dict_data):
        a_uuid = str(uuid.uuid4())
        user_uuid = dict_data.get('user_uuid')
        wise = 0
        cpu_value = dict_data.get('cpu_value')
        memory_value = dict_data.get('memory_value')
        network_value = dict_data.get('network_value')
        storage_value = dict_data.get('storage_value')
        time_span = dict_data.get('time_span')
        alarm_time = dict_data.get('alarm_time')
        email = dict_data.get('email')
        phone = dict_data.get('phone')

        sql = "insert into alarming(uuid, user_uuid, wise,cpu_value,memory_value," \
              "network_value,storage_value,time_span,alarm_time," \
              "email,phone) VALUES ('%s','%s',%d,%d,%d,%d,%d,'%s','%s','%s'," \
              "%s)" % (a_uuid, user_uuid, wise, cpu_value, memory_value,
                       network_value, storage_value, time_span, alarm_time, email,
                       phone)
        sql_acl = "insert into resources_acl(resource_uuid,resource_type,admin_uuid,team_uuid,project_uuid," \
                  "user_uuid) VALUES ('%s','%s','%s','%s','%s'," \
                  "'%s')" % (a_uuid, 'alarm', 'global', dict_data.get('team_uuid'),
                             dict_data.get('project_uuid'), dict_data.get('user_uuid'))

        super(AlarmDB, self).exec_update_sql(sql, sql_acl)

        return a_uuid

    def only_alarm_query(self, dict_data):
        user_uuid = dict_data.get('user_uuid')
        sql = "select uuid alarm_uuid,cpu_value,memory_value," \
              "network_value, storage_value,time_span,alarm_time,email,phone,wise FROM " \
              "alarming WHERE user_uuid='%s'" % user_uuid

        return super(AlarmDB, self).exec_select_sql(sql)

    def only_detail_query(self, dict_data):
        alarm_uuid = dict_data.get('alarm_uuid')
        sql = "select uuid alarm_uuid,cpu_value,memory_value," \
              "network_value,storage_value,time_span,alarm_time,email,phone,wise FROM " \
              "alarming WHERE uuid ='%s'" % alarm_uuid

        return super(AlarmDB, self).exec_select_sql(sql)

    def only_update_alarm(self, dict_data):

        alarm_uuid = dict_data.get('alarm_uuid')
        alarm_name = dict_data.get('alarm_name')
        cpu_value = dict_data.get('cpu_value')
        memory_value = dict_data.get('memory_value')
        network_value = dict_data.get('network_value')
        storage_value = dict_data.get('storage_value')
        time_span = dict_data.get('time_span')
        alarm_time = dict_data.get('alarm_time')
        email = dict_data.get('email')
        phone = dict_data.get('phone')

        sql = "update alarming set wise='%s',cpu_value=%d," \
              "memory_value=%d," \
              "network_value=%d,storage_value=%d," \
              "time_span='%s',alarm_time='%s',email='%s',phone='%s'" \
              "WHERE uuid='%s'" % (alarm_name, cpu_value, memory_value,
                                   network_value, storage_value, time_span,
                                   alarm_time, email, phone, alarm_uuid)

        return super(AlarmDB, self).exec_update_sql(sql)

    def alarm_if_used(self, dict_data):
        alarm_uuid = dict_data.get('alarm_uuid')

        sql = "select service_uuid from alarm_service_rules WHERE alarm_uuid='%s'" % alarm_uuid

        return super(AlarmDB, self).exec_select_sql(sql)

    def only_delete_alarm(self, dict_data):

        sql = "delete from alarming WHERE uuid='%s'" % (dict_data.get('alarm_uuid'))

        return super(AlarmDB, self).exec_update_sql(sql)


class DeviceDB(MysqlInit):

    def __init__(self):
        super(DeviceDB, self).__init__()
        self.element_ex = ElementExplain()

    def catch_message(self, list_data):

        for dict_data in list_data:
            log.info('inner the db data is: %s' % dict_data)
            sql = "insert INTO device_alarming(ip, cpu_used, cpu_wa, mem_used, network, disk_used, " \
                  "lb) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (dict_data.get('ip'),
                                                                             dict_data.get('cpu_used'),
                                                                             dict_data.get('cpu_wa'),
                                                                             dict_data.get('mem_used'),
                                                                             json.dumps(dict_data.get('network')),
                                                                             json.dumps(dict_data.get('disk_device')),
                                                                             json.dumps(dict_data.get('lb')))
            log.info('insert the monitor for device sql is: %s' % sql)

            super(DeviceDB, self).exec_update_sql(sql)

        return
