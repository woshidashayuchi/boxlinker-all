# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/02/07

from common.mysql_base import MysqlInit
from common.logs import logging as log


class ServiceDB(MysqlInit):

    def __init__(self):
        super(ServiceDB, self).__init__()

    def compare_image_id(self, image_name):
        sql = "select a.service_name, a.project_uuid from font_service a, replicationcontrollers b " \
              "WHERE a.rc_uuid=b.uuid AND b.image_name='%s' AND b.policy=%d AND lifecycle is NULL " \
              "UNION ALL (select a.service_name, a.project_uuid from font_service a, replicationcontrollers b " \
              "WHERE a.rc_uuid=b.uuid AND b.image_name='%s' AND b.policy=%d AND lifecycle ='' )" % (image_name, 1,
                                                                                                    image_name, 1)

        log.info('select the database sql is: %s' % sql)

        return super(ServiceDB, self).exec_select_sql(sql)

    def update_image_id(self, image_id, service_name, project_uuid):
        sql = "update replicationcontrollers SET image_id='%s' WHERE uuid=(SELECT rc_uuid from font_service " \
              "WHERE service_name='%s' AND project_uuid='%s')" % (image_id, service_name, project_uuid)

        log.info('update the database sql is: %s' % sql)

        return super(ServiceDB, self).exec_update_sql(sql)
