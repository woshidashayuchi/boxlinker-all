# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import json

from conf import conf
from common.logs import logging as log
from common.code import request_result
from common.json_encode import CJsonEncoder

from billing.db.billing_db import BillingDB


class LimitsManager(object):

    def __init__(self):

        self.balancecheck = conf.balance_check
        self.limitcheck = conf.limit_check
        self.billing_db = BillingDB()

    def limit_check(self, team_uuid, project_uuid,
                    user_uuid, resource_type, cost=None):

        result = {
                     "team_uuid": team_uuid,
                     "resource_type": resource_type
                 }

        if (self.balancecheck is True) and (cost is not None):
            try:
                balance = self.billing_db.balance_info(team_uuid)[0][0]
            except Exception, e:
                log.error('Database select error, reason=%s' % (e))
                return request_result(404)
            if float(balance) > float(cost):
                result['balance_check'] = 0
                balance_check = True
            else:
                balance_check = False

            if balance_check is False:
                try:
                    self.billing_db.voucher_check(
                                    team_uuid, cost)[0][0]
                    result['balance_check'] = 0
                except Exception:
                    result['balance_check'] = 1
        else:
            result['balance_check'] = 0

        if self.limitcheck is True:
            try:
                limit_info = self.billing_db.limit_info(
                                  team_uuid, resource_type)[0][0]
            except Exception, e:
                log.error('Database select error, reason=%s' % (e))
                return request_result(404)

            result['limit_check'] = limit_info
        else:
            result['limit_check'] = 0

        return request_result(0, result)

    def limit_list(self, page_size, page_num):

        try:
            limits_list_info = self.billing_db.limit_list(
                                    page_size, page_num)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        user_limits_list = limits_list_info.get('limits_list')
        count = limits_list_info.get('count')

        limits_list = []
        for limits_info in user_limits_list:
            team_level = limits_info[0]
            teams = limits_info[1]
            teamusers = limits_info[2]
            projects = limits_info[3]
            projectusers = limits_info[4]
            roles = limits_info[5]
            images = limits_info[6]
            services = limits_info[7]
            volumes = limits_info[8]
            create_time = limits_info[9]
            update_time = limits_info[10]

            v_limits_info = {
                                "team_level": team_level,
                                "teams": teams,
                                "teamusers": teamusers,
                                "projects": projects,
                                "projectusers": projectusers,
                                "roles": roles,
                                "images": images,
                                "services": services,
                                "volumes": volumes,
                                "create_time": create_time,
                                "update_time": update_time
                            }
            v_limits_info = json.dumps(v_limits_info, cls=CJsonEncoder)
            v_limits_info = json.loads(v_limits_info)
            limits_list.append(v_limits_info)

        result = {"limits_list": limits_list}
        result['count'] = count

        return request_result(0, result)

    def limit_update(self, team_level, resource_type, limit):

        # 提供系统管理员修改限额的接口，
        # 当前只能修改不同等级对应的限额
        try:
            self.billing_db.limit_update(
                 team_level, resource_type, limit)
        except Exception, e:
            log.error('Database update error, reason=%s' % (e))
            return request_result(403)

        result = {
                     "team_level": team_level,
                     "resource_type": resource_type,
                     "limit": limit
                 }

        return request_result(0, result)
