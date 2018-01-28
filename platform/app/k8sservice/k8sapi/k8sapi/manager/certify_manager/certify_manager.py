# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 17/5/2 下午5:35

from common.logs import logging as log
from common.code import request_result
from db.service_db import CertifyDB
from common.code import request_result
from driver.certify_driver import CertifyDriver


class CertifyManager(object):
    def __init__(self):
        self.certify = CertifyDB()
        self.certify_driver = CertifyDriver()

    def create_manager(self, context):
        try:
            k_ret = self.certify_driver.create_cer_driver(context)
            if k_ret.get('status') != 0:
                return k_ret
        except Exception, e:
            log.error('create the secret to k8s error, reason is: %s' % e)
            return request_result(501)

        try:
            certify_uuid = self.certify.infix_certify(context)
            return request_result(0, {'resource_uuid': certify_uuid})
        except Exception, e:
            log.error('inner the certify message into database error, reason is: %s' % e)
            return request_result(401)

    def query_manager(self, context):
        certify_uuid = ''
        crt = ''
        tls_key = ''
        try:
            db_ret = self.certify.query_certify(context)
            for i in db_ret:
                crt = i[0]
                tls_key = i[1]
                certify_uuid = i[2]
            content = crt + ',tls.key:' + tls_key
        except Exception, e:
            log.error('query the certify message error, reason is: %s' % e)
            return request_result(404)

        return request_result(0, {"certify_uuid": certify_uuid, "certify": content})

    def update_manager(self, context):
        ks_ret = self.certify_driver.update_certify_driver(context)
        if ks_ret.get('status') != 0:
            return ks_ret

        try:
            self.certify.update_certify(context)
        except Exception, e:
            log.error('update the database when update the certify error, reason is: %s' % e)
            return request_result(403)

        return ks_ret
