# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/02/14

from db.metal_work import MetalWork
from db.service_db import ServiceDB
from common.logs import logging as log
from common.code import request_result
from driver.kubernetes_driver import KubernetesDriver


class QueryManager(object):

    def __init__(self):
        self.metal_work = MetalWork()
        self.k_driver = KubernetesDriver()
        self.service_db = ServiceDB()

    def service_list(self, context):

        if context.get('service_name') is None:
            try:
                query_result = self.metal_work.query_service(context)
                log.info('the query service list result is:%s, type is %s' % (query_result, type(query_result)))

                return query_result
            except Exception, e:
                log.error('query the message of the service list error....reason = %s' % e)
                raise

        else:
            try:
                query_result = self.metal_work.query_only_service(context)
                log.info('the query service list(have service_name) result is:%s, type is %s' % (query_result,
                                                                                                 type(query_result)))

                return query_result
            except Exception, e:
                log.error('query the message of the service list error....reason = %s' % e)
                raise

    def service_detail(self, context):

        try:
            ret = self.metal_work.service_detail(context)
        except Exception, e:
            log.error('get the service detail message error, reason=%s' % e)
            raise

        return ret

    def pod_message(self, context):
        try:
            context = self.service_db.get_service_name(context)
        except Exception, e:
            log.error('get the service_name based on uuid error, reason=%s' % e)
            raise

        try:
            ret = self.k_driver.get_pod_name(context)
        except Exception, e:
            log.error('get the service detail message error, reason=%s' % e)
            raise

        return ret

    def check_name_use_or_not(self, context):

        try:
            if context.get('rtype') == 'service':
                using_name_info = self.service_db.name_if_used_check(context)
                if len(using_name_info) != 0:
                    for i in using_name_info:
                        service_name = i[0]
                        if service_name.replace('_', '-') == context.get('service_name').replace('_', '-'):
                            return request_result(0, 1)

            else:
                ret_http = self.service_db.get_http_domain(context)
                domain = self.service_db.domain_list(context)
                if int(ret_http[0][0]) != 0 or not domain:
                    return request_result(0, 1)
        except Exception, e:
            log.error('Database select error when check the name..., reason=%s' % e)
            return request_result(404)

        return request_result(0, 0)
