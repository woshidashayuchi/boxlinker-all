#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import json

from flask import request
from flask import redirect
from flask import render_template
from flask_restful import Resource

from conf import conf
from common.logs import logging as log
from common.code import request_result
from common.time_log import time_log
from common.parameters import context_data
from common.token_localauth import token_auth

from ucenter.rpcapi import rpc_api as ucenter_rpcapi


def user_activate(status):

    user_activate_ret = '%s%s%s' % (conf.boxlinker_index,
                                    ('/user_activate/status'
                                     '?ret_status='), status)

    return render_template("user_activate.html",
                           item=user_activate_ret)


class UcenterUsersApi(Resource):

    def __init__(self):

        self.ucenter_api = ucenter_rpcapi.UcenterRpcApi()

    @time_log
    def post(self):

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(None, "uct_usr_usr_crt", "create")

        return self.ucenter_api.user_create(context, parameters)

    @time_log
    def get(self):

        try:
            user_name = request.args.get('user_name')
            name_check = request.args.get('name_check')
            parameters = {
                             "user_name": user_name
                         }
        except Exception, e:
            log.warning('Parameters error, reason=%s' % (e))

            return request_result(101)

        if name_check == 'true':
            context = {}
            return self.ucenter_api.user_check(context, parameters)
        else:
            try:
                token = request.headers.get('token')
                token_auth(token)
            except Exception, e:
                log.warning('Token check error, token=%s, reason=%s'
                          % (token, e))
                return request_result(201)

            context = context_data(token, "uct_usr_usr_lst", "read")
            return self.ucenter_api.user_list(context, parameters)


