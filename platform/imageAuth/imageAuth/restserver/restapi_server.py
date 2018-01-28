#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 17/2/6 17:31
"""


import sys
from time import sleep


from common.logs import logging as log
from imageAuth.restserver.restapi_register import rest_app_run



# 启动 restful 服务
def server_start():
    while True:
        try:
            log.info('Starting ImageRepo Restful API Server')
            rest_app_run()
        except Exception, e:
            log.error('ImageRepo RESTful API Server running error, reason=%s' % (e))
            sleep(4)


if __name__ == '__main__':
    server_start()
