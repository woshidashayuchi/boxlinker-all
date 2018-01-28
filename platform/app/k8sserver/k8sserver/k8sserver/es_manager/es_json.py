#! /usr/bin python
# -*- coding:utf8 -*-
# Date:2016/8/9
# Author:wang-xf

from es_logs import get_index
import json
from now_time import get_now_time_ymd, get_now_time_ss_z
import os
from common.logs import logging as log


def create_esjson(json_list, log_info):
    namespace = json_list.get("metadata").get('namespace')
    service_name = json_list.get("metadata").get('name')

    host = "http://elasticsearch:9200"
    rtype = 'fluentd'
    log_dict = get_index(json_list, log_info)
    es_url = host + '/' + 'logstash-' + get_now_time_ymd(part='.') + '/' + rtype
    log.info('es url--url is: %s' % es_url)
    msg_json = {
        "log": json.dumps(log_dict),
        "kubernetes":
            {
                "namespace_name": "%s" % service_name + namespace,
                "pod_id": "%s" % service_name + namespace,
                "pod_name": "%s" % service_name + namespace,
                "container_name": "%s" % service_name + namespace,
                "labels":
                    {
                        "logs": "%s" % service_name + namespace
                    },
            },
        "@timestamp": str(get_now_time_ss_z())
    }

    return msg_json, es_url
