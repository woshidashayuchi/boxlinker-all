# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import json

from authServer.tools.logs import logging as log

from authServer.code_build.common.single import Singleton
from authServer.pyTools.tools.codeString import request_result

from authServer.code_build.git_clone import auto_build
from authServer.code_build.auto_build import auto_build_two


class RabbitResponse():
    def __init__(self):
        print 'sss'

    def manager(self, jsonstr):

        print 'RabbitResponse manager'
        dict_t = json.loads(jsonstr)
        print dict_t

        try:
            # auto_build(dict_t)
            auto_build_two(dict_t)
        except Exception as msg:
            print 'RabbitResponse have Exception'
            print msg.message
        return request_result(0)


class RabbitmqResponse(object):

    __metaclass__ = Singleton

    def __init__(self, queue_name):

        self.storage_manager = RabbitResponse()

    def rpc_exec(self, json_data):
        try:
            response = self.storage_manager.manager(json_data)
            print response

            return response

        except Exception, e:
            print e.message
            print e.args
            log.error('RPC Server exec error: %s' % (e))
            return request_result(599)
