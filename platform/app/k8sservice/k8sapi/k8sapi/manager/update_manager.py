# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/02/17

from common.logs import logging as log
from common.code import request_result
from db.service_db import ServiceDB
from driver.token_driver import TokenDriver
from driver.kubernetes_driver import KubernetesDriver
from driver.volume_driver import VolumeDriver
from driver.billing_driver import BillingResource
from common.operation_record import operation_record


class UpdateManager(object):

    def __init__(self):
        self.kuber = KubernetesDriver()
        self.service_db = ServiceDB()
        self.token_driver = TokenDriver()
        self.volume = VolumeDriver()
        self.billing = BillingResource()

    def identify_change_uuid(self, context):
        try:
            uuids = self.service_db.get_uuid_from_admin(context)
            if len(uuids[0]) != 0:
                team_uuid = uuids[0][0]
                project_uuid = uuids[0][1]
            else:
                return False
        except Exception, e:
            log.error('get the team_uuid and project_uuid for admin error, reason is: %s' % e)
            return False

        new_dict = {'team_uuid': team_uuid, 'project_uuid': project_uuid}
        context.update(new_dict)

        return context

    @operation_record(resource_type='app', action='update')
    def service_update(self, context, token, source_ip, resource_uuid):
        log.info('the data(in) when update service....is: %s' % context)
        try:
            if context.get('rtype') != 'identify':
                context = self.service_db.get_service_name(context)
        except Exception, e:
            log.error('get the service name error, reason=%s' % e)
            return request_result(404)

        try:
            if context.get('rtype') == 'identify':
                context = self.identify_change_uuid(context)
            team_name, project_name = self.token_driver.gain_team_name(context)
            if team_name is False:
                log.info('CREATE SERVICE ERROR WHEN GET THE PROJECT NAME FROM TOKEN...')
                return request_result(501)
        except Exception, e:
            log.error('get the team name, project name error, reason is: %s' % e)
            return request_result(502)
        context['team_name'] = team_name
        context['project_name'] = project_name

        try:
            result_old = self.kuber.update_volume_status(context)
            context['action'] = 'post'
            result_new = self.volume.storage_status(context)
            if result_old is False or result_new is False:
                return request_result(502)
        except Exception, e:
            log.error('update volume error, reason=%s' % e)
            return request_result(502)

        try:
            context = self.service_db.get_service_name(context)
        except Exception, e:
            log.error('get the service name error, reason=%s' % e)
            return request_result(404)

        ret = self.kuber.update_main(context)

        if ret is not True:
            return ret

        if context.get('rtype') == 'cm' or context.get('rtype') == 'telescopic' or \
                context.get('rtype') == 'status':
            try:
                b_ret = self.billing.update_billing(context)
                if not b_ret:
                    log.error('update the billing resources error, result is: %s' % b_ret)
            except Exception, e:
                log.error('update the billing resources error, reason is: %s' % e)

        return request_result(0, {'resource_name': context.get('service_name')})

