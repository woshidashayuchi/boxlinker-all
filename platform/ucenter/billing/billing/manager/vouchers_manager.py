# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import json
import time
import uuid

from common.logs import logging as log
from common.code import request_result
from common.json_encode import CJsonEncoder

from billing.db.billing_db import BillingDB


class VouchersManager(object):

    def __init__(self):

        self.billing_db = BillingDB()

    def voucher_create(self, user_uuid, denomination, invalid_time):

        voucher_uuid = str(uuid.uuid4())
        try:
            invalid_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                         time.localtime(float(invalid_time)))
            self.billing_db.voucher_insert(
                 voucher_uuid, user_uuid, denomination, invalid_time)
        except Exception, e:
            log.error('Database insert error, reason=%s' % (e))
            return request_result(401)

        result = {
                     "voucher_uuid": voucher_uuid,
                     "denomination": denomination,
                     "invalid_time": invalid_time
                 }

        return request_result(0, result)

    def voucher_active(self, voucher_uuid, user_uuid,
                       team_uuid, project_uuid, activator):

        try:
            voucher_check = self.billing_db.voucher_uuid_check(
                                 voucher_uuid)[0][0]
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        if voucher_check == 0:
            log.warning('Voucher(%s) not exists' % (voucher_uuid))
            return request_result(202)

        try:
            self.billing_db.voucher_active(
                 voucher_uuid, user_uuid,
                 team_uuid, project_uuid, activator)
        except Exception, e:
            log.error('Database update error, reason=%s' % (e))
            return request_result(403)

        result = {
                     "voucher_uuid": voucher_uuid,
                     "user_uuid": user_uuid,
                     "team_uuid": team_uuid,
                     "project_uuid": project_uuid,
                     "activator": activator
                 }

        return request_result(0, result)

    def voucher_distribute(self, voucher_uuid, accepter):

        try:
            voucher_status = self.billing_db.voucher_status(
                                  voucher_uuid)[0][0]
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        if voucher_status != 'unused':
            log.warning('Voucher distribute error, '
                        'voucher(%s) status=%s'
                        % (voucher_uuid, voucher_status))
            return request_result(202)

        try:
            self.billing_db.voucher_distribute(
                            voucher_uuid, accepter)
        except Exception, e:
            log.error('Database update error, reason=%s' % (e))
            return request_result(403)

        result = {
                     "voucher_uuid": voucher_uuid,
                     "accepter": accepter
                 }

        return request_result(0, result)

    def voucher_update(self, voucher_uuid, amount):

        try:
            self.billing_db.voucher_update(voucher_uuid, amount)
        except Exception, e:
            log.error('Database update error, reason=%s' % (e))

        return

    def voucher_list_admin(self, user_uuid, start_time,
                           end_time, page_size, page_num):

        try:
            start_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                       time.localtime(float(start_time)))
            end_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                     time.localtime(float(end_time)))
            vouchers_list_info = self.billing_db.voucher_list_admin(
                                      user_uuid, start_time, end_time,
                                      page_size, page_num)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        admin_vouchers_list = vouchers_list_info.get('vouchers_list')
        count = vouchers_list_info.get('count')

        vouchers_list = []
        for vouchers_info in admin_vouchers_list:
            voucher_uuid = vouchers_info[0]
            denomination = vouchers_info[1]
            balance = vouchers_info[2]
            active_time = vouchers_info[3]
            invalid_time = vouchers_info[4]
            status = vouchers_info[5]
            accepter = vouchers_info[6]
            activator = vouchers_info[7]
            create_time = vouchers_info[8]
            update_time = vouchers_info[9]
            team_uuid = vouchers_info[10]

            v_vouchers_info = {
                                  "voucher_uuid": voucher_uuid,
                                  "denomination": denomination,
                                  "balance": balance,
                                  "active_time": active_time,
                                  "invalid_time": invalid_time,
                                  "status": status,
                                  "team_uuid": team_uuid,
                                  "accepter": accepter,
                                  "activator": activator,
                                  "create_time": create_time,
                                  "update_time": update_time
                              }
            v_vouchers_info = json.dumps(v_vouchers_info, cls=CJsonEncoder)
            v_vouchers_info = json.loads(v_vouchers_info)
            vouchers_list.append(v_vouchers_info)

        result = {"count": count}
        result['vouchers_list'] = vouchers_list

        return request_result(0, result)

    def voucher_list_user(self, team_uuid, start_time,
                          end_time, page_size, page_num):

        try:
            start_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                       time.localtime(float(start_time)))
            end_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                     time.localtime(float(end_time)))
            vouchers_list_info = self.billing_db.voucher_list_user(
                                      team_uuid, start_time, end_time,
                                      page_size, page_num)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        user_vouchers_list = vouchers_list_info.get('vouchers_list')
        count = vouchers_list_info.get('count')

        vouchers_list = []
        for vouchers_info in user_vouchers_list:
            voucher_uuid = vouchers_info[0]
            user_uuid = vouchers_info[1]
            denomination = vouchers_info[2]
            balance = vouchers_info[3]
            active_time = vouchers_info[4]
            invalid_time = vouchers_info[5]
            status = vouchers_info[6]

            v_vouchers_info = {
                                  "voucher_uuid": voucher_uuid,
                                  "user_uuid": user_uuid,
                                  "denomination": denomination,
                                  "balance": balance,
                                  "status": status,
                                  "active_time": active_time,
                                  "invalid_time": invalid_time
                              }
            v_vouchers_info = json.dumps(v_vouchers_info, cls=CJsonEncoder)
            v_vouchers_info = json.loads(v_vouchers_info)
            vouchers_list.append(v_vouchers_info)

        result = {"count": count}
        result['vouchers_list'] = vouchers_list

        return request_result(0, result)

    def voucher_list_accept(self, user_name, page_size, page_num):

        try:
            vouchers_list_info = self.billing_db.voucher_list_accept(
                                      user_name, page_size, page_num)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        accept_vouchers_list = vouchers_list_info.get('vouchers_list')
        count = vouchers_list_info.get('count')

        vouchers_list = []
        for vouchers_info in accept_vouchers_list:
            voucher_uuid = vouchers_info[0]
            denomination = vouchers_info[1]
            invalid_time = vouchers_info[2]
            status = vouchers_info[3]

            v_vouchers_info = {
                                  "gift_type": "voucher",
                                  "voucher_uuid": voucher_uuid,
                                  "denomination": denomination,
                                  "status": status,
                                  "invalid_time": invalid_time
                              }
            v_vouchers_info = json.dumps(v_vouchers_info, cls=CJsonEncoder)
            v_vouchers_info = json.loads(v_vouchers_info)
            vouchers_list.append(v_vouchers_info)

        result = {"count": count}
        result['vouchers_list'] = vouchers_list

        return request_result(0, result)

    def voucher_list(self, user_uuid, team_uuid,
                     start_time, end_time,
                     page_size, page_num):

        try:
            self.billing_db.voucher_status_update()
        except Exception, e:
            log.error('Database update error, reason=%s' % (e))
            return request_result(403)

        if user_uuid == 'sysadmin':
            return self.voucher_list_admin(
                        user_uuid, start_time, end_time,
                        page_size, page_num)
        else:
            return self.voucher_list_user(
                        team_uuid, start_time, end_time,
                        page_size, page_num)
