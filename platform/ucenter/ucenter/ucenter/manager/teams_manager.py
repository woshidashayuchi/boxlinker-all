# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import uuid
import json
import time

from conf import conf
from common.logs import logging as log
from common.code import request_result
from common.json_encode import CJsonEncoder
from common.md5_encrypt import md5_encrypt
from common.limit_local import limit_check

from ucenter.db import ucenter_db
from ucenter.driver import ucenter_driver


class TeamsManager(object):

    def __init__(self):

        self.user_image = conf.user_image
        self.default_avatar = conf.default_avatar
        self.ucenter_db = ucenter_db.UcenterDB()
        self.ucenter_driver = ucenter_driver.UcenterDriver()

    @limit_check('teams')
    def team_create(self, token, team_name,
                    team_owner, team_desc=None):

        try:
            team_check = self.ucenter_db.team_duplicate_check(
                              team_name)[0][0]
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        if team_check != 0:
            log.warning('Team(%s) already exists' % (team_name))
            return request_result(301, 'Team(%s) already exists'
                                  % (team_name))

        team_uuid = str(uuid.uuid4())
        project_uuid = str(uuid.uuid4())

        user_token = str(uuid.uuid4())
        token = md5_encrypt(user_token)

        try:
            self.ucenter_db.token_create(
                 token, team_owner, team_uuid, project_uuid)
        except Exception, e:
            log.error('Database insert error, reason=%s' % (e))
            return request_result(401)

        level_init = self.ucenter_driver.level_init(
                          user_token).get('status')
        if int(level_init) != 0:
            log.error('Team(%s) level init failure' % (team_name))
            return request_result(599)

        balance_init = self.ucenter_driver.balance_init(
                            user_token).get('status')
        if int(balance_init) != 0:
            log.error('Team(%s) balance init failure' % (team_name))
            return request_result(599)

        try:
            self.ucenter_db.team_create(
                 team_uuid, team_name, team_owner,
                 team_desc, project_uuid)
        except Exception, e:
            log.error('Database insert error, reason=%s' % (e))
            return request_result(401)

        result = {
                     "team_uuid": team_uuid,
                     "team_name": team_name,
                     "team_owner": team_owner,
                     "team_desc": team_desc,
                     "project_uuid": project_uuid
                 }

        return request_result(0, result)

    def team_info_public(self, team_name):

        try:
            team_single_info = self.ucenter_db.team_info_public(team_name)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        team_uuid = team_single_info[0][0]
        team_name = team_single_info[0][1]
        team_owner = team_single_info[0][2]
        team_type = team_single_info[0][3]
        team_desc = team_single_info[0][4]
        status = team_single_info[0][5]
        create_time = team_single_info[0][6]
        update_time = team_single_info[0][7]

        v_team_info = {
                          "team_uuid": team_uuid,
                          "team_name": team_name,
                          "team_owner": team_owner,
                          "team_type": team_type,
                          "team_desc": team_desc,
                          "status": status,
                          "create_time": create_time,
                          "update_time": update_time
                      }

        v_team_info = json.dumps(v_team_info, cls=CJsonEncoder)
        result = json.loads(v_team_info)

        return request_result(0, result)

    def team_list(self, user_uuid, team_name,
                  name_check, uuid_info, public_info):

        if team_name:
            if name_check == 'true':
                result = self.ucenter_db.team_duplicate_check(
                              team_name)[0][0]

                return request_result(0, result)

            elif uuid_info == 'true':
                try:
                    team_info = self.ucenter_db.team_info_uuid(team_name)
                except Exception, e:
                    log.error('Database select error, reason=%s' % (e))
                    return request_result(404)

                team_uuid = team_info[0][0]
                team_name = team_info[0][1]
                team_owner = team_info[0][2]
                result = {
                             "team_uuid": team_uuid,
                             "team_name": team_name,
                             "team_owner": team_owner
                 }

                return request_result(0, result)

            elif public_info == 'true':

                return self.team_info_public(team_name)

        try:
            team_list_info = self.ucenter_db.team_list(user_uuid)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        t_team_list = []
        for team_info in team_list_info:
            team_uuid = team_info[0]
            team_name = team_info[1]
            team_owner = team_info[2]
            team_type = team_info[3]
            team_desc = team_info[4]
            status = team_info[5]
            create_time = team_info[6]
            update_time = team_info[7]
            role_name = team_info[8]

            v_team_info = {
                              "team_uuid": team_uuid,
                              "team_name": team_name,
                              "team_owner": team_owner,
                              "team_type": team_type,
                              "team_desc": team_desc,
                              "status": status,
                              "role_name": role_name,
                              "create_time": create_time,
                              "update_time": update_time
                          }

            v_team_info = json.dumps(v_team_info, cls=CJsonEncoder)
            v_team_info = json.loads(v_team_info)
            t_team_list.append(v_team_info)

        result = {"team_list": t_team_list}

        return request_result(0, result)

    def team_info(self, team_uuid, user_uuid):

        if self.user_image is True:
            # 获取用户头像存储地址
            ret = self.ucenter_driver.image_info(team_uuid)
            if int(ret.get('status')) == 0:
                team_avatar = ret.get('result')
            else:
                team_avatar = self.default_avatar
        else:
            team_avatar = self.default_avatar

        if (user_uuid != 'sysadmin'):
            try:
                user_team_check = self.ucenter_db.user_team_check(
                                       user_uuid, team_uuid)
            except Exception, e:
                log.error('Database select error, reason=%s' % (e))
                return request_result(404)

            if user_team_check == 0:
                return request_result(202)

        try:
            team_single_info = self.ucenter_db.team_info(team_uuid)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        team_name = team_single_info[0][0]
        team_owner = team_single_info[0][1]
        team_type = team_single_info[0][2]
        team_desc = team_single_info[0][3]
        status = team_single_info[0][4]
        create_time = team_single_info[0][5]
        update_time = team_single_info[0][6]

        v_team_info = {
                          "team_uuid": team_uuid,
                          "team_name": team_name,
                          "team_owner": team_owner,
                          "team_type": team_type,
                          "team_avatar": team_avatar,
                          "team_desc": team_desc,
                          "status": status,
                          "create_time": create_time,
                          "update_time": update_time
                      }

        v_team_info = json.dumps(v_team_info, cls=CJsonEncoder)
        result = json.loads(v_team_info)

        return request_result(0, result)

    def team_update(self, team_uuid, team_owner=None,
                    team_type=None, team_desc=None):

        try:
            team_type_check = self.ucenter_db.team_type(team_uuid)[0][0]
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        if team_type_check == 'system':
            log.warning('System team not allow update')
            return request_result(202)

        result = {"team_uuid": team_uuid}

        if team_owner:
            try:
                user_team_check = self.ucenter_db.user_team_check(
                                       team_owner, team_uuid)
            except Exception, e:
                log.error('Database select error, reason=%s' % (e))
                return request_result(404)

            if user_team_check == 0:
                log.warning('Team update owner denied, \
                            team_owner=%s, team_uuid=%s'
                            % (team_owner, team_uuid))
                return request_result(202)

            try:
                project_uuid = self.ucenter_db.project_default(
                                    team_uuid)[0][0]
                self.ucenter_db.project_update_owner(
                                project_uuid, team_owner)
                self.ucenter_db.team_update_owner(
                                team_uuid, team_owner)
            except Exception, e:
                log.error('Database update error, reason=%s' % (e))
                return request_result(403)
            result['team_owner'] = team_owner

        if (team_type == 'private') or (team_type == 'public'):
            try:
                self.ucenter_db.team_update_type(team_uuid, team_type)
            except Exception, e:
                log.error('Database update error, reason=%s' % (e))
                return request_result(403)
            result['team_type'] = team_type

        if team_desc:
            try:
                self.ucenter_db.team_update_desc(team_uuid, team_desc)
            except Exception, e:
                log.error('Database update error, reason=%s' % (e))
                return request_result(403)
            result['team_desc'] = team_desc

        return request_result(0, result)

    def team_delete(self, team_uuid):

        try:
            team_type = self.ucenter_db.team_type(team_uuid)[0][0]
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        if team_type == 'system':
            log.warning('System team not allow delete')
            return request_result(202)

        try:
            team_check = self.ucenter_db.team_check(team_uuid)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        if team_check <= 1:
            try:
                self.ucenter_db.team_delete(team_uuid)
            except Exception, e:
                log.error('Database delete error, reason=%s' % (e))
                return request_result(402)
        else:
            error_reason = "Team delete denied, there are users in the team"
            log.warning(error_reason)
            result = {"reason": error_reason}
            return request_result(202, result)
        return request_result(0)
