# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import time
import uuid
import json

from common.logs import logging as log
from common.code import request_result
from common.json_encode import CJsonEncoder

from billing.db.billing_db import BillingDB


class OrdersManager(object):

    def __init__(self):

        self.billing_db = BillingDB()

    def order_create(self, user_uuid, team_uuid,
                     project_uuid, resource_uuid,
                     cost, status):

        order_uuid = str(uuid.uuid4())
        try:
            self.billing_db.order_insert(user_uuid, team_uuid,
                                         project_uuid, order_uuid,
                                         resource_uuid, cost, status)
        except Exception, e:
            log.error('Database insert error, reason=%s' % (e))
            return request_result(401)

        result = {
                     "user_uuid": user_uuid,
                     "team_uuid": team_uuid,
                     "project_uuid": project_uuid,
                     "order_uuid": order_uuid,
                     "resource_uuid": resource_uuid,
                     "cost": cost,
                     "status": status
                 }

        return request_result(0, result)

    def order_update(self, order_uuid, cost, status):

        result = {"order_uuid": order_uuid}

        if cost:
            try:
                self.billing_db.order_update_cost(order_uuid, cost)
            except Exception, e:
                log.error('Database update error, reason=%s' % (e))
                return request_result(403)
            result['cost'] = cost

        if status:
            try:
                self.billing_db.order_update_status(order_uuid, status)
            except Exception, e:
                log.error('Database update error, reason=%s' % (e))
                return request_result(403)
            result['status'] = status

        return request_result(0, result)

    def order_list(self, team_uuid,
                   start_time, end_time,
                   page_size, page_num):

        try:
            start_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                       time.localtime(float(start_time)))
            end_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                     time.localtime(float(end_time)))
            orders_list_info = self.billing_db.order_list(
                                    team_uuid, start_time, end_time,
                                    page_size, page_num)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        user_orders_list = orders_list_info.get('orders_list')
        count = orders_list_info.get('count')

        orders_list = []
        for orders_info in user_orders_list:
            team_uuid = orders_info[0]
            project_uuid = orders_info[1]
            user_uuid = orders_info[2]
            order_uuid = orders_info[3]
            resource_uuid = orders_info[4]
            cost = orders_info[5]
            status = orders_info[6]
            create_time = orders_info[7]
            update_time = orders_info[8]

            v_orders_info = {
                                "order_uuid": order_uuid,
                                "resource_uuid": resource_uuid,
                                "cost": cost,
                                "status": status,
                                "team_uuid": team_uuid,
                                "project_uuid": project_uuid,
                                "user_uuid": user_uuid,
                                "create_time": create_time,
                                "update_time": update_time
                            }

            v_orders_info = json.dumps(v_orders_info, cls=CJsonEncoder)
            v_orders_info = json.loads(v_orders_info)
            orders_list.append(v_orders_info)

        result = {"orders_list": orders_list}
        result['count'] = count

        return request_result(0, result)
