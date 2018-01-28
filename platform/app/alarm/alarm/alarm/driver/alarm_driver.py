# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 17/4/14 上午10:53

from __future__ import division
from common.logs import logging as log
from conf import conf
import json
import base64
import time
import requests
from db.alarm_db import AlarmDB
from rbt_client import PodsRpcClient
from common.code import request_result


class AlarmDriver(object):
    def __init__(self):
        self.GRAFANA = conf.GRAFANA
        self.alarm_db = AlarmDB()
        self.user = conf.user
        self.password = base64.decodestring(conf.password)
        self.recover_login = conf.recover_login
        self.k8s_pod = conf.k8s_pod
        self.pods_rbt_client = PodsRpcClient()
        self.email_api = conf.email_api
        self.login = conf.login_url
        self.all_svc = conf.all_svc_url

    @staticmethod
    def sql_driver(parameters):
        time_long = parameters.get("time_long")
        time_span = parameters.get("time_span")
        project_uuid = parameters.get("project_uuid")
        pod_name = parameters.get("pod_name")
        STATICSQL = "SELECT sum(\"value\") FROM \"change\" WHERE \"type\" = \'pod_container\' " \
                    "AND \"namespace_name\" =~ /%s$/ " \
                    "AND \"pod_name\" =~ /%s$/ " \
                    "AND time > now() - %s GROUP BY time(%s), \"container_name\" fill(null)&epoch=ms" % (project_uuid,
                                                                                                pod_name,
                                                                                                time_long,
                                                                                                time_span)
        STATICNET = "SELECT sum(\"value\") FROM \"change\" WHERE \"type\" = \'pod\' " \
                    "AND \"namespace_name\" =~ /%s$/ " \
                    "AND \"pod_name\" =~ /%s$/ " \
                    "AND time > now() - %s GROUP BY time(%s) fill(null)&epoch=ms" % (project_uuid,
                                                                                     pod_name,
                                                                                     time_long,
                                                                                     time_span)
        try:
            if parameters.get("type") == "cpu":
                usage_sql = STATICSQL.replace("change", "cpu/usage_rate")
                limit_sql = STATICSQL.replace("change", "cpu/limit")
                # request_sql = STATICSQL.replace("change", "cpu/request")
                result = {"usage_sql": usage_sql, "limit_sql": limit_sql}   # , "request_sql": request_sql
                return result
            if parameters.get("type") == "memory":
                usage_sql = STATICSQL.replace("change", "memory/usage")
                limit_sql = STATICSQL.replace("change", "memory/limit")
                # request_sql = STATICSQL.replace("change", "memory/request")
                # set_sql = STATICSQL.replace("change", "memory/working_set")
                result = {"usage_sql": usage_sql, "limit_sql": limit_sql}   # , "request_sql": request_sql, "set_sql": set_sql
                return result
            if parameters.get("type") == "network":
                tx_sql = STATICNET.replace("change", "network/tx_rate")
                rx_sql = STATICNET.replace("change", "network/rx_rate")
                result = {"tx_sql": tx_sql, "rx_sql": rx_sql}
                return result
            if parameters.get("type") == "filesystem":
                usage_sql = STATICNET.replace("change", "filesystem/usage")
                limit_sql = STATICNET.replace("change", "filesystem/limit")
                result = {"usage_sql": usage_sql, "limit_sql": limit_sql}
                return result
        except Exception, e:
            log.error("sql create error, reason=%s" % e)
            raise Exception('sql create error')

    def get_pods_name(self, project_uuid, service_name):
        pods_name = []
        pod_message = {"namespace": project_uuid, 'rtype': 'pods'}

        try:
            response = self.pods_rbt_client.get_pod_messages(pod_message)
            response = response.get('items')

        except Exception, e:
            log.error("explain the kubernetes response error,reason=%s" % e)
            raise Exception('explain the kubernetes response error')

        for i in response:
            if service_name == i.get("metadata").get("labels").get("component"):
                pod_name = i.get("metadata").get("name")
                pods_name.append(pod_name)

        return pods_name

    def email_driver(self, data):
        headers = {'content-type': "application/json"}
        body = json.JSONEncoder().encode(data)

        try:
            r = requests.post(self.email_api, headers=headers,
                              data=body, timeout=5)
            status = r.json()['status']
            log.info('Email send request=%s, request_status=%s' % (r, status))
            if int(status) != 0:
                raise(Exception('request_code not equal 0'))
        except Exception, e:
            log.error('Email send error: reason=%s' % e)
            return request_result(601)

        return request_result(0)

    def get_email_and_phone(self, service_uuid):

        try:
            ret = self.alarm_db.get_email_phone(service_uuid)
            email = ret[0][0]
        except Exception, e:
            log.error('get the email and phone error, reason is: %s' % e)
            return request_result(404)

        return request_result(0, email)

    def send_email(self, email_list, service_uuid):
        email = self.get_email_and_phone(service_uuid)

        if email.get('status') != 0:
            return request_result(404)
        email = email.get('result')
        log.info('send to the email is: %s' % email)

        usage = ""
        for i in email_list:
            usage = usage + "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (i.get('service_name'), i.get('usage'),
                                                                            i.get('time'))
        html_body = ("<table bgcolor=\"#FF5151\" border=\"2\">"
                     "<th>service name</th>"
                     "<th>alarm message</th>"
                     "<th>alarm time</th>"
                     "%s"
                     "</table>") % str(usage)

        data = {
                   "to": email,
                   "title": "服务告警啦",
                   "text": None,
                   "html": html_body
               }

        email_send = self.email_driver(data).get('status')
        if int(email_send) != 0:
            return request_result(601)

    def explain_monitor_data(self, dict_data, memory_value):
        memory_limit = 0
        memory_usage = 0
        sum = 0
        for i in dict_data.get('results'):
            for j in i.get('series'):
                if j.get('name') == 'memory/limit':
                    memory_limit = j.get('values')[1][1]/1000000
                if j.get('name') == 'memory/usage':
                    for n in range(1, 15):
                        all_usage = sum+j.get('values')[n][1]
                        memory_usage = all_usage/15
        if memory_usage/memory_limit <= memory_value:
            self.send_email(memory_usage)

    def get_admin_token(self):
        try:
            admin_data = {'user_name': 'service', 'password': 'service@2017'}
            ret = json.loads(requests.post(self.login, json.dumps(admin_data), timeout=5).text)
            log.info('admin login the result is: %s,type is: %s' % (ret, type(ret)))
            if ret.get('status') != 0:
                return False

            return ret.get('result').get('user_token')

        except Exception, e:
            log.error('get the admin token error, reason is: %s' % e)
            return False

    def alarm_driver(self, dict_data):
        base_sql = conf.basesql
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        now_hour = int(time.strftime('%H', time.localtime(time.time())))
        service_uuid = ''
        alarm_start_time = 12
        alarm_end_time = 15
        memory_limit = 0
        cpu_limit = 0
        to_email = []

        # 获取数据库所有服务预告警规则与信息
        try:
            q_ret = self.alarm_db.get_alarm_svc()
        except Exception, e:
            log.error('get the alarm rules from database error, reason is: %s' % e)
            raise Exception('get the alarm rules from database error')

        admin_token = self.get_admin_token()
        header = {'token': admin_token}
        if not admin_token:
            raise Exception('get token error')

        try:
            svc_ret = requests.get(self.all_svc, headers=header)
            log.info('------------------------------%s' % svc_ret)
            svc_ret = json.loads(svc_ret.text)
            if svc_ret.get('status') != 0:
                raise Exception('get the all svc1 error')
        except Exception, e:
            log.error('get the all svc error, reason is: %s' % e)
            raise Exception('get the all svc error')

        # 获取每个对应服务下的pod名称
        for i in q_ret:
            # project_uuid = i[0]
            # service_name = i[1]
            service_uuid = i[0]
            cpu_value = i[1]
            memory_value = i[2]
            network_value = i[3]
            storage_value = i[4]
            time_span = i[5]
            alarm_time = i[6]  # 00~03 03~06 06~09 09~12 12~15 15~18 18~21 21~24
            pod_name = ""
            for x in svc_ret.get('result'):
                if x.get('service_uuid') == service_uuid:
                    project_uuid = x.get('project_uuid')
                    service_name = x.get('service_name')
                    try:
                        pods_name = self.get_pods_name(project_uuid, service_name)
                        log.info('from k8s api get the pod_name is %s' % str(pods_name))
                    except Exception, e:
                        log.error('get the pod message error, reason is: %s' % e)
                        raise Exception('get the pod message error')

                    for j in pods_name:
                        dict_data['project_uuid'] = project_uuid
                        dict_data['pod_name'] = j
                        try:
                            sql_dict = self.sql_driver(dict_data)
                            log.info('sql_dict is: %s' % sql_dict)
                        except Exception, e:
                            log.error('create the query sql error, reason is:%s' % e)
                            raise Exception('sql create error')

                        try:

                            limit_sql = sql_dict.get('limit_sql')
                            limit_ret = json.loads(requests.get(base_sql+limit_sql).text)
                            for m in limit_ret.get('results'):
                                for n in m.get('series'):
                                    if dict_data.get('type') == 'memory':
                                        memory_limit = n.get('values')[1][1]
                                    if dict_data.get('type') == 'cpu':
                                        cpu_limit = n.get('values')[1][1]

                            usage_sql = sql_dict.get('usage_sql')
                            usage_ret = json.loads(requests.get(base_sql+usage_sql).text)
                            sum_m = 0
                            sum_c = 0
                            for x in usage_ret.get('results'):
                                for y in x.get('series'):
                                    for l in range(2, 16):
                                        if dict_data.get('type') == 'memory':
                                            sum_m = sum_m+y.get('values')[l][1]
                                        if dict_data.get('type') == 'cpu':
                                            sum_c = sum_c+y.get('values')[l][1]
                            memory_usage = sum_m/14
                            cpu_usage = sum_c/14

                            alarm_start_time = int(alarm_time.split('~')[0])
                            alarm_end_time = int(alarm_time.split('~')[1])
                            log.info('from database get the alarm time, latest time is: %s, '
                                     'last time is: %s' % (alarm_start_time, alarm_end_time))
                            if memory_limit != 0 and memory_usage/memory_limit*100 >= memory_value:
                                to_email.append({'usage': str(round(memory_usage/memory_limit*100, 2))+'%',
                                                 'service_name': service_name,
                                                 'time': now_time})

                                # self.send_email(str(round(memory_usage/memory_limit*100, 2))+'%')
                            if cpu_limit != 0 and cpu_usage/cpu_limit*100 >= cpu_value:
                                log.info('explain the memory monitor data result is:cpu_usage=%s,cpu_limit=%s,'
                                         'cpu_value=%s,shang=%s' % (cpu_usage, cpu_limit,
                                                                    cpu_value, cpu_usage/cpu_limit))

                                to_email.append({'usage': str(round(cpu_usage/cpu_limit*100, 2))+'%',
                                                 'service_name': service_name,
                                                 'time': now_time})
                                # self.send_email(str(round(cpu_usage/cpu_limit*100, 2))+'%')
                        except Exception, e:
                            log.error('explain the data error, reason is: %s' % e)
                            raise Exception('explain the memory data error')
        log.info('now_hour=======%s,alarm_start_time=====%s,alarm_end_time=====%s' % (now_hour, alarm_start_time,
                                                                                      alarm_end_time))
        if alarm_start_time <= now_hour < alarm_end_time:
            # self.send_email(to_email, service_uuid)
            log.info('will send the email data is: %s ' % to_email)

        return

    def get_detail_msg(self, dict_data):
        inner = {}
        try:
            ret = self.alarm_db.get_detail(dict_data)
            for i in ret:
                uuid = i[0]
                wise = i[1]
                cpu_unit = i[2]
                cpu_value = i[3]
                memory_unit = i[4]
                memory_value = i[5]
                network_unit = i[6]
                network_value = i[7]
                storage_unit = i[8]
                storage_value = i[9]
                time_span = i[10]
                alarm_time = i[11]
                email = i[12]
                phone = i[13]
        except Exception, e:
            log.error('get the alarm details error, reason is: %s' % e)
            return 'error'

        inner['uuid'] = uuid
        inner['wise'] = wise
        inner['cpu_unit'] = cpu_unit
        inner['cpu_value'] = cpu_value
        inner['memory_unit'] = memory_unit
        inner['memory_value'] = memory_value
        inner['network_unit'] = network_unit
        inner['network_value'] = network_value
        inner['storage_unit'] = storage_unit
        inner['storage_value'] = storage_value
        inner['time_span'] = time_span
        inner['alarm_time'] = alarm_time
        inner['email'] = email
        inner['phone'] = phone

        dict_data.update(inner)
        return dict_data

    def update_alarm(self, dict_data):
        service_uuid = dict_data.get('service_uuid')
        dict_data = self.get_detail_msg(dict_data)
        if dict_data == 'error':
            return request_result(601)

        try:
            ret = self.alarm_db.get_default(service_uuid)
            if len(ret) == 0 or len(ret[0]) == 0:
                dict_data['up_or_in'] = 'insert'
            else:
                dict_data['up_or_in'] = 'update'

            self.alarm_db.update_alarm_more(dict_data)
        except Exception, e:
            log.error('database operate error, reason is: %s' % e)
            return request_result(404)
