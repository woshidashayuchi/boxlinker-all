# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/02/07

import sys
p_path = sys.path[0] + '/..'
sys.path.append(p_path)

import json
from common.logs import logging as log
from kubernetes.kapi import KApiMethods
from es_manager.to_es import post_es
from billing_manager.billing_manager import BillingResource


class KubernetesRpcAPIs(object):

    def __init__(self):
        self.kubernetes = KApiMethods()
        self.billing = BillingResource()

    def service_crea(self, context, parameters=None):
        log.info('create the service base data is: %s' % context)
        ret = dict()
        try:
            token = context.pop('token')
            user_uuid = context.pop('user_uuid')
            ret = self.kubernetes.post_namespace_resource(context)
            ret = json.loads(ret)

            context['token'] = token
            context['user_uuid'] = user_uuid
            if ret.get('kind') != 'ReplicationController' and ret.get('kind') != 'Service' and \
                    ret.get('kind') != 'ConfigMap':
                log.info('CREATE SERVICE ERROR... result is:%s, type is:%s' % (ret, type(ret)))
        except Exception, e:
            log.error('create the service(kubernetes) error, reason=%s' % e)

        if ret.get('kind') == 'ReplicationController':
            try:
                billing_ret = self.billing.create_billing(context)
                if billing_ret is not True:
                    log.error('create the billing resources error')
            except Exception, e:
                log.error('create the billing resources error, reason is: %s' % e)

        log.info('create service success, result is:%s, type is: %s' % (ret, type(ret)))
        post_es(context, 'scheduling...')

    def ns_show(self, context, parameters=None):
        try:
            log.info('getting the namespace message...')
            return self.kubernetes.show_namespace(context)
        except Exception, e:
            log.error('get the namespace(kubernetes) error, reason=%s' % e)

    def ns_cre(self, context, parameters=None):
        try:
            return self.kubernetes.post_namespace(context)
        except Exception, e:
            log.error('create the namespace(kubernetes) error, reason=%s' % e)

    def svc_account_show(self, context, parameters=None):

        try:
            return self.kubernetes.get_account(context)
        except Exception, e:
            log.error('get the service account(kubernetes) error, reason=%s' % e)

    def secret_cre(self, context, parameters=None):
        try:
            return self.kubernetes.post_secret(context)
        except Exception, e:
            log.error('create the secret(kubernetes) error, reason=%s' % e)

    def svc_account_create(self, context, parameters=None):
        try:
            return self.kubernetes.post_account(context)
        except Exception, e:
            log.error('create the account(kubernetes) error, reason=%s' % e)

    def svc_delete(self, context, parameters=None):
        try:
            return self.kubernetes.delete_name_resource(context)
        except Exception, e:
            log.error('delete the service(kubernetes) error, reason=%s' % e)

    def pods_messages(self, context, parameters=None):
        try:
            return self.kubernetes.get_namespace_resource(context)
        except Exception, e:
            log.error('get pods messages(kubernetes) error, reason=%s' % e)

    def svc_update(self, context, parameters=None):
        try:
            return self.kubernetes.put_name_resource(context)
        except Exception, e:
            log.error('update service(%s) error, reason=%s' % (context.get('rtype'), e))

    def get_one_re(self, context, parameters=None):
        try:
            return self.kubernetes.get_name_resource(context)
        except Exception, e:
            log.error('get resource(%s) error, reason=%s' % (context.get('rtype'), e))

    def delete_ns(self, context, parameters=None):
        try:
            return self.kubernetes.delete_namespace(context)
        except Exception, e:
            log.error('delete the namespace error, reason is: %s' % e)
            return False

    def default_ingress(self, context, parameters=None):
        token = context.pop('token')
        user_uuid = context.pop('user_uuid')
        try:
            ret = self.kubernetes.post_ingress(context)

            context['token'] = token
            context['user_uuid'] = user_uuid

            if ret.get('kind') != 'Ingress':
                log.error('create the ingress result is: %s' % ret)
                post_es(context, 'load create failure...')
        except Exception, e:
            log.error('create the default ingress error, reason is: %s' % e)

    def get_default_ingress(self, context, parameters=None):
        try:
            return self.kubernetes.get_ingress(context)
        except Exception, e:
            log.error('get the default ingress message error, reason is: %s' % e)
            return False

    def update_ingress(self, context, parameters=None):
        try:
            return self.kubernetes.update_ingress(context)
        except Exception, e:
            log.error('update the ingress error, reason is: %s' % e)

    def update_secret(self, context, parameters=None):
        try:
            context['rtype'] = 'secrets'
            return self.kubernetes.put_name_resource(context)
        except Exception, e:
            log.error('update the secret error, reason is: %s' % e)
