#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import requests

from conf import conf
from common.logs import logging as log
from common.code import request_result

requests.adapters.DEFAULT_RETRIES = 5


class K8sDriver(object):

    def __init__(self):

        self.get_pod_status_url = conf.K8S_POD_API
        self.get_events_url = conf.K8S_EVENTS_API

        with open(conf.TOKEN_PATH, 'r') as f:
            token = f.read()

        auth_info = "Bearer %s" % token
        self.headers = {"Authorization": auth_info}

    def rc_status_info(self, token=None):

        try:
            r = requests.get(self.get_pod_status_url,
                             headers=self.headers,
                             verify=False, timeout=5)
            log.debug('rc_status=%s' % r.text)
            return request_result(0, r.text)
        except Exception, e:
            log.error('requests k8s api error, reason=%s' % e)
            return request_result(103)

    def app_events_info(self, namespace):
        url = self.get_events_url+namespace+'/events'
        try:
            r = requests.get(url, headers=self.headers, verify=False, timeout=5)
            return request_result(0, r.text)
        except Exception, e:
            log.error('requests k8s api(events) error, reason=%s' % e)
            return request_result(103)