# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 17/3/9 下午6:15

from common.logs import logging as log
from common.mysql_base import MysqlInit
from common.logs import logging as log
from time import sleep


class ServiceDB(MysqlInit):
    def __init__(self):
        super(ServiceDB, self).__init__()

    def billing_for_create(self, dict_data):
        project_uuid = dict_data.get('metadata').get('namespace')
        service_name = dict_data.get('metadata').get('name')

        sql = "select a.uuid, b.cm_format from font_service a, replicationcontrollers b WHERE " \
              "a.project_uuid='%s' and a.service_name='%s' AND a.rc_uuid=b.uuid" % (project_uuid, service_name)
        log.info('create the service, get the message for the billings sql is: %s' % sql)
        try:
            sleep(2)
            ret = super(ServiceDB, self).exec_select_sql(sql)

            log.info('for billing,--------%s' % type(ret))
            log.info(ret)
            # log.info('for billing,select the database, get the data is: %s' % ret)
        except Exception, e:
            log.error('exec the select sql error, reason is: %s' % e)
            raise Exception(e)

        # log.info('the database select result is: %s' % ret)
        if len(ret[0]) == 0:
            return False

        else:
            resource_uuid = ret[0][0]
            cm_format = ret[0][1]

            return project_uuid, resource_uuid, cm_format, service_name
