# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

from common.logs import logging as log
from common.code import request_result
from common.acl import acl_check
from common.parameters import parameter_check
from common.token_ucenterauth import token_auth

from log.manager import k8slog_manager


class LogRpcManager(object):

    def __init__(self):

        self.k8slog_manager = k8slog_manager.K8sLogManager()

    @acl_check
    def log_label(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')

            label_value = parameters.get('label_value')
            date_time = parameters.get('date_time')
            start_time = parameters.get('start_time')
            end_time = parameters.get('end_time')

            label_value = parameter_check(label_value, ptype='pstr')
            date_time = parameter_check(date_time, ptype='pflt', exist='no')
            start_time = parameter_check(start_time, ptype='pflt', exist='no')
            end_time = parameter_check(end_time, ptype='pflt', exist='no')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.k8slog_manager.pod_log_list(
                    user_uuid, label_value=label_value,
                    date_time=date_time, start_time=start_time,
                    end_time=end_time)

    @acl_check
    def log_pod(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')

            pod_name = parameters.get('pod_name')
            date_time = parameters.get('date_time')
            start_time = parameters.get('start_time')
            end_time = parameters.get('end_time')

            pod_name = parameter_check(pod_name, ptype='pstr')
            date_time = parameter_check(date_time, ptype='pflt', exist='no')
            start_time = parameter_check(start_time, ptype='pflt', exist='no')
            end_time = parameter_check(end_time, ptype='pflt', exist='no')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.k8slog_manager.pod_log_list(
                    user_uuid, pod_name=pod_name,
                    date_time=date_time, start_time=start_time,
                    end_time=end_time)

    @acl_check
    def log_poll(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')

            label_value = parameters.get('label_value')
            start_time = parameters.get('start_time')

            label_value = parameter_check(label_value, ptype='pstr')
            start_time = parameter_check(start_time, ptype='pflt', exist='no')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.k8slog_manager.pod_log_list(
                    user_uuid, label_value=label_value,
                    start_time=start_time)
