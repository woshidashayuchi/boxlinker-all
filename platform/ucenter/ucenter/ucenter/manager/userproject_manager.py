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


class UserProjectManager(object):

    def __init__(self):

        self.ucenter_db = ucenter_db.UcenterDB()

    @limit_check('projectusers')
    def user_project_add(self, token, user_uuid, role_uuid,
                         project_uuid, project_team):

        if role_uuid is None:
            role_uuid = 'user'

        try:
            user_team_check = self.ucenter_db.user_team_check(
                                   user_uuid, project_team)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        if user_team_check == 0:
            log.warning('Project add user denied, \
                        user_uuid=%s, project_team=%s'
                        % (user_uuid, project_team))
            return request_result(202)

        try:
            user_project_check = self.ucenter_db.user_project_check(
                                      user_uuid, project_uuid)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        if user_project_check == 0:
            try:
                self.ucenter_db.user_project_add(
                     user_uuid, project_uuid, role_uuid)
            except Exception, e:
                log.error('Database insert error, reason=%s' % (e))
                return request_result(401)

        result = {
                     "user_uuid": user_uuid,
                     "project_uuid": project_uuid,
                     "project_role": role_uuid
                 }

        return request_result(0, result)

    def user_project_list(self, project_uuid, page_size, page_num):

        'show project user and role list'

        try:
            user_list_info = self.ucenter_db.user_project_list(
                                  project_uuid, page_size, page_num)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        project_user_list = user_list_info.get('project_user_list')
        count = user_list_info.get('count')

        t_user_list = []
        for user_info in project_user_list:
            user_uuid = user_info[0]
            user_name = user_info[1]
            project_role = user_info[2]
            create_time = user_info[3]
            update_time = user_info[4]

            v_user_info = {
                              "user_uuid": user_uuid,
                              "user_name": user_name,
                              "project_role": project_role,
                              "create_time": create_time,
                              "update_time": update_time
                          }

            v_user_info = json.dumps(v_user_info, cls=CJsonEncoder)
            v_user_info = json.loads(v_user_info)
            t_user_list.append(v_user_info)

        result = {"count": count}
        result['user_list'] = t_user_list

        return request_result(0, result)

    def user_project_update(self, project_uuid, project_priv,
                            n_user_uuid, n_role_uuid):

        try:
            now_project_priv = self.ucenter_db.project_priv(
                                    n_user_uuid, project_uuid)[0][0]
            if ('U' in now_project_priv) and (project_priv != 'CRUD'):
                raise(Exception('Operation denied'))
        except Exception, e:
            log.warning('Operation denied, operator project_priv=%s, \
                        user project_priv=%s, reason=%s'
                        % (project_priv, now_project_priv, e))
            return request_result(202)

        try:
            self.ucenter_db.user_project_update(
                 n_user_uuid, project_uuid, n_role_uuid)
        except Exception, e:
            log.error('Database update error, reason=%s' % (e))
            return request_result(403)

        result = {
                     "user_uuid": n_user_uuid,
                     "project_uuid": project_uuid,
                     "project_role": n_role_uuid
                 }

        return request_result(0, result)

    def user_project_delete(self, user_uuid, project_uuid,
                            project_priv, n_user_uuid):

        if n_user_uuid != user_uuid:
        # 执行管理员或群主踢人操作
            try:
                now_project_priv = self.ucenter_db.project_priv(
                                        n_user_uuid, project_uuid)[0][0]
                if ('U' in now_project_priv) and (project_priv != 'CRUD'):
                    raise(Exception('Operation denied'))
            except Exception, e:
                log.warning('Operation denied, operator project_priv=%s, \
                            user project_priv=%s, reason=%s'
                            % (project_priv, now_project_priv, e))
                return request_result(202)

        try:
            self.ucenter_db.user_project_del(n_user_uuid, project_uuid)
        except Exception, e:
            log.error('Database delete error, reason=%s' % (e))
            return request_result(402)

        return request_result(0)
