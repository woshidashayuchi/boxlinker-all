# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 17/4/11 上午9:58

from common.logs import logging as log
from db.service_db import ServiceDB
from common.code import request_result
from driver.billing_driver import BillingResource


class CheckManager(object):

    def __init__(self):
        self.service_db = ServiceDB()
        self.billing_resource = BillingResource()

    @staticmethod
    def explain(in_tuple):
        add_list = []

        for c in in_tuple:
            resource_uuid = c[0]
            resource_name = c[1]
            team_uuid = c[3]
            project_uuid = c[4]
            user_uuid = c[5]
            resource_type = 'app'
            if c[2].lower() != 'stopping':
                resource_status = 'on'
                pods_num = c[6]
                cm_format = c[7][:-1]
                resource_conf = str(int(pods_num)*int(cm_format)) + 'x'
            else:
                resource_status = 'off'
                resource_conf = '0x'

            dict_add = {
                'resource_uuid': resource_uuid,
                'resource_name': resource_name,
                'team_uuid': team_uuid,
                'project_uuid': project_uuid,
                'user_uuid': user_uuid,
                'resource_type': resource_type,
                'resource_status': resource_status,
                'resource_conf': resource_conf
            }
            add_list.append(dict_add)

            return add_list

    def check_manager(self):
        # 24小时删除的服务
        try:
            svc_del = self.service_db.delete_in24()
        except Exception, e:
            log.error('get the delete service error, reason is: %s' % e)
            return request_result(404)

        delete_list = []
        for i in svc_del:
            service_uuid = i[0]
            v_svc_info = {
                            "resource_uuid": service_uuid
                          }

            delete_list.append(v_svc_info)

        # 24小时新增与更新的服务
        try:
            svc_create = self.service_db.create_in24()
            svc_update = self.service_db.update_in24()
        except Exception, e:
            log.error('get the update service in 24 hours error, reason is: %s' % e)
            return request_result(404)

        try:
            add_list = self.explain(svc_create)
            update_list = self.explain(svc_update)
        except Exception, e:
            log.error('explain the database data error, reason is: %s' % e)
            return request_result(404)

        try:
            ret = self.billing_resource.service_check(add_list, update_list, delete_list)
        except Exception, e:
            log.error('update the billing error, reason is: %s' % e)
            return request_result(505)

        return ret
