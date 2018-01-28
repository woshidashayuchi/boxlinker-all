# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import uuid
import json
import time

from common.logs import logging as log
from common.code import request_result
from common.json_encode import CJsonEncoder
from common.limit_local import limit_check

from ucenter.db import ucenter_db


class ProjectsManager(object):

    def __init__(self):

        self.ucenter_db = ucenter_db.UcenterDB()

    @limit_check('projects')
    def project_create(self, token, project_name, project_owner,
                       project_team, project_desc=None):

        try:
            project_check = self.ucenter_db.project_duplicate_check(
                                 project_name, project_team)[0][0]
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        if project_check != 0:
            log.warning('Project(%s) already exists in Team(%s)'
                        % (project_name, project_team))
            return request_result(301, 'Project(%s) already exists in Team'
                                  % (project_name))

        project_uuid = str(uuid.uuid4())
        try:
            self.ucenter_db.project_create(
                 project_uuid, project_name, project_owner,
                 project_team, project_desc)
        except Exception, e:
            log.error('Database insert error, reason=%s' % (e))
            return request_result(401)

        result = {
                     "project_uuid": project_uuid,
                     "project_name": project_name,
                     "project_owner": project_owner,
                     "project_team": project_team,
                     "project_desc": project_desc
                 }

        return request_result(0, result)

    def project_list(self, user_uuid, team_uuid):

        try:
            project_list_info = self.ucenter_db.project_list(
                                     user_uuid, team_uuid)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        t_project_list = []
        for project_info in project_list_info:
            project_uuid = project_info[0]
            project_name = project_info[1]
            project_owner = project_info[2]
            project_team = project_info[3]
            project_type = project_info[4]
            project_desc = project_info[5]
            status = project_info[6]
            create_time = project_info[7]
            update_time = project_info[8]
            role_name = project_info[9]

            v_project_info = {
                                 "project_uuid": project_uuid,
                                 "project_name": project_name,
                                 "project_owner": project_owner,
                                 "project_team": project_team,
                                 "project_type": project_type,
                                 "project_desc": project_desc,
                                 "status": status,
                                 "role_name": role_name,
                                 "create_time": create_time,
                                 "update_time": update_time
                             }

            v_project_info = json.dumps(v_project_info, cls=CJsonEncoder)
            v_project_info = json.loads(v_project_info)
            t_project_list.append(v_project_info)

        result = {"project_list": t_project_list}

        return request_result(0, result)

    def project_info(self, project_uuid):

        try:
            project_single_info = self.ucenter_db.project_info(project_uuid)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        project_name = project_single_info[0][0]
        project_owner = project_single_info[0][1]
        project_team = project_single_info[0][2]
        project_type = project_single_info[0][3]
        project_desc = project_single_info[0][4]
        status = project_single_info[0][5]
        create_time = project_single_info[0][6]
        update_time = project_single_info[0][7]

        v_project_info = {
                             "project_uuid": project_uuid,
                             "project_name": project_name,
                             "project_owner": project_owner,
                             "project_team": project_team,
                             "project_type": project_type,
                             "project_desc": project_desc,
                             "status": status,
                             "create_time": create_time,
                             "update_time": update_time
                         }

        v_project_info = json.dumps(v_project_info, cls=CJsonEncoder)
        result = json.loads(v_project_info)

        return request_result(0, result)

    def project_update(self, project_uuid, team_uuid,
                       project_owner=None, project_desc=None):

        try:
            project_type = self.ucenter_db.project_type(project_uuid)[0][0]
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        if project_type == 'system':
            log.warning('System project not allow update')
            return request_result(202)

        result = {"project_uuid": project_uuid}

        if project_owner:

            try:
                user_team_check = self.ucenter_db.user_team_check(
                                       project_owner, team_uuid)
            except Exception, e:
                log.error('Database select error, reason=%s' % (e))
                return request_result(404)

            if user_team_check == 0:
                log.warning('Project update owner denied, \
                            project_owner=%s, team_uuid=%s'
                            % (project_owner, team_uuid))
                return request_result(202)

            try:
                self.ucenter_db.project_update_owner(
                                project_uuid, project_owner)
            except Exception, e:
                log.error('Database update error, reason=%s' % (e))
                return request_result(403)
            result['project_owner'] = project_owner

        if project_desc:
            try:
                self.ucenter_db.project_update_desc(project_uuid, project_desc)
            except Exception, e:
                log.error('Database update error, reason=%s' % (e))
                return request_result(403)
            result['project_desc'] = project_desc

        return request_result(0, result)

    def project_delete(self, project_uuid):

        try:
            project_type = self.ucenter_db.project_type(project_uuid)[0][0]
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        if project_type == 'system':
            log.warning('System project not allow delete')
            return request_result(202)

        try:
            project_check = self.ucenter_db.project_check(project_uuid)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        if project_check <= 1:
            try:
                self.ucenter_db.project_delete(project_uuid)
            except Exception, e:
                log.error('Database update error, reason=%s' % (e))
                return request_result(403)
        else:
            error_reason = ('Project delete denied, '
                            'there are users in the project.')
            log.warning(error_reason)
            result = {"reason": error_reason}
            return request_result(202, result)
        return request_result(0)
