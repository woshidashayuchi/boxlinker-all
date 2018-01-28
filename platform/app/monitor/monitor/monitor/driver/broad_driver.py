# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/03/02
from common.logs import logging as log
from common.code import request_result
from conf import conf
from rpcapi_client import KubernetesRpcClient
import json
import urllib


class BroadDriver(object):

    def __init__(self):
        self.kuber = KubernetesRpcClient()

    @staticmethod
    def console(pods):

        changes = ["cpu/usage_rate", "cpu/limit", "memory/usage", "memory/limit"]
        cpu_limit = 0
        cnt_c = 0
        cnt_m = 0
        memory_limit = 0
        cpu_result = []
        memory_result = []
        a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        namespace = pods.get("namespace")
        pods = pods.get("pods")
        STATICHTTP = "http://%s/api/datasources/proxy/1/query?db=k8s&q=" % conf.GRAFANA
        log.info("aaaaaaa=======%s" % pods)
        for i in pods:
            for j in changes:

                sql_s = "SELECT sum(\"value\") FROM \"change\" WHERE \"type\" = \'pod_container\' " \
                        "AND \"namespace_name\" =~ /%s$/ " \
                        "AND \"pod_name\" =~ /%s$/ " \
                        "AND time > now() - 15m GROUP BY time(1m), \"container_name\" fill(null)&epoch=ms" % (namespace,
                                                                                                              i)
                url1 = STATICHTTP + sql_s
                url = url1.replace("change", j)
                res = json.loads(urllib.urlopen(url).read())
                log.info("xxxx===%s" % res)
                x = res.get("results")

                if x is not None:

                    try:
                        xx = x[0].get("series")[0].get("name")
                        log.info("hhh===%s" % xx)

                        if xx == "cpu/usage_rate":
                            xxx = x[0].get("series")[0].get("values")

                            if cnt_c == 0:
                                cpu_result = xxx
                                cnt_c += 1
                            else:
                                for g in a:
                                    if cpu_result[g][1] is None or cpu_result[g][1] == "":
                                        cpu_result[g][1] = float(xxx[g][1])
                                    if xxx[g][1] is None or xxx[g][1] == "":
                                        pass
                                    else:
                                        cpu_result[g][1] = float(cpu_result[g][1]) + float(xxx[g][1])
                                    cnt_c += 1

                        if xx == "cpu/limit":
                            cpu_limit = int(cpu_limit) + abs(x[0].get("series")[0].get("values")[1][1])

                        if xx == "memory/usage":
                            # memory_usage = int(memory_usage) + abs(int(x[0].get("series")[0].get("values")[1][1]))
                            xxx = x[0].get("series")[0].get("values")

                            if cnt_m == 0:
                                memory_result = xxx
                                cnt_m += 1
                            else:
                                for g in a:
                                    if memory_result[g][1] is None or memory_result[g][1] == "":
                                        memory_result[g][1] = float(xxx[g][1])
                                    if xxx[g][1] is None or xxx[g][1] == "":
                                        pass
                                    else:
                                        memory_result[g][1] = float(memory_result[g][1]) + float(xxx[g][1])
                                    cnt_m += 1

                        if xx == "memory/limit":
                            memory_limit = int(memory_limit) + abs(int(x[0].get("series")[0].get("values")[1][1]))

                    except Exception, e:
                        log.error("error, reason=%s" % e)

        resu = {"cpu_usage": cpu_result, "cpu_limit": cpu_limit, "memory_usage": memory_result,
                "memory_limit": memory_limit}
        return resu

    def get_broad_message(self, parameters):
        pods = []
        to_server = {"namespace": parameters.get("project_uuid"), 'rtype': 'pods'}
        try:

            resu = self.kuber.get_pod_messages(to_server).get('items')
            for i in resu:
                log.info('aaaaaaaaa===%s' % i)
                if i.get("status").get("phase") == "Running" or resu.get("status").get("phase") == "Ready":
                    pod_name = i.get("metadata").get("name")
                    pods.append(pod_name)
                else:
                    log.info("important message: in this namespace, some pods not running!!!")

        except Exception, e:
            log.error("query the pods error,reason=%s" % e)

        to = {"namespace": parameters.get("project_uuid"), "pods": pods}
        res = self.console(to)
        log.info(res)

        # if res.get("cpu_limit") != 0 and res.get("cpu_usage") is not None and res.get("cpu_limit") is not None:
        #     cpu_b = abs(int(res.get("cpu_usage")))/abs(int(res.get("cpu_limit")))

        # else:
        #     cpu_b = 0
        # if res.get("memory_limit") != 0 and res.get("memory_limit") is not None and res.get("memory_usage") is not None:
        #     memory_b = abs(int(res.get("memory_usage")))/abs(int(res.get("memory_limit")))
        # else:
        #     memory_b = 0
        # cpu_b = str(100-cpu_b*100) + "%"
        # memory_b = str(100-memory_b*100) + "%"
        # bb = {"cpu_limit": res.get("cpu_limit")/200, "cpu_usage": res.get("cpu_usage")/200,
        #       "memory_limit": res.get("memory_limit")/1000000, "memory_usage": res.get("memory_usage")/1000000}
        # aa = {"cpu_b": cpu_b, "memory_b": memory_b}
        # aa.update(bb)

        bb = {"cpu_usage": res.get("cpu_usage"), "memory_usage": res.get("memory_usage")}
        return request_result(0, bb)
