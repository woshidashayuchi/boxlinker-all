# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

from common.logs import logging as log
from common.code import request_result
from common.acl import acl_check
from common.parameters import parameter_check
from common.token_localauth import token_auth

from ucenter.manager import users_manager
from ucenter.manager import roles_manager
from ucenter.manager import passwords_manager
from ucenter.manager import tokens_manager
from ucenter.manager import teams_manager
from ucenter.manager import projects_manager
from ucenter.manager import userteam_manager
from ucenter.manager import userproject_manager


class UcenterRpcManager(object):

    def __init__(self):

        self.users_manager = users_manager.UsersManager()
        self.roles_manager = roles_manager.RolesManager()
        self.passwords_manager = passwords_manager.PasswordsManager()
        self.tokens_manager = tokens_manager.TokensManager()
        self.teams_manager = teams_manager.TeamsManager()
        self.projects_manager = projects_manager.ProjectsManager()
        self.userteam_manager = userteam_manager.UserTeamManager()
        self.userproject_manager = userproject_manager.UserProjectManager()

    def user_create(self, context, parameters):

        try:
            user_name = parameters.get('user_name')
            password = parameters.get('password')
            email = parameters.get('email')
            mobile = parameters.get('mobile')
            code_id = parameters.get('code_id')
            code_str = parameters.get('code_str')

            user_name = parameter_check(user_name, ptype='pnam')
            password = parameter_check(password, ptype='ppwd')
            email = parameter_check(email, ptype='peml')
            mobile = parameter_check(mobile, ptype='pint', exist='no')
            code_id = parameter_check(code_id, ptype='pstr', exist='no')
            code_str = parameter_check(code_str, ptype='pstr', exist='no')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.users_manager.user_create(
                    user_name, password, email,
                    mobile, code_id, code_str)

    def user_activate(self, context, parameters):

        try:
            user_uuid = context.get('resource_uuid')

            user_uuid = parameter_check(user_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.users_manager.user_activate(user_uuid)

    @acl_check
    def user_status(self, context, parameters):

        try:
            user_uuid = parameters.get('user_uuid')
            status = parameters.get('user_status')

            user_uuid = parameter_check(user_uuid, ptype='pstr')
            status = parameter_check(status, ptype='pstr')
            if (status != 'enable') and (status != 'disable'):
                raise(Exception('parameter error'))
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.users_manager.user_status(user_uuid, status)

    def user_check(self, context, parameters):

        try:
            user_name = parameters.get('user_name')

            try:
                user_name = parameter_check(user_name, ptype='pnam')
                email = None
            except Exception:
                email = parameter_check(user_name, ptype='peml')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        if email:
            return self.users_manager.email_check(email)
        else:
            return self.users_manager.user_check(user_name)

    @acl_check
    def user_list(self, context, parameters):

        try:
            user_name = parameters.get('user_name')

            try:
                user_name = parameter_check(user_name, ptype='pnam')
            except Exception:
                user_name = parameter_check(user_name, ptype='peml')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.users_manager.user_list(user_name)

    @acl_check
    def user_info(self, context, parameters):

        try:
            token = context['token']
            user_info = token_auth(context['token'])['result']
            team_uuid = user_info.get('team_uuid')

            user_uuid = context.get('resource_uuid')

            user_uuid = parameter_check(user_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.users_manager.user_info(user_uuid, team_uuid)

    @acl_check
    def user_update(self, context, parameters):

        try:
            user_uuid = context.get('resource_uuid')

            real_name = parameters.get('real_name')
            mobile = parameters.get('mobile')
            sex = parameters.get('sex')
            birth_date = parameters.get('birth_date')

            user_uuid = parameter_check(user_uuid, ptype='pstr')
            real_name = parameter_check(real_name, ptype='pnam', exist='no')
            mobile = parameter_check(mobile, ptype='pint', exist='no')
            sex = parameter_check(sex, ptype='pstr', exist='no')
            birth_date = parameter_check(birth_date, ptype='pflt', exist='no')
            if sex and (sex != 'man') and (sex != 'woman'):
                raise(Exception('parameter error'))
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.users_manager.user_update(
                    user_uuid, real_name, mobile, sex, birth_date)

    @acl_check
    def role_create(self, context, parameters):

        try:
            token = context['token']
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')
            team_uuid = user_info.get('team_uuid')

            role_name = parameters.get('role_name')
            role_priv = parameters.get('role_priv')

            user_uuid = parameter_check(user_uuid, ptype='pstr')
            team_uuid = parameter_check(team_uuid, ptype='pstr')
            role_name = parameter_check(role_name, ptype='pnam')
            role_priv = parameter_check(role_priv, ptype='pstr')
            for i in role_priv:
                if (i not in 'CRUD'):
                    raise(Exception('parameter error'))
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.roles_manager.role_create(
                    token, role_name, role_priv,
                    user_uuid, team_uuid)

    @acl_check
    def role_list(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            team_uuid = user_info.get('team_uuid')

            team_uuid = parameter_check(team_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.roles_manager.role_list(team_uuid)

    @acl_check
    def role_info(self, context, parameters):

        try:
            role_uuid = context.get('resource_uuid')

            role_uuid = parameter_check(role_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.roles_manager.role_info(role_uuid)

    @acl_check
    def role_update(self, context, parameters):

        try:
            role_uuid = context.get('resource_uuid')
            role_priv = parameters.get('role_priv')

            role_uuid = parameter_check(role_uuid, ptype='pstr')
            role_priv = parameter_check(role_priv, ptype='pstr')
            for i in role_priv:
                if (i not in 'CRUD'):
                    raise(Exception('parameter error'))
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.roles_manager.role_update(role_uuid, role_priv)

    @acl_check
    def role_delete(self, context, parameters):

        try:
            role_uuid = context.get('resource_uuid')

            role_uuid = parameter_check(role_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.roles_manager.role_delete(role_uuid)

    @acl_check
    def password_change(self, context, parameters):

        try:
            user_uuid = context.get('resource_uuid')
            old_password = parameters.get('old_password')
            new_password = parameters.get('new_password')

            user_uuid = parameter_check(user_uuid, ptype='pstr')
            old_password = parameter_check(old_password, ptype='ppwd')
            new_password = parameter_check(new_password, ptype='ppwd')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.passwords_manager.password_change(
                    user_uuid, old_password, new_password)

    def password_find(self, context, parameters):

        try:
            user_name = context.get('resource_uuid')

            try:
                user_name = parameter_check(user_name, ptype='pnam')
            except Exception:
                user_name = parameter_check(user_name, ptype='peml')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.passwords_manager.password_find(user_name)

    @acl_check
    def password_reset(self, context, parameters):

        try:
            user_uuid = context.get('resource_uuid')
            password = parameters.get('password')

            user_uuid = parameter_check(user_uuid, ptype='pstr')
            password = parameter_check(password, ptype='ppwd')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.passwords_manager.password_reset(
                    user_uuid, password)

    def token_login(self, context, parameters):

        try:
            user_name = parameters.get('user_name')
            password = parameters.get('password')

            try:
                user_name = parameter_check(user_name, ptype='pnam')
            except Exception:
                user_name = parameter_check(user_name, ptype='peml')
            password = parameter_check(password, ptype='ppwd')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.tokens_manager.token_login(user_name, password)

    def token_switch(self, context, parameters):

        try:
            user_token = context.get('token')
            team_uuid = parameters.get('team_uuid')
            project_uuid = parameters.get('project_uuid')

            user_token = parameter_check(user_token, ptype='pstr')
            team_uuid = parameter_check(team_uuid, ptype='pstr')
            project_uuid = parameter_check(project_uuid, ptype='pstr',
                                           exist='no')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.tokens_manager.token_switch(
                    user_token, team_uuid, project_uuid)

    def token_auth(self, context, parameters):

        try:
            user_token = context.get('token')

            user_token = parameter_check(user_token, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.tokens_manager.token_check(user_token)

    def token_delete(self, context, parameters):

        try:
            user_token = context.get('token')

            user_token = parameter_check(user_token, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.tokens_manager.token_delete(user_token)

    @acl_check
    def team_create(self, context, parameters):

        try:
            token = context['token']
            user_info = token_auth(context['token'])['result']
            team_owner = user_info.get('user_uuid')

            team_name = parameters.get('team_name')
            team_desc = parameters.get('team_desc')

            team_name = parameter_check(team_name, ptype='pnam')
            team_owner = parameter_check(team_owner, ptype='pstr')
            team_desc = parameter_check(team_desc, ptype='pstr', exist='no')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.teams_manager.team_create(
                    token, team_name, team_owner, team_desc)

    @acl_check
    def team_list(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')

            team_name = parameters.get('team_name')
            name_check = parameters.get('name_check')
            uuid_info = parameters.get('uuid_info')
            public_info = parameters.get('public_info')

            team_name = parameter_check(team_name, ptype='pstr', exist='no')
            name_check = parameter_check(name_check, ptype='pstr', exist='no')
            uuid_info = parameter_check(uuid_info, ptype='pstr', exist='no')
            public_info = parameter_check(public_info, ptype='pstr',
                                          exist='no')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.teams_manager.team_list(
                    user_uuid, team_name, name_check,
                    uuid_info, public_info)

    @acl_check
    def team_info(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')

            team_uuid = parameters.get('team_uuid')

            team_uuid = parameter_check(team_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.teams_manager.team_info(team_uuid, user_uuid)

    @acl_check
    def team_update(self, context, parameters):

        try:
            team_uuid = context.get('resource_uuid')
            team_owner = parameters.get('team_owner')
            team_type = parameters.get('team_type')
            team_desc = parameters.get('team_desc')

            team_uuid = parameter_check(team_uuid, ptype='pstr')
            team_owner = parameter_check(team_owner, ptype='pstr', exist='no')
            team_type = parameter_check(team_type, ptype='pstr', exist='no')
            team_desc = parameter_check(team_desc, ptype='pstr', exist='no')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.teams_manager.team_update(
                    team_uuid, team_owner, team_type, team_desc)

    @acl_check
    def team_delete(self, context, parameters):

        try:
            team_uuid = context.get('resource_uuid')

            team_uuid = parameter_check(team_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.teams_manager.team_delete(team_uuid)

    @acl_check
    def project_create(self, context, parameters):

        try:
            token = context['token']
            user_info = token_auth(context['token'])['result']
            project_owner = user_info.get('user_uuid')
            project_team = user_info.get('team_uuid')

            project_name = parameters.get('project_name')
            project_desc = parameters.get('project_desc')

            project_name = parameter_check(project_name, ptype='pnam')
            project_owner = parameter_check(project_owner, ptype='pstr')
            project_team = parameter_check(project_team, ptype='pstr')
            project_desc = parameter_check(project_desc, ptype='pstr',
                                           exist='no')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.projects_manager.project_create(
                    token, project_name, project_owner,
                    project_team, project_desc)

    @acl_check
    def project_list(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')
            team_uuid = user_info.get('team_uuid')

            user_uuid = parameter_check(user_uuid, ptype='pstr')
            team_uuid = parameter_check(team_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.projects_manager.project_list(user_uuid, team_uuid)

    @acl_check
    def project_info(self, context, parameters):

        try:
            project_uuid = context.get('resource_uuid')

            project_uuid = parameter_check(project_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.projects_manager.project_info(project_uuid)

    @acl_check
    def project_update(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            team_uuid = user_info.get('team_uuid')

            project_uuid = context.get('resource_uuid')
            project_owner = parameters.get('project_owner')
            project_desc = parameters.get('project_desc')

            team_uuid = parameter_check(team_uuid, ptype='pstr')
            project_uuid = parameter_check(project_uuid, ptype='pstr')
            project_owner = parameter_check(project_owner, ptype='pstr',
                                            exist='no')
            project_desc = parameter_check(project_desc, ptype='pstr',
                                           exist='no')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.projects_manager.project_update(
                    project_uuid, team_uuid, project_owner, project_desc)

    @acl_check
    def project_delete(self, context, parameters):

        try:
            project_uuid = context.get('resource_uuid')

            project_uuid = parameter_check(project_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.projects_manager.project_delete(project_uuid)

    @acl_check
    def user_team_add(self, context, parameters):

        try:
            token = context['token']
            user_info = token_auth(context['token'])['result']
            team_uuid = user_info.get('team_uuid')

            user_uuid = parameters.get('user_uuid')
            role_uuid = parameters.get('role_uuid')

            team_uuid = parameter_check(team_uuid, ptype='pstr')
            user_uuid = parameter_check(user_uuid, ptype='pstr')
            role_uuid = parameter_check(role_uuid, ptype='pstr', exist='no')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.userteam_manager.user_team_add(
                    token, user_uuid, team_uuid, role_uuid)

    @acl_check
    def user_team_list(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            team_uuid = user_info.get('team_uuid')

            page_size = parameters.get('page_size')
            page_num = parameters.get('page_num')

            team_uuid = parameter_check(team_uuid, ptype='pstr')
            page_size = parameter_check(page_size, ptype='pint')
            page_num = parameter_check(page_num, ptype='pint')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.userteam_manager.user_team_list(
                    team_uuid, page_size, page_num)

    @acl_check
    def user_team_activate(self, context, parameters):

        try:
            user_uuid = context.get('resource_uuid')
            team_uuid = parameters.get('team_uuid')

            user_uuid = parameter_check(user_uuid, ptype='pstr')
            team_uuid = parameter_check(team_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.userteam_manager.user_team_activate(
                    user_uuid, team_uuid)

    @acl_check
    def user_team_update(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            team_uuid = user_info.get('team_uuid')
            team_priv = user_info.get('team_priv')

            n_user_uuid = parameters.get('user_uuid')
            n_role_uuid = parameters.get('role_uuid')

            team_uuid = parameter_check(team_uuid, ptype='pstr')
            team_priv = parameter_check(team_priv, ptype='pstr')
            n_user_uuid = parameter_check(n_user_uuid, ptype='pstr')
            n_role_uuid = parameter_check(n_role_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.userteam_manager.user_team_update(
                    team_uuid, team_priv, n_user_uuid, n_role_uuid)

    @acl_check
    def user_team_delete(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')
            team_priv = user_info.get('team_priv')

            n_user_uuid = parameters.get('user_uuid')
            n_team_uuid = parameters.get('team_uuid')

            n_user_uuid = parameter_check(n_user_uuid, ptype='pstr')
            n_team_uuid = parameter_check(n_team_uuid, ptype='pstr')
            team_priv = parameter_check(team_priv, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.userteam_manager.user_team_delete(
                    n_user_uuid, n_team_uuid, user_uuid, team_priv)

    @acl_check
    def user_project_add(self, context, parameters):

        try:
            token = context['token']
            user_info = token_auth(context['token'])['result']
            team_uuid = user_info.get('team_uuid')
            project_uuid = user_info.get('project_uuid')

            user_uuid = parameters.get('user_uuid')
            role_uuid = parameters.get('role_uuid')

            team_uuid = parameter_check(team_uuid, ptype='pstr')
            project_uuid = parameter_check(project_uuid, ptype='pstr')
            user_uuid = parameter_check(user_uuid, ptype='pstr')
            role_uuid = parameter_check(role_uuid, ptype='pstr', exist='no')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.userproject_manager.user_project_add(
                    token, user_uuid, role_uuid,
                    project_uuid, team_uuid)

    @acl_check
    def user_project_list(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            project_uuid = user_info.get('project_uuid')

            page_size = parameters.get('page_size')
            page_num = parameters.get('page_num')

            project_uuid = parameter_check(project_uuid, ptype='pstr')
            page_size = parameter_check(page_size, ptype='pint')
            page_num = parameter_check(page_num, ptype='pint')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.userproject_manager.user_project_list(
                    project_uuid, page_size, page_num)

    @acl_check
    def user_project_update(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            project_uuid = user_info.get('project_uuid')
            project_priv = user_info.get('project_priv')

            n_user_uuid = parameters.get('user_uuid')
            n_role_uuid = parameters.get('role_uuid')

            project_uuid = parameter_check(project_uuid, ptype='pstr')
            project_priv = parameter_check(project_priv, ptype='pstr')
            n_user_uuid = parameter_check(n_user_uuid, ptype='pstr')
            n_role_uuid = parameter_check(n_role_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.userproject_manager.user_project_update(
                    project_uuid, project_priv, n_user_uuid, n_role_uuid)

    @acl_check
    def user_project_delete(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')
            project_uuid = user_info.get('project_uuid')
            project_priv = user_info.get('project_priv')

            n_user_uuid = parameters.get('user_uuid')

            n_user_uuid = parameter_check(n_user_uuid, ptype='pstr')
            project_uuid = parameter_check(project_uuid, ptype='pstr')
            project_priv = parameter_check(project_priv, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.userproject_manager.user_project_delete(
                    user_uuid, project_uuid, project_priv, n_user_uuid)
