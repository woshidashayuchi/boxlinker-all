# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 17/5/15 下午1:47

from common.logs import logging as log
from common.code import request_result
from db.service_db import AdminServicesDB


class AdminServiceManager(object):
    def __init__(self):
        self.admin_services = AdminServicesDB()

    def get_all_services(self):
        result = []
        try:
            db_ret = self.admin_services.get_all_no_stopping_svc()
            for i in db_ret:
                service_uuid = i[0]
                project_uuid = i[1]
                service_name = i[2]
                inner = {'service_uuid': service_uuid, 'project_uuid': project_uuid, 'service_name': service_name}

                result.append(inner)
        except Exception, e:
            log.error('get the all service which is not stopping error, reason is: %s' % e)
            return request_result(404)

        return request_result(0, result)
