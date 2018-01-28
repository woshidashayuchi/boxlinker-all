# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import uuid
import json
import time

from conf import conf
from common.logs import logging as log
from common.code import request_result
from common.json_encode import CJsonEncoder
from common.limit_local import limit_check

from ucenter.db import ucenter_db


class UserTeamManager(object):

    def __init__(self):

        self.ucenter_db = ucenter_db.UcenterDB()
        self.user_image = conf.user_image
        self.default_avatar = conf.default_avatar

    @limit_check('teamusers')
    def user_team_add(self, token, user_uuid,
                      team_uuid, team_role):

        if team_role is None:
            team_role = 'user'

        try:
            user_team_check = self.ucenter_db.user_team_check(
                                   user_uuid, team_uuid)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        if user_team_check == 0:
            try:
                self.ucenter_db.user_team_add(
                     user_uuid, team_uuid, team_role)
            except Exception, e:
                log.error('Database insert error, reason=%s' % (e))
                return request_result(401)

        result = {
                     "user_uuid": user_uuid,
                     "team_uuid": team_uuid,
                     "team_role": team_role
                 }

        return request_result(0, result)

    def user_team_list(self, team_uuid, page_size, page_num):

        'show team user and role list'

        try:
            user_list_info = self.ucenter_db.user_team_list(
                                  team_uuid, page_size, page_num)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        team_user_list = user_list_info.get('team_user_list')
        count = user_list_info.get('count')

        t_user_list = []
        for user_info in team_user_list:
            user_uuid = user_info[0]
            user_name = user_info[1]
            team_role = user_info[2]
            create_time = user_info[3]
            update_time = user_info[4]

            v_user_info = {
                              "user_uuid": user_uuid,
                              "user_name": user_name,
                              "team_role": team_role,
                              "create_time": create_time,
                              "update_time": update_time
                          }

            v_user_info = json.dumps(v_user_info, cls=CJsonEncoder)
            v_user_info = json.loads(v_user_info)
            t_user_list.append(v_user_info)

        result = {"count": count}
        result['user_list'] = t_user_list

        return request_result(0, result)

    def user_team_activate(self, user_uuid, team_uuid):

        try:
            self.ucenter_db.user_team_activate(
                 user_uuid, team_uuid)
        except Exception, e:
            log.error('Database update error, reason=%s' % (e))
            return request_result(403)

        result = {
                     "user_uuid": user_uuid,
                     "team_uuid": team_uuid
                 }

        return request_result(0, result)

    def user_team_update(self, team_uuid, team_priv,
                         n_user_uuid, n_role_uuid):

        try:
            now_team_priv = self.ucenter_db.team_priv(
                                 n_user_uuid, team_uuid)[0][0]
            if ('U' in now_team_priv) and (team_priv != 'CRUD'):
                raise(Exception('Operation denied'))
        except Exception, e:
            log.warning('Operation denied, operator team_priv=%s, \
                        user team_priv=%s, reason=%s'
                        % (team_priv, now_team_priv, e))
            return request_result(202)

        try:
            self.ucenter_db.user_team_update(
                 n_user_uuid, team_uuid, n_role_uuid)
        except Exception, e:
            log.error('Database update error, reason=%s' % (e))
            return request_result(403)

        result = {
                     "user_uuid": n_user_uuid,
                     "team_uuid": team_uuid,
                     "team_role": n_role_uuid
                 }

        return request_result(0, result)

    def user_team_delete(self, n_user_uuid, n_team_uuid,
                         user_uuid, team_priv):

        if n_user_uuid != user_uuid:
        # 执行管理员或群主踢人操作
            try:
                now_team_priv = self.ucenter_db.team_priv(
                                     n_user_uuid, n_team_uuid)[0][0]
                if ('U' in now_team_priv) and (team_priv != 'CRUD'):
                    raise(Exception('Operation denied'))
            except Exception, e:
                log.warning('Operation denied, operator team_priv=%s, \
                            user team_priv=%s, reason=%s'
                            % (team_priv, now_team_priv, e))
                return request_result(202)

        try:
            self.ucenter_db.user_team_del(n_user_uuid, n_team_uuid)
        except Exception, e:
            log.error('Database delete error, reason=%s' % (e))
            return request_result(402)

        return request_result(0)
