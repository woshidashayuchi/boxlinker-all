# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/02/07

import sys
p_path = sys.path[0] + '/..'
sys.path.append(p_path)

from common.logs import logging as log
from common.acl import acl_check
from common.code import request_result
from common.parameters import parameter_check
from manager.recover_manager import RecoverManager


class KubernetesRpcAPI(object):

    def __init__(self):
        self.recover = RecoverManager()

    @acl_check
    def service_create(self, context, parameters):
        log.info('rpc server get the data is : %s' % parameters)

        token = parameters.get('token')
        cost = parameters.get('cost')

        return self.recover.create_apps(token, context, parameters, cost)

    @acl_check
    def service_query(self, context, parameters):
        try:
            ret = self.recover.service_list(parameters)
            log.info('get the service list result is: %s, type is: %s' % (ret, type(ret)))
            return ret
        except Exception, e:
            log.error('get the service list error, reason is: %s' % e)
            return request_result(404)

    @acl_check
    def service_delete(self, context, parameters):
        ret = self.recover.physics_del(parameters)
        return ret
