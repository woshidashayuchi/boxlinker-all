# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import time
import json

from common.logs import logging as log
from common.code import request_result
from common.json_encode import CJsonEncoder
from common.time_log import time_log

from billing.db.billing_db import BillingDB


class BillsManager(object):

    def __init__(self):

        self.billing_db = BillingDB()

    def bill_create(self, user_uuid, team_uuid, project_uuid,
                    resource_uuid, resource_cost, voucher_cost):

        try:
            self.billing_db.bill_insert(user_uuid, team_uuid,
                                        project_uuid, resource_uuid,
                                        resource_cost, voucher_cost)
        except Exception, e:
            log.error('Database insert error, reason=%s' % (e))

        return

    def bill_list(self, team_uuid,
                  start_time, end_time,
                  page_size, page_num):

        try:
            start_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                       time.localtime(float(start_time)))
            end_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                     time.localtime(float(end_time)))
            bills_list_info = self.billing_db.bill_list(
                                   team_uuid, start_time, end_time,
                                   page_size, page_num)
            bills_total_info = self.billing_db.bill_total(
                                   team_uuid, start_time, end_time)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        resource_cost_total = bills_total_info[0][0]
        voucher_cost_total = bills_total_info[0][1]

        bills_total = {
                          "resource_cost": resource_cost_total,
                          "voucher_cost": voucher_cost_total
                      }

        result = {"bills_total": bills_total}

        user_bills_list = bills_list_info.get('bills_list')
        count = bills_list_info.get('count')

        bills_list = []
        for bills_info in user_bills_list:
            resource_uuid = bills_info[0]
            resource_name = bills_info[1]
            resource_conf = bills_info[2]
            resource_status = bills_info[3]
            resource_type = bills_info[4]
            team_uuid = bills_info[5]
            project_uuid = bills_info[6]
            user_uuid = bills_info[7]
            resource_cost = bills_info[8]
            voucher_cost = bills_info[9]

            v_bills_info = {
                               "team_uuid": team_uuid,
                               "project_uuid": project_uuid,
                               "user_uuid": user_uuid,
                               "resource_uuid": resource_uuid,
                               "resource_name": resource_name,
                               "resource_type": resource_type,
                               "resource_conf": resource_conf,
                               "resource_status": resource_status,
                               "resource_cost": resource_cost,
                               "voucher_cost": voucher_cost,
                               "start_time": start_time,
                               "end_time": end_time
                           }
            v_bills_info = json.dumps(v_bills_info, cls=CJsonEncoder)
            v_bills_info = json.loads(v_bills_info)

            bills_list.append(v_bills_info)

        result["bills_list"] = bills_list
        result['count'] = count

        return request_result(0, result)

    @time_log
    def bills_merge(self):

        # 为了防止服务器时间和数据库时间出现时区不统一的情况，
        # 该情况会导致刚写入bills库的数据被当成前一天的数据进行汇总，
        # 所以汇总合并时需要多减去8小时时区。
        now_time = time.time()
        yesterday_time = now_time - 115200
        yesterday = time.strftime("%Y-%m-%d",
                                  time.localtime(yesterday_time))
        start_time = str(yesterday) + ' ' + '00:00:00'
        end_time = str(yesterday) + ' ' + '23:59:59'
        log.info('bills merge exec, start_time=%s, end_time=%s'
                 % (start_time, end_time))

        # 获取前一天所有的资源id
        try:
            bills_resources_uuid = self.billing_db.bill_resource(
                                        start_time, end_time)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        # 使用for循环根据资源id合并数据，
        # 将每项资源一天的24条数据合并为一条，
        # 并写入bills_days表，然后删除bills中记录
        for resources_uuid in bills_resources_uuid:
            resource_uuid = resources_uuid[0]
            try:
                self.billing_db.bills_merge(
                     resource_uuid, start_time, end_time)
            except Exception, e:
                log.error('bills merge error, reason=%s' % (e))
                return
