# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 17/5/2 下午5:39

from common.logs import logging as log
from common.code import request_result
from rpcapi_client import CertifyRpcClient
import base64


class CertifyDriver(object):
    def __init__(self):
        self.rpc_client = CertifyRpcClient()

    @staticmethod
    def secret_json(context):
        namespace = context.get('project_uuid')
        crt = base64.b64encode(context.get('content').get('tls.crt'))
        tls_key = base64.b64encode(context.get('content').get('tls.key'))
        secret = {"apiVersion": "v1",
                  "kind": "Secret",
                  "metadata": {"name": "certify-https",
                               "namespace": namespace},
                  "type": "Opaque",
                  "data": {"tls.crt": crt,
                           "tls.key": tls_key}}

        return secret

    def create_cer_driver(self, context):
        try:
            secret_json = self.secret_json(context)
        except Exception, e:
            log.error('create the secret json error, reason is: %s' % e)
            return request_result(501)

        ret = self.rpc_client.create_certify(secret_json)

        if ret.get('kind') != 'Secret':
            return request_result(501)

        else:
            return request_result(0, {'resources_name': 'certify-https'})

    def update_certify_driver(self, context):
        try:
            secret_json = self.secret_json(context)
        except Exception, e:
            log.error('create the secret json error, reason is: %s' % e)
            return request_result(501)

        ret = self.rpc_client.update_certify(secret_json)

        if ret.get('result') != '<Response [200]>':
            log.error('update the secret result is: %s' % ret)
            return request_result(501)

        return request_result(0, {'resource_name': 'certify-https'})
