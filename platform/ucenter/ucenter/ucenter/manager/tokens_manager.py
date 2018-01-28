# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import uuid
import json
import time

from ucenter_common import passwd_encrypt

from common.logs import logging as log
from common.code import request_result
from common.parameters import parameter_check
from common.json_encode import CJsonEncoder
from common.md5_encrypt import md5_encrypt

from ucenter.db import ucenter_db


class TokensManager(object):

    def __init__(self):

        self.ucenter_db = ucenter_db.UcenterDB()

    def token_login(self, user_name, password):

        try:
            email = parameter_check(user_name, ptype='peml')
            user_name = self.ucenter_db.email_user_name(email)[0][0]
        except Exception, e:
            log.debug('Email account login error, reason=%s' % (e))

        try:
            user_info = self.ucenter_db.user_token_info(user_name)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        try:
            user_uuid = user_info[0][0]
            passwd_db = user_info[0][1]
            salt = user_info[0][2]
            team_uuid = user_info[0][3]
            project_uuid = user_info[0][4]
        except Exception, e:
            log.warning('Get user token info error, '
                        'user_name=%s, reason=%s'
                        % (user_name, e))
            return request_result(201)

        passwd_user = passwd_encrypt(user_name, password, salt)
        if passwd_user != passwd_db:
            log.warning('user(%s) login error, password not correct'
                        % (user_name))
            return request_result(201)

        user_token = str(uuid.uuid4())
        token = md5_encrypt(user_token)

        try:
            self.ucenter_db.token_create(
                 token, user_uuid, team_uuid, project_uuid)
        except Exception, e:
            log.error('Database insert error, reason=%s' % (e))
            return request_result(401)

        result = {
                     "user_token": user_token
                 }

        return request_result(0, result)

    def token_switch(self, user_token,
                     team_uuid, project_uuid=None):

        u_token_check = self.token_check(user_token)
        if u_token_check['status'] != 0:
            log.warning('Token auth error, token=%s' % (user_token))
            return request_result(201)
        user_uuid = u_token_check['result']['user_uuid']

        if project_uuid is None:
            try:
                project_uuid = self.ucenter_db.project_default(
                                    team_uuid)[0][0]
            except Exception, e:
                log.error('Database select error, reason=%s' % (e))
                return request_result(404)

        try:
            project_check = self.ucenter_db.project_team_check(
                                 project_uuid, team_uuid)[0][0]
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        if project_check == 0:
            log.warning('Token switch error, project(%s) not in team(%s)'
                        % (project_uuid, team_uuid))
            return request_result(202,
                                  'Token switch error, project not in team')

        orga_token = str(uuid.uuid4())
        token = md5_encrypt(orga_token)

        try:
            self.ucenter_db.token_create(
                 token, user_uuid, team_uuid, project_uuid)
        except Exception, e:
            log.error('Database insert error, reason=%s' % (e))
            return request_result(401)

        result = {
                     "orga_token": orga_token
                 }

        return request_result(0, result)

    def token_check(self, user_token):

        token = md5_encrypt(user_token)
        try:
            token_info = self.ucenter_db.token_check(token)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        try:
            user_uuid = token_info[0][0]
            team_uuid = token_info[0][1]
            project_uuid = token_info[0][2]
            user_name = token_info[0][3]
        except Exception, e:
            log.warning('Token authentication failure, token=%s'
                        % (user_token))
            return request_result(201)

        try:
            team_priv = self.ucenter_db.team_priv(
                             user_uuid, team_uuid)[0][0]
        except Exception, e:
            log.info('Database select error, reason=%s' % (e))
            team_priv = None

        try:
            project_priv = self.ucenter_db.project_priv(
                                user_uuid, project_uuid)[0][0]
        except Exception, e:
            log.info('Database select error, reason=%s' % (e))
            project_priv = None

        try:
            self.ucenter_db.token_update(token)
        except Exception, e:
            log.error('Database update error, reason=%s' % (e))
            return request_result(403)

        result = {
                     "user_uuid": user_uuid,
                     "user_name": user_name,
                     "team_uuid": team_uuid,
                     "team_priv": team_priv,
                     "project_uuid": project_uuid,
                     "project_priv": project_priv
                 }

        return request_result(0, result)

    def token_delete(self, user_token):

        token = md5_encrypt(user_token)
        try:
            self.ucenter_db.token_delete(token)
        except Exception, e:
            log.error('Database delete error, reason=%s' % (e))
            return request_result(402)

        return request_result(0)
