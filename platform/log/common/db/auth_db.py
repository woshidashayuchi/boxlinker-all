# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>


from common.mysql_base import MysqlInit
from common.logs import logging as log


class AuthDB(MysqlInit):

    def __init__(self):

        super(AuthDB, self).__init__()

    def admin_acl_check(self, resource_uuid):

        sql = "select admin_uuid from resources_acl where resource_uuid = '%s'" \
              % (resource_uuid)

        return super(AuthDB, self).exec_select_sql(sql)[0][0]

    def team_acl_check(self, resource_uuid):

        sql = "select team_uuid from resources_acl where resource_uuid = '%s'" \
              % (resource_uuid)

        return super(AuthDB, self).exec_select_sql(sql)[0][0]

    def project_acl_check(self, resource_uuid):

        sql = "select project_uuid from resources_acl where resource_uuid = '%s'" \
              % (resource_uuid)

        return super(AuthDB, self).exec_select_sql(sql)[0][0]

    def user_acl_check(self, resource_uuid):

        sql = "select user_uuid from resources_acl where resource_uuid = '%s'" \
              % (resource_uuid)

        return super(AuthDB, self).exec_select_sql(sql)[0][0]
