# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 17/3/9 下午1:59
import sys
p_path = sys.path[0] + '/..'
sys.path.append(p_path)
from common.logs import logging as log
from kubernetes.kapi import KApiMethods
from service_db import ServiceDB
from conf import conf
import requests
import json


class BillingResource(object):

    def __init__(self):
        self.billing_url = conf.BILLING_URL
        self.kuber_api = KApiMethods()
        self.service_db = ServiceDB()

    def get_pods_num(self, context):
        context['rtype'] = 'replicationcontrollers'
        try:
            ret = self.kuber_api.get_name_resource(context)
        except Exception, e:
            log.error('get the replicationcontroller resources error, reason is: %s' % e)
            return False

        pods_num = int(ret.get('spec').get('replicas'))

        return pods_num

    def base_element(self, context):
        pods_num = self.get_pods_num(context)
        header = {'token': context.get('token')}

        try:
            project_uuid, resource_uuid, cm_format, service_name = self.service_db.billing_for_create(context)
        except Exception, e:
            log.error('get the detail parameters error, reason is: %s' % e)
            raise Exception('get the detail parameters error')

        return pods_num, header, project_uuid, resource_uuid, cm_format, service_name

    def create_billing(self, context):
        to_billing = dict()

        pods_num, header, project_uuid, resource_uuid, cm_format, service_name = self.base_element(context)
        if pods_num == 0:
            to_billing['resource_status'] = 'off'
        else:
            to_billing['resource_status'] = 'on'

        try:
            to_billing['resource_uuid'] = resource_uuid
            to_billing['resource_name'] = service_name
            to_billing['resource_type'] = 'app'
            to_billing['resource_conf'] = str(int(cm_format[0]*pods_num)) + 'X'
        except Exception, e:
            log.error('struct the data to billing error, reason is: %s' % e)
            raise Exception('struct the data to billing error')

        try:
            log.info('the data when create billing resources is: %s' % to_billing)
            billing_ret = requests.post(self.billing_url, json.dumps(to_billing), headers=header, timeout=5)
            log.info('post the resource to billing result is: %s' % billing_ret.text)
            billing_ret = json.loads(billing_ret.text)

            if int(billing_ret.get('status')) == 0:
                return True
        except Exception, e:
            log.error('post the resource to billing error, reason is: %s' % e)
            raise Exception('post the resource to billing error')

    def update_billing(self, context):
        log.info('the data when update billing resources is: %s' % context)

        to_billing = dict()
        resource_uuid = context.get('service_uuid')
        try:
            pods_num, header, project_uuid, resource_uuid, cm_format, service_name = self.base_element(context)
            to_billing['resource_conf'] = str(int(context.get('container_cpu'))*pods_num) + 'X'
            to_billing['resource_status'] = context.get('resource_status')
            to_billing['team_uuid'] = context.get('team_uuid')
            to_billing['project_uuid'] = context.get('project_uuid')
            to_billing['user_uuid'] = context.get('user_uuid')
        except Exception, e:
            log.error('struct the data to billing error, reason is: %s' % e)
            raise Exception('struct the data to billing error')

        try:
            url = self.billing_url+'/%s' % resource_uuid
            billing_ret = json.loads(requests.post(url, json.dumps(to_billing), headers=header, timeout=5))
            if int(billing_ret.get('status')) == 0:
                return True
        except Exception, e:
            log.error('put the resource to billing error, reason is: %s' % e)
            raise Exception('put the resource to billing error')

    def delete_billing(self, context):
        log.info('the data when delete billing resource is: %s' % context)

        resource_uuid = context.get('service_uuid')

        try:
            pods_num, header, project_uuid, resource_uuid, cm_format, service_name = self.base_element(context)
        except Exception, e:
            log.error('struct the data to billing error, reason is: %s' % e)
            raise Exception('struct the data to billing error')

        try:
            url = self.billing_url+'/%s' % resource_uuid
            billing_ret = json.loads(requests.delete(url, headers=header, timeout=5))
            if int(billing_ret.get('status')) == 0:
                return True
        except Exception, e:
            log.error('delete the resource of billing error, reason is: %s' % e)
            raise Exception('delete the resource of billing error')
