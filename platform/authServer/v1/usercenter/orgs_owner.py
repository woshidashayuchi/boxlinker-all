#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/10/18 14:56
"""

from flask_restful import Resource
from flask import jsonify, request, g
from authServer.pyTools.tools.codeString import request_result

from authServer.common.decorate import check_headers, get_userinfo_by_payload
from authServer.models.hub_db_meta import OrgsUser, UserBase

from authServer.common.role import OrgaRole
class OrganizationOwner(Resource):
    @staticmethod
    @check_headers
    @get_userinfo_by_payload
    def modify_orga_owner(kwargs):
        # 不是拥有者 或  要操作的组织和token不符
        if kwargs['role_uuid'] != str(OrgaRole.OrgaMaster.value) or kwargs['orga_uuid_arg'] != kwargs['orga_uuid']:
            return request_result(806)

        try:

            # 新拥有者,并赋予管理员权限
            g.db_session.query(OrgsUser).filter(
                OrgsUser.org_id == kwargs['orga_uuid'],
                OrgsUser.uid == kwargs['user_uuid_arg']
            ).update({"role": OrgaRole.OrgaMaster.value})

            # 解除拥有者权限
            g.db_session.query(OrgsUser).filter(
                OrgsUser.org_id == kwargs['orga_uuid'],
                OrgsUser.uid == kwargs['uid']
            ).update({"role": OrgaRole.OrgaAdmin.value})

            g.db_session.commit()

            from authServer.common.usercenter.token import get_login_token
            return get_login_token(kwargs['user_name'])  # 返回用户token
            # return request_result(0)
        except Exception as msg:
            return request_result(403)

    def put(self, orga_uuid, user_uuid):
        """
        @apiGroup OrganizationOwner

        @apiDescription           修改组织拥有者
        @apiVersion 1.0.0
        @apiHeader {String} token 请求接口的token,放在请求头中
        @api {put} /api/v1.0/usercenter/orgs/<string:orga_uuid>/owner/<string:user_uuid>  修改组织拥有者

        @apiParamExample {json} Request-Param-Example:
            {
                "status": 0,
                "msg": "OK",
                "result": "some msg"
            }

        @apiParam {String} orga_uuid      组织id
        @apiParam {String} user_uuid     用户id  组织新拥有者的用户id
        """
        try:
            kwargs = dict()
            kwargs['user_uuid_arg'] = user_uuid
            kwargs['orga_uuid_arg'] = orga_uuid
        except Exception as msg:
            return jsonify(request_result(710, ret=msg.message))
        return jsonify(self.modify_orga_owner(kwargs))





    @staticmethod
    @check_headers
    @get_userinfo_by_payload
    def get_orga_owner(kwargs):

        # 不是管理员 或  要操作的组织和token不符
        if kwargs['role_uuid'] != '1' or kwargs['orga_uuid_arg'] != kwargs['orga_uuid']:
            return request_result(806)

        try:
            orgs_u = g.db_session.query(OrgsUser).filter(
                OrgsUser.org_id == kwargs['orga_uuid'],
                OrgsUser.uid == kwargs['uid']).first()

            if orgs_u is None:
                return request_result(806)

            user = g.db_session.query(UserBase).filter(
                UserBase.user_id == kwargs['uid']).first()

            if user is None:
                return request_result(808)

            user_msg = dict()
            user_msg['username'] = user.username
            user_msg['email'] = user.email
            user_msg['logo'] = user.logo
            user_msg['orga_role'] = orgs_u.role

            return request_result(0, ret=user_msg)
        except Exception as msg:
            return request_result(403)


    def get(self, orga_uuid):
        """
        @apiGroup OrganizationOwner
        @apiDescription           获取组织拥有者信息
        @apiVersion 1.0.0
        @apiHeader {String} token 请求接口的token,放在请求头中
        @api {get} /api/v1.0/usercenter/orgs/<string:orga_uuid>/owner   获取组织拥有者信息

        @apiParamExample {json} Request-Param-Example:
            {
                "status": 0,
                "msg": "OK",
                "result": "some msg"
            }

        @apiParam {String} org_id      组织id
        """
        try:
            kwargs = dict()
            kwargs['orga_uuid_arg'] = orga_uuid
        except Exception as msg:
            return jsonify(request_result(710, ret=msg.message))
        return jsonify(self.get_orga_owner(kwargs))