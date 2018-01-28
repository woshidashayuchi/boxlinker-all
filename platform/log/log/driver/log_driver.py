#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import os
import time
import requests

from conf import conf
from common.logs import logging as log
from common.code import request_result

requests.adapters.DEFAULT_RETRIES = 5


class LogDriver(object):

    def __init__(self):

        self.url = conf.kibana_log_api
        self.headers = {"kbn-version": "5.2.1"}

    def pod_log_info(self, label_value, date_time,
                     start_time, end_time):

        now_time = int(round(time.time()*1000))

        body = (' {"index": ["logstash-%s"], "ignore_unavailable": true, '
                ' "preference": %d} \n '
                ' {"size": 100, '
                ' "sort": [{"@timestamp": '
                ' {"order": "asc", "unmapped_type": "boolean"}}], '
                ' "query": {"bool": {"must": [{"query_string": '
                ' {"analyze_wildcard": false, "query":"*"}}, '
                ' {"match": {"kubernetes.labels.logs": '
                ' {"query": "%s", "type": "phrase"}}}, '
                ' {"range": {"@timestamp": {"gte": %d, "lte": %d, '
                ' "format": "epoch_millis"}}}], '
                ' "must_not": []}}, '
                ' "highlight": {"pre_tags": ["@kibana-highlighted-field@"], '
                ' "post_tags": ["@/kibana-highlighted-field@"], '
                ' "fields": {"*":{}}, "require_field_match": false, '
                ' "fragment_size": 2147483647}, '
                ' "_source": {"excludes": []}, '
                ' "aggs": {"2": {"date_histogram": '
                ' {"field": "@timestamp", "interval": "30s", '
                ' "time_zone": "Asia/Shanghai", "min_doc_count": 1}}}, '
                ' "stored_fields": ["*"], "script_fields": {}, '
                ' "docvalue_fields": ["@timestamp", "time"]} \n '
                % (str(date_time), now_time, label_value,
                   start_time, end_time))

        log.debug('body=%s, type=%s' % (body, type(body)))

        try:
            r = requests.post(self.url, headers=self.headers,
                              data=body, timeout=5)
            # log.debug('logs_info=%s' % (r.text))
            return request_result(0, r.text)
        except Exception, e:
            log.error('requests error, reason=%s' % (e))
            return request_result(103)
