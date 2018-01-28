# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import json
import time

from time import sleep

from common.logs import logging as log
from common.code import request_result
from common.json_encode import CJsonEncoder
from log.driver import log_driver


class K8sLogManager(object):

    def __init__(self):

        self.log_driver = log_driver.LogDriver()

    def pod_log_list(self, user_uuid, label_value=None,
                     pod_name=None, date_time=None,
                     start_time=None, end_time=None):

        if date_time is None:
            date_time = time.strftime("%Y.%m.%d", time.localtime())
        else:
            date_time = time.strftime("%Y.%m.%d",
                                      time.gmtime(float(date_time)))

        if end_time is None:
            now_time = time.time()
            end_time = int(round(now_time*1000))

        if start_time is None:
            start_time = end_time - 300000

        start_time = int(start_time)
        end_time = int(end_time)
        ret = self.log_driver.pod_log_info(
                   label_value, date_time,
                   start_time, end_time)
        log.debug('label_value=%s, date_time=%s, '
                  'start_time=%s, end_time=%s'
                  % (label_value, date_time, start_time, end_time))
        log.debug('Log driver get log result, pod_log_info=%s' % (ret))
        status_code = int(ret['status'])
        if status_code != 0:
            return request_result(status_code)

        log_list_info = ret['result']
        log_list_info = json.loads(log_list_info)

        pod_logs_list = log_list_info['responses'][0]['hits']['hits']
        log.debug('pod_logs_list=%s' % (pod_logs_list))

        result = {}
        end_epoch_time = 0
        log_list = []
        for pod_log in pod_logs_list:
            epoch_time = pod_log['fields']['@timestamp'][0]
            log.debug('epoch_time=%s, type=%s'
                      % (epoch_time, type(epoch_time)))
            if epoch_time <= start_time:
                continue

            if epoch_time > end_epoch_time:
                end_epoch_time = epoch_time

            pod_log = pod_log['_source']
            log.debug('pod_log=%s, type=%s' % (pod_log, type(pod_log)))
            log.debug('user_uuid=%s' % (user_uuid))

            try:
                mlogs = json.loads(pod_log['log'])
                user_id = mlogs['log']['userid']
                log.debug('log_user_id=%s' % (user_id))
                if (user_uuid == 'sysadmin'):
                    plogs = mlogs
                    plogs['log_info'] = mlogs['log']['log_info']
                    del plogs['log']
                else:
                    if user_id == user_uuid:
                        plogs = mlogs
                        plogs['log_info'] = mlogs['log']['log_info']
                        del plogs['log']
                    else:
                        continue
            except Exception, e:
                try:
                    label_tag = label_value[0:9]
                    if (label_tag == 'boxlinker') \
                       and (user_uuid != 'sysadmin'):
                        continue
                except Exception, e:
                    pass

                log.debug('logs no user info')
                plogs = {}
                plogs['log_info'] = pod_log['log']

            log_time = pod_log['@timestamp']
            log.debug('log_time=%s' % (log_time))
            pod_name = pod_log['kubernetes']['pod_name']

            plogs['pod_name'] = pod_name
            plogs['log_time'] = log_time

            log_list.append(plogs)

        result['end_time'] = end_epoch_time
        result['logs_list'] = log_list

        return request_result(0, result)
