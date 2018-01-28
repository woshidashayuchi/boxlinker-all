# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>


from common.mysql_base import MysqlInit
from common.logs import logging as log


class ResourcesDB(MysqlInit):

    def __init__(self):

        super(ResourcesDB, self).__init__()

    def resource_count(self, resource_type,
                       team_uuid, project_uuid, user_uuid):

        if resource_type == 'teams':
            sql = "select count(*) from resources_acl \
                   where resource_type='team' and user_uuid='%s'" \
                  % (user_uuid)
        elif resource_type == 'teamusers':
            sql = "select count(*) from users_teams \
                   where team_uuid='%s'" \
                  % (team_uuid)
        elif resource_type == 'projects':
            sql = "select count(*) from resources_acl \
                   where resource_type='project' and team_uuid='%s'" \
                  % (team_uuid)
        elif resource_type == 'projectusers':
            sql = "select count(*) from users_projects \
                   where project_uuid='%s'" \
                  % (project_uuid)
        elif resource_type == 'roles':
            sql = "select count(*) from resources_acl \
                   where resource_type='role' and team_uuid='%s'" \
                  % (team_uuid)
        elif resource_type == 'images':
            sql = "select count(*) from resources_acl \
                   where resource_type='image' and team_uuid='%s'" \
                  % (team_uuid)
        elif resource_type == 'services':
            sql = "select count(*) from resources_acl \
                   where resource_type='service' and team_uuid='%s'" \
                  % (team_uuid)
        elif resource_type == 'volumes':
            sql = "select count(*) from resources_acl \
                   where resource_type='volume' and team_uuid='%s'" \
                  % (team_uuid)

        return super(ResourcesDB, self).exec_select_sql(sql)[0][0]
