# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/02/10

from db.service_db import ServiceDB
from driver.rpcapi_client import KubernetesRpcClient
from common.limit import limit_check
from common.logs import logging as log
from common.code import request_result
from common.operation_record import operation_record
from driver.token_driver import TokenDriver
from driver.kubernetes_driver import KubernetesDriver
from driver.volume_driver import VolumeDriver
from driver.photo_driver import photo_dir
from driver.es_driver.to_es import post_es
from driver.image_driver import images_message_get


class CreateManager(object):

    def __init__(self):
        self.service_db = ServiceDB()
        self.krpc_client = KubernetesRpcClient()
        self.token_driver = TokenDriver()
        self.kuber_driver = KubernetesDriver()
        self.volume = VolumeDriver()

    def check_name(self, context):
        try:
            using_name_info = self.service_db.name_if_used_check(context)
            if len(using_name_info) != 0:
                for i in using_name_info:
                    service_name = i[0]
                    if service_name.replace('_', '-') == context.get('service_name').replace('_', '-'):
                        return False
                # return False
        except Exception, e:
            log.error('Database select error when check the name..., reason=%s' % e)
            return 'error'

        return True

    def infix_db(self, context):
        try:
            infix = self.service_db.infix_db(context)
            log.info('the infix result is %s,type is %s' % (infix, type(infix)))
            if infix is not None:
                return False

            service_uuid = self.service_db.get_service_uuid(context)
            log.info('get the service_uuid is: %s' % service_uuid)
        except Exception, e:
            log.error('Database infix error when create the service..., reason=%s' % e)
            return False

        return service_uuid

    def diff_infix_db(self, dict_data):
        try:
            rc_uuid = self.service_db.get_rc_uuid(dict_data)
        except Exception, e:
            log.error('Database error when get the rc_uuid...,reason=%s' % e)
            return False

        container = dict_data.get('container')
        env = dict_data.get('env')
        volume = dict_data.get('volume')

        if container is not None and len(container) != 0:
            for i in container:
                i['rc_uuid'] = rc_uuid
                try:
                    infix = self.service_db.container_infix_db(i)
                except Exception, e:
                    log.error('Database error when infix the containers...,reason=%s' % e)
                    return False

                if infix is not None:
                    return False

        if env is not None and len(env) != 0:
            for j in env:
                j['rc_uuid'] = rc_uuid
                try:
                    infix_env = self.service_db.env_infix_db(j)
                except Exception, e:
                    log.error('Database error when infix the env...,reason=%s' % e)
                    return False

                if infix_env is not None:
                    return False

        if volume is not None and len(volume) != 0:
            for l in volume:
                l['rc_uuid'] = rc_uuid
                try:
                    infix_volume = self.service_db.volume_infix_db(l)
                except Exception, e:
                    log.error('Database error when infix the volume...,reason=%s' % e)
                    return False

                if infix_volume is not None:
                    return False

        return True

    @operation_record(resource_type='app', action='create')
    @limit_check('services')
    def service_create(self, context, cost, token, source_ip, resource_name):
        log.info('the create service data is: %s' % context)

        if context.get('rtype') != 'lifecycle':
            check_name = self.check_name(context)
            if check_name is False:
                return request_result(301)
            if check_name == 'error':
                return request_result(404)

        team_name, project_name = self.token_driver.gain_team_name(context)
        if team_name is False:
            log.info('CREATE SERVICE ERROR WHEN GET THE PROJECT NAME FROM TOKEN...')
            return request_result(501)
        context['team_name'] = team_name
        context['project_name'] = project_name
        context['action'] = 'post'

        ret = self.kuber_driver.create_service(context)
        if ret is not True:
            log.info('kubernetes resource create result is: %s' % ret)
            return request_result(501)

        try:
            change_volume = self.volume.storage_status(context)
            if change_volume is False:
                log.info('VOLUME STATUS UPDATE ERROR,CHANGE_VOLUME RESULT IS: %s' % change_volume)
                return request_result(501)
        except Exception, e:
            log.error('change the volume status error, reason is:%s' % e)
            return request_result(501)

        if context.get('rtype') != 'lifecycle':
            try:
                image_name, image_version = images_message_get(context)
                context['image_name'] = image_name
            except Exception, e:
                log.error('get the image message error, reason is: %s' % e)
                return request_result(501)

            try:
                infix = self.infix_db(context)

                domain = self.kuber_driver.container_domain(context)
                context.update({'container': domain})
                diff = self.diff_infix_db(context)

            except Exception, e:
                log.error('resource in database error, reason=%s' % e)
                return request_result(401)

            if infix is False or diff is False:
                return request_result(401)

            try:
                context['service_uuid'] = infix
                photo_dir(context)
            except Exception, e:
                log.error('from the photo url make the photo for service error, reason is: ' % e)

            post_es(context, 'service is creating...please wait')
            return request_result(0, {'resource_uuid': infix})
        else:
            return request_result(0, {'resource_uuid': 'recovering...'})