class UcenterUserApi(Resource):

    def __init__(self):

        self.ucenter_api = ucenter_rpcapi.UcenterRpcApi()

    @time_log
    def get(self, user_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        context = context_data(token, user_uuid, "read")

        return self.ucenter_api.user_info(context)

    @time_log
    def put(self, user_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, user_uuid, "update")

        return self.ucenter_api.user_update(context, parameters)


class UcenterUserStatusApi(Resource):

    def __init__(self):

        self.ucenter_api = ucenter_rpcapi.UcenterRpcApi()

    @time_log
    def get(self, user_uuid):

        context = context_data(None, user_uuid, "create")

        ret_status = self.ucenter_api.user_activate(context).get('status')
        if int(ret_status) != 0:
            log.warning('User_id(%s) activate failure' % (user_uuid))

        return redirect('/api/v1.0/ucenter/users/activate/%s'
                        % (ret_status))

    @time_log
    def put(self, user_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, "uct_usr_usr_stu", "update")

        parameters['user_uuid'] = user_uuid

        return self.ucenter_api.user_status(context, parameters)


class UcenterRolesApi(Resource):

    def __init__(self):

        self.ucenter_api = ucenter_rpcapi.UcenterRpcApi()

    @time_log
    def post(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, "uct_rol_rol_crt", "create")

        return self.ucenter_api.role_create(context, parameters)

    @time_log
    def get(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        context = context_data(token, "uct_rol_rol_lst", "read")

        return self.ucenter_api.role_list(context)


class UcenterRoleApi(Resource):

    def __init__(self):

        self.ucenter_api = ucenter_rpcapi.UcenterRpcApi()

    @time_log
    def get(self, role_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        context = context_data(token, role_uuid, "read")

        return self.ucenter_api.role_info(context)

    @time_log
    def put(self, role_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, role_uuid, "update")

        return self.ucenter_api.role_update(context, parameters)

    @time_log
    def delete(self, role_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        context = context_data(token, role_uuid, "delete")

        return self.ucenter_api.role_delete(context)


class UcenterPasswordApi(Resource):

    def __init__(self):

        self.ucenter_api = ucenter_rpcapi.UcenterRpcApi()

    @time_log
    def post(self, user_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, user_uuid, "update")

        return self.ucenter_api.password_change(context, parameters)

    @time_log
    def get(self, user_uuid):

        context = context_data(None, user_uuid, "read")

        return self.ucenter_api.password_find(context)

    @time_log
    def put(self, user_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, user_uuid, "update")

        return self.ucenter_api.password_reset(context, parameters)


class UcenterTokensApi(Resource):

    def __init__(self):

        self.ucenter_api = ucenter_rpcapi.UcenterRpcApi()

    @time_log
    def post(self):

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(None, "uct_tkn_tkn_lgi", None)

        return self.ucenter_api.token_login(context, parameters)

    @time_log
    def get(self):

        try:
            token = request.headers.get('token')
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        context = context_data(token, None, None)

        return self.ucenter_api.token_check(context)

    @time_log
    def put(self):

        try:
            token = request.headers.get('token')
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, None, None)

        return self.ucenter_api.token_switch(context, parameters)

    @time_log
    def delete(self):

        try:
            token = request.headers.get('token')
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        context = context_data(token, None, None)

        return self.ucenter_api.token_delete(context)


class UcenterTeamsApi(Resource):

    def __init__(self):

        self.ucenter_api = ucenter_rpcapi.UcenterRpcApi()

    @time_log
    def post(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, "uct_tem_tem_crt", "create")

        return self.ucenter_api.team_create(context, parameters)

    @time_log
    def get(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            team_name = request.args.get('team_name')
            name_check = request.args.get('name_check')
            uuid_info = request.args.get('uuid_info')
            public_info = request.args.get('public_info')
            parameters = {
                             "team_name": team_name,
                             "name_check": name_check,
                             "uuid_info": uuid_info,
                             "public_info": public_info
                         }
        except Exception, e:
            log.warning('Parameters error, reason=%s' % (e))

            return request_result(101)

        context = context_data(token, "uct_tem_tem_lst", "read")

        return self.ucenter_api.team_list(context, parameters)


class UcenterTeamApi(Resource):

    def __init__(self):

        self.ucenter_api = ucenter_rpcapi.UcenterRpcApi()

    @time_log
    def get(self, team_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        context = context_data(token, "uct_usr_usr_com", "read")

        parameters = {"team_uuid": team_uuid}

        return self.ucenter_api.team_info(context, parameters)

    @time_log
    def put(self, team_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, team_uuid, "update")

        return self.ucenter_api.team_update(context, parameters)

    @time_log
    def delete(self, team_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        context = context_data(token, team_uuid, "delete")

        return self.ucenter_api.team_delete(context)


class UcenterProjectsApi(Resource):

    def __init__(self):

        self.ucenter_api = ucenter_rpcapi.UcenterRpcApi()

    @time_log
    def post(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, "uct_pro_pro_crt", "create")

        return self.ucenter_api.project_create(context, parameters)

    @time_log
    def get(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        context = context_data(token, "uct_pro_pro_lst", "read")

        return self.ucenter_api.project_list(context)


class UcenterProjectApi(Resource):

    def __init__(self):

        self.ucenter_api = ucenter_rpcapi.UcenterRpcApi()

    @time_log
    def get(self, project_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        context = context_data(token, project_uuid, "read")

        return self.ucenter_api.project_info(context)

    @time_log
    def put(self, project_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, project_uuid, "update")

        return self.ucenter_api.project_update(context, parameters)

    @time_log
    def delete(self, project_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        context = context_data(token, project_uuid, "delete")

        return self.ucenter_api.project_delete(context)


class UcenterUsersTeamsApi(Resource):

    def __init__(self):

        self.ucenter_api = ucenter_rpcapi.UcenterRpcApi()

    @time_log
    def post(self):

        try:
            token = request.headers.get('token')
            user_info = token_auth(token)['result']
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, user_info['team_uuid'], "create")

        return self.ucenter_api.user_team_add(context, parameters)

    @time_log
    def get(self):

        try:
            token = request.headers.get('token')
            user_info = token_auth(token)['result']
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            page_size = request.args.get('page_size')
            page_num = request.args.get('page_num')
            parameters = {
                             "page_size": page_size,
                             "page_num": page_num
                         }
        except Exception, e:
            log.warning('Parameters error, reason=%s' % (e))

            return request_result(101)

        context = context_data(token, user_info['team_uuid'], "read")

        return self.ucenter_api.user_team_list(context, parameters)

    @time_log
    def delete(self):

        try:
            token = request.headers.get('token')
            user_info = token_auth(token)['result']
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            user_uuid = request.args.get('user_uuid')
            team_uuid = request.args.get('team_uuid')
            if team_uuid is None:
                team_uuid = user_info['team_uuid']
            parameters = {
                             "user_uuid": user_uuid,
                             "team_uuid": team_uuid
                         }
        except Exception, e:
            log.warning('Parameters error, reason=%s' % (e))

            return request_result(101)

        if user_uuid == user_info['user_uuid']:
            resource_uuid = user_uuid
        else:
            resource_uuid = team_uuid

        context = context_data(token, resource_uuid, "delete")

        return self.ucenter_api.user_team_delete(context, parameters)


class UcenterUserTeamApi(Resource):

    def __init__(self):

        self.ucenter_api = ucenter_rpcapi.UcenterRpcApi()

    @time_log
    def post(self, user_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, user_uuid, "update")

        return self.ucenter_api.user_team_activate(context, parameters)

    @time_log
    def put(self, user_uuid):

        try:
            token = request.headers.get('token')
            user_info = token_auth(token)['result']
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, user_info['team_uuid'], "update")

        parameters['user_uuid'] = user_uuid

        return self.ucenter_api.user_team_update(context, parameters)


class UcenterUsersProjectsApi(Resource):

    def __init__(self):

        self.ucenter_api = ucenter_rpcapi.UcenterRpcApi()

    @time_log
    def post(self):

        try:
            token = request.headers.get('token')
            user_info = token_auth(token)['result']
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, user_info['project_uuid'], "create")

        return self.ucenter_api.user_project_add(context, parameters)

    @time_log
    def get(self):

        try:
            token = request.headers.get('token')
            user_info = token_auth(token)['result']
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            page_size = request.args.get('page_size')
            page_num = request.args.get('page_num')
            parameters = {
                             "page_size": page_size,
                             "page_num": page_num
                         }
        except Exception, e:
            log.warning('Parameters error, reason=%s' % (e))

            return request_result(101)

        context = context_data(token, user_info['project_uuid'], "read")

        return self.ucenter_api.user_project_list(context, parameters)


class UcenterUserProjectApi(Resource):

    def __init__(self):

        self.ucenter_api = ucenter_rpcapi.UcenterRpcApi()

    @time_log
    def put(self, user_uuid):

        try:
            token = request.headers.get('token')
            user_info = token_auth(token)['result']
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, user_info['project_uuid'], "update")

        parameters['user_uuid'] = user_uuid

        return self.ucenter_api.user_project_update(context, parameters)

    @time_log
    def delete(self, user_uuid):

        try:
            token = request.headers.get('token')
            user_info = token_auth(token)['result']
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        if user_uuid == user_info['user_uuid']:
            resource_uuid = user_uuid
        else:
            resource_uuid = user_info['project_uuid']

        context = context_data(token, resource_uuid, "delete")

        parameters = {"user_uuid": user_uuid}

        return self.ucenter_api.user_project_delete(context, parameters)
