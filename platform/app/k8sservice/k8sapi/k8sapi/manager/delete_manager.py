# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/02/14

from common.logs import logging as log
from common.code import request_result
from db.service_db import ServiceDB
from driver.token_driver import TokenDriver
from common.operation_record import operation_record
from driver.kubernetes_driver import KubernetesDriver
from driver.billing_driver import BillingResource


class DeleteManager(object):

    def __init__(self):
        self.service_db = ServiceDB()
        self.kuber = KubernetesDriver()
        self.billing = BillingResource()
        self.token_driver = TokenDriver()

    @operation_record(resource_type='app', action='logical_delete')
    def service_delete(self, context, token, source_ip, resource_uuid):
        log.info('the data(in) when delete service....is: %s' % context)

        try:
            context = self.service_db.get_service_name(context)
        except Exception, e:
            log.error('get the service name error, reason=%s' % e)
            return request_result(404)

        try:
            ret_volume = self.kuber.update_volume_status(context)
            if ret_volume is False:
                log.error('update the volume status error')
                return request_result(503)
        except Exception, e:
            log.error('update volume status error, reason is: %s' % e)
            return request_result(503)

        team_name, project_name = self.token_driver.gain_team_name(context)
        if team_name is False:
            log.info('CREATE SERVICE ERROR WHEN GET THE PROJECT NAME FROM TOKEN...')
            return request_result(501)
        context['team_name'] = team_name
        context['project_name'] = project_name

        ret = self.kuber.delete_service(context)
        if ret is not True:
            return ret

        try:
            b_ret = self.billing.delete_billing(context)
            if not b_ret:
                log.error('update the billing resources error, result is: %s' % b_ret)
            log.info('delete billing success, result is: %s' % b_ret)
        except Exception, e:
            log.error('delete billing resource error, reason is: %s' % e)

        # try:
        #     ret_logic = self.service_db.phy_insert(context)
        #     if ret_logic is not None:
        #         return request_result(402)
        # except Exception, e:
        #     log.error('update the logic error, reason is: %s' % e)
        #     return request_result(402)

        try:
            ret_database = self.service_db.delete_all(context)
            if ret_database is not None:
                return request_result(402)
        except Exception, e:
            log.error('database delete error, reason=%s' % e)
            return request_result(402)

        return request_result(0, {'resource_name': context.get('service_name')})
