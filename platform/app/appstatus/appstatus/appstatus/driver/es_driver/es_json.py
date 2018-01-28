#! /usr/bin python
# -*- coding:utf8 -*-
# Date:2016/8/9
# Author:wang-xf

from es_logs import get_index
import json
from now_time import get_now_time_ymd, get_now_time_ss_z
from conf import conf


def create_esjson(dict_data, log_info):
    host = "http://%s" % conf.ELASTIC_SEARCH
    rtype = 'fluentd'
    log_dict = get_index(dict_data, log_info)
    es_url = host + '/' + 'logstash-' + get_now_time_ymd(part='.') + '/' + rtype
    msg_json = {
        "log": json.dumps(log_dict),
        "kubernetes":
            {
                "namespace_name": "%s" % dict_data.get("project_uuid"),
                "pod_id": "%s" % dict_data.get('service_name').lower().replace('_', '-') +
                          dict_data.get('project_uuid'),
                "pod_name": "%s" % dict_data.get('service_name').lower().replace('_', '-') +
                            dict_data.get('project_uuid'),
                "container_name": "%s" % dict_data.get('service_name').lower().replace('_', '-') +
                                  dict_data.get('project_uuid'),
                "labels":
                    {
                        "logs": "%s" % dict_data.get('service_name').lower().replace('_', '-') +
                                dict_data.get("project_uuid")
                    },
            },
        "@timestamp": str(get_now_time_ss_z())
    }

    return msg_json, es_url
