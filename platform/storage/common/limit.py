# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import time
import json
import inspect
import requests

from conf import conf
from common.logs import logging as log
from common.code import request_result
from common.parameters import context_data
from common.token_ucenterauth import token_auth
from common.db import resources_db


requests.adapters.DEFAULT_RETRIES = 5
limit_url = '%s%s' % (conf.billing_api, '/api/v1.0/billing/limits')


def billing_limit_check(token, resource_type, cost):

    try:
        log.debug('Start billing limit check, '
                  'token=%s, resource_type=%s, cost=%s'
                  % (token, resource_type, cost))

        headers = {'token': token}
        body = {
                   "resource_type": resource_type,
                   "cost": cost
               }

        limit = requests.post(limit_url, headers=headers,
                              data=json.dumps(body),
                              timeout=5).json()

        log.debug('Billing limit result=%s' % (limit))

        status = limit['status']
        if status != 0:
            raise(Exception('Billing limit check error, '
                            'request code not equal 0'))
    except Exception, e:
        log.error('Billing limit local check error: reason=%s' % (e))
        raise(Exception('Billing limit check error'))

    return limit


def limit_check(resource_type):

    def _reslmt(func):

        def __reslmt(*args, **kwargs):

            try:
                func_args = inspect.getcallargs(func, *args, **kwargs)
                token = func_args.get('token')
                cost = func_args.get('cost')

                user_info = token_auth(token)['result']
                team_uuid = user_info.get('team_uuid')
                project_uuid = user_info.get('project_uuid')
                user_uuid = user_info.get('user_uuid')

                if user_uuid != 'sysadmin':
                    limit_info = billing_limit_check(
                                 token, resource_type, cost)
                    balance_check = limit_info['result']['balance_check']
                    if int(balance_check) != 0:
                        log.warning('Limit check denied, not enough balance')
                        return request_result(302)

                    limit_check = limit_info['result']['limit_check']
                    res_db = resources_db.ResourcesDB()
                    resource_count = res_db.resource_count(
                                            resource_type, team_uuid,
                                            project_uuid, user_uuid)
                    log.debug('billing_limit_check=%s, resource_count=%s'
                              % (limit_check, resource_count))
                    if int(resource_count) >= int(limit_check):
                        log.warning('Limit check denied, Team(%s) resource(%s) '
                                    'reach upper limit'
                                    % (team_uuid, resource_type))
                        return request_result(303)

                try:
                    return func(*args, **kwargs)
                except Exception, e:
                    log.error('function(%s) exec error, reason = %s'
                              % (func.__name__, e))
                    return request_result(601)
            except Exception, e:
                log.error('Limit check error, reason=%s' % (e))
                return request_result(303)

        return __reslmt

    return _reslmt
