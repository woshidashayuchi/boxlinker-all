# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/03/01
import json
import requests
from common.logs import logging as log
from conf import conf
from common.code import request_result


class MonitorDriver(object):
    def __init__(self):
        pass

    @staticmethod
    def struct_sql(parameters):
        # client = InfluxDBClient(host='influxdb', port=8086, username='root', password='root', database='dashboard')
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
                request_sql = STATICSQL.replace("change", "cpu/request")
                result = {"usage_sql": usage_sql, "limit_sql": limit_sql, "request_sql": request_sql}
                return result
            if parameters.get("type") == "memory":
                usage_sql = STATICSQL.replace("change", "memory/usage")
                limit_sql = STATICSQL.replace("change", "memory/limit")
                request_sql = STATICSQL.replace("change", "memory/request")
                set_sql = STATICSQL.replace("change", "memory/working_set")
                result = {"usage_sql": usage_sql, "limit_sql": limit_sql, "request_sql": request_sql, "set_sql": set_sql}
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
            return "error"

    def get_monitor_message(self, parameters):

        BASEURL = "http://%s/api/datasources/proxy/1/query?db=k8s&q=" % conf.GRAFANA
        get_sql = ""
        result = []
        try:
            if parameters.get("type") == "cpu":
                get_sql = self.struct_sql(parameters)
            if parameters.get("type") == "memory":
                get_sql = self.struct_sql(parameters)
            if parameters.get("type") == "network":
                get_sql = self.struct_sql(parameters)
            if parameters.get("type") == "filesystem":
                get_sql = self.struct_sql(parameters)
            log.info('get_sql is: %s' % get_sql)
        except Exception, e:
            log.error("create sql(cpu) error, reason=%s" % e)
            return "error"

        try:
            rname = ""
            values = ""
            respon = {}
            for i in get_sql.keys():
                change = i
                res_sql = get_sql.get(change)
                re = json.loads(requests.get(BASEURL+res_sql).text)
                log.info('1111111>>>>>>>>>>>>>>>>>>>>>')
                log.info(re)
                for i in re.get("results"):
                    if i.get("series") is None:
                        pass
                    else:
                        for j in i.get("series"):
                            rname = j.get("name")
                            values = j.get("values")
                        respon = {"name": rname, "value": values}
                # log.info(json.loads(requests.get(BASEURL+res_sql).text))
                result.append(respon)
            # result["aaa"] = json.loads(requests.get(BASEURL+res_sql).text)
            if result[0].get("value") is not None:
                for i in result:
                    for j in i.get("value"):
                        if j[1] == 0 and i.get("value").index(j) > 0 and i.get("value")[i.get("value").index(j)-1][1] is not None:
                            j[1] = i.get("value")[i.get("value").index(j)-1][1]

                        if j[1] == 0 and i.get("value").index(j) == 0:
                            for x in i.get("value"):
                                if x[1] != 0 and x[1] is not None:
                                    j[1] = x[1]
                            # j[1] = i.get("value")[i.get("value").index(j)+1][1]
                        if j[1] < 0 and j[1] is not None:
                            j[1] = abs(j[1])

            return request_result(0, result)

        except Exception, e:
            log.error("get the result error, reason=%s" % e)
            return "error"
