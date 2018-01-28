# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 17/4/14 上午10:55

from common.logs import logging as log
from db.alarm_db import AlarmDB
from common.code import request_result
from driver.alarm_driver import AlarmDriver


class AlarmManager(object):
    def __init__(self):
        self.alarm_db = AlarmDB()
        self.alarm_drv = AlarmDriver()

    def alarm_into_manager(self, dict_data):
        try:
            self.alarm_db.insert_alarm(dict_data)
        except Exception, e:
            log.error('insert the table alarming error, reason is: %s' % e)
            return request_result(401)

        return request_result(0, 'create the alarming successfully')

    def query_result_ex(self, dict_data):
        result = []

        try:
            ret = self.alarm_db.get_alarm(dict_data)
        except Exception, e:
            log.error('query the database error, reason is: %s' % e)
            raise Exception('query the database error')
        try:
            for i in ret:
                ret_ex = {
                    'wise': i[0],
                    'cpu_value': i[1],
                    'memory_value': i[2],
                    'network_value': i[3],
                    'storage_value': i[4],
                    'time_span': i[5],
                    'alarm_time': i[6],
                    'service_uuid': i[7]
                }
                result.append(ret_ex)
        except Exception, e:
            log.error('explain the db result error, reason is: %s' % e)
            raise Exception('explain the db result error')

        return result

    def query_manager(self, dict_data):
        try:
            ret = self.query_result_ex(dict_data)
        except Exception, e:
            log.error('get the alarm message error, reason is: %s' % e)
            return request_result(404)

        return request_result(0, ret)

    def alarm_svc_delete(self, dict_data):
        try:
            ret = self.alarm_db.delete_alarm_svc(dict_data)
            if ret is not None:
                return request_result(402)

            return request_result(0, {'resource_uuid': dict_data.get('alarm_uuid')})
        except Exception, e:
            log.error('delete database data error, reason is: %s' % e)
            return request_result(402)

    def alarm_svc_update(self, dict_data):
        try:
            ret = self.alarm_db.update_alarm_svc(dict_data)
            if ret is not None:
                return request_result(403)

            return request_result(0, {'resource_uuid': dict_data.get('alarm_uuid')})
        except Exception, e:
            log.error('update the database data error, reason is: %s' % e)
            return request_result(403)

    def only_alarm_create(self, dict_data):

        try:
            alarm_uuid = self.alarm_db.only_alarm_create(dict_data)
            return request_result(0, {'alarm_uuid': alarm_uuid})
        except Exception, e:
            log.error('database insert error, reason is: %s' % e)
            return request_result(401)

    @staticmethod
    def query_result_work(database_ret):
        result = []

        for i in database_ret:
            alarm_uuid = i[0]
            cpu_value = i[1]
            memory_value = i[2]
            network_value = i[3]
            storage_value = i[4]
            time_span = i[5]
            alarm_time = i[6]
            email = i[7]
            phone = i[8]
            alarm_name = i[9]

            dict_ret = {
                'alarm_name': alarm_name,
                'alarm_uuid': alarm_uuid,
                'cpu_value': cpu_value,
                'memory_value': memory_value,
                'network_value': network_value,
                'storage_value': storage_value,
                'time_span': time_span,
                'alarm_time': alarm_time,
                'email': email,
                'phone': phone,
            }

            result.append(dict_ret)

        return result

    def only_alarm_query(self, dict_data):
        try:
            ret = self.alarm_db.only_alarm_query(dict_data)

        except Exception, e:
            log.error('database insert error, reason is: %s' % e)
            return request_result(404)

        try:
            result = self.query_result_work(ret)
        except Exception, e:
            log.error('explain the data error ,reason is: %s' % e)
            return request_result(601)

        return request_result(0, {'alarm_list': result})

    def only_detail_query(self, dict_data):

        try:
            ret = self.alarm_db.only_detail_query(dict_data)

        except Exception, e:
            log.error('database insert error, reason is: %s' % e)
            return request_result(404)

        try:
            result = self.query_result_work(ret)
        except Exception, e:
            log.error('explain the data error ,reason is: %s' % e)
            return request_result(601)

        return request_result(0, result[0])

    def only_update_alarm(self, dict_data):
        try:
            ret = self.alarm_db.only_detail_query(dict_data)
        except Exception, e:
            log.error('database select error, reason is: %s' % e)
            return request_result(404)

        try:
            result = self.query_result_work(ret)[0]
            result.update(dict_data)
            log.info('to update the database json is: %s' % result)
        except Exception, e:
            log.error('ecplain the data error, reason is: %s' % e)
            return request_result(601)

        try:
            self.alarm_db.only_update_alarm(result)
            return request_result(0, {'resource_uuid': dict_data.get('alarm_uuid')})
        except Exception, e:
            log.error('database update error, reason is: %s' % e)
            return request_result(403)

    def only_del_alarm(self, dict_data):
        # 判断要删除的规则是否有服务使用
        try:
            ret = self.alarm_db.alarm_if_used(dict_data)
            if len(ret[0]) != 0:
                return request_result(301)
        except Exception, e:
            log.error('get the service id when check the alarm is used by service, reason is: %s' % e)
            return request_result(404)

        # 证实没有服务使用要删除的告警规则,继续下一步:删除告警规则
        try:
            up_ret = self.alarm_db.only_delete_alarm(dict_data)
            if up_ret is not None:
                return request_result(402)

            return request_result(0, {'resource_uuid': dict_data.get('alarm_uuid')})
        except Exception, e:
            log.error('delete the database error, reason is: %s' % e)
            return request_result(402)


class AlarmForService(object):
    def __init__(self):
        self.alarm_drv = AlarmDriver()

    def alarm_for_svc(self, dict_data):
        for i in ['cpu', 'memory']:
            dict_data['type'] = i
            self.alarm_drv.alarm_driver(dict_data)
