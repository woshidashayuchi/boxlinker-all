#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/10/17 14:15
@func: 组织成员操作
"""
import os
from authServer.common.role import OrgaRole
import json

from flask import jsonify, request, g
from flask_restful import Resource
from authServer.pyTools.tools.codeString import request_result

from authServer.models.hub_db_meta import OrgsUser, UserBase


from authServer.common.decorate import check_headers, get_userinfo_by_payload, check_default_orga, check_orga_uuid_arg_is_orga_uuid
from authServer.pyTools.tools.timeControl import get_now_time


def get_orga_user_list(orga_uuid):
    """ 得到一个组织的用户列表 """
    try:
        orga_users = g.db_session.query(OrgsUser).filter(
            OrgsUser.org_id == orga_uuid, OrgsUser.is_delete == '0').all()

        if orga_users is None:
            return request_result(808)

        orga_user_list = list()
        for orga_user_n in orga_users:
            orga_user = dict()
            orga_user['uid'] = orga_user_n.uid
            orga_user['role'] = orga_user_n.role
            orga_user['creation_time'] = orga_user_n.creation_time
            orga_user['update_time'] = orga_user_n.update_time

            user_base = g.db_session.query(UserBase).filter(UserBase.user_id == orga_user_n.uid).first()
            if user_base is not None:
                orga_user['user_name'] = user_base.username
                orga_user['email'] = user_base.email
                # orga_user['logo'] = user_base.logo
                from authServer.conf.conf import OssHost
                if user_base.logo is None or user_base.logo == '':
                    orga_user['logo'] = OssHost + os.sep + 'repository/default.png'
                else:
                    orga_user['logo'] = OssHost + os.sep + user_base.logo
            orga_user_list.append(orga_user)
        return request_result(0, ret=orga_user_list)
    except Exception as msg:
        return request_result(403, ret=msg.message)




class OrganizationUser(Resource):

    @staticmethod
    @check_headers
    @get_userinfo_by_payload
    @check_default_orga
    @check_orga_uuid_arg_is_orga_uuid
    def create_org_user(kwargs):

        # 不是管理员 或  要操作的组织和token不符
        print kwargs['role_uuid']
        print type(kwargs['role_uuid'])
        print OrgaRole.OrgaMaster.value
        print OrgaRole.OrgaDevelop.value

        if kwargs['role_uuid'] != str(OrgaRole.OrgaMaster.value) and kwargs['role_uuid'] != str(OrgaRole.OrgaDevelop.value):
            return request_result(806)

        try:
            now_time = get_now_time()

            # 已经是组织成员
            orgs_u = g.db_session.query(OrgsUser).filter(
                OrgsUser.org_id == kwargs['orga_uuid'],
                OrgsUser.uid == kwargs['user_uuid_arg']
            ).first()

            # print "----create_org_user----"

            if orgs_u is not None:
                # print "----create_org_user---- orgs_u is not None"
                # print orgs_u.is_delete
                # print type(orgs_u.is_delete)
                if str(orgs_u.is_delete) == '0':    # 已经是组织成员
                    return request_result(807, ret=kwargs['user_name'])
                elif str(orgs_u.is_delete) == '1':  # 删除的用户,冲洗标记
                    g.db_session.query(OrgsUser).filter(
                        OrgsUser.org_id == kwargs['orga_uuid'],
                        OrgsUser.uid == kwargs['user_uuid_arg']
                    ).update({"is_delete": '0', "update_time": now_time, "role": OrgaRole.OrgaDevelop.value})

                    g.db_session.commit()
                    return request_result(0)


            org_user = OrgsUser(
                org_id=kwargs['orga_uuid'], uid=kwargs['user_uuid_arg'],
                role=OrgaRole.OrgaDevelop.value, creation_time=now_time, update_time=now_time)
            g.db_session.add(org_user)
            g.db_session.commit()
            return request_result(0)
        except Exception as msg:
            return request_result(401, ret=msg.message)

    def post(self, orga_uuid):
        """
        @apiGroup OrganizationUser
        @apiDescription       添加组织成员;添加用户到某一个组织;只有组织管理员可以添加用户
        @apiVersion 1.0.0
        @apiHeader {String} token 请求接口的token,放在请求头中
        @api {post} /api/v1.0/usercenter/orgs/<string:orga_uuid>/users 添加组织成员

        @apiParamExample {json} Request-Param-Example:
            {
                "user_uuid": ....
            }

        @apiSuccessExample {json} Request-Param-Example:
            {
                "status": 0,
                "msg": "OK",
                "result": "some msg"
            }

        @apiParam {String} orga_uuid    组织id
        @apiParam {String} user_uuid   用户id
        """
        try:
            data = request.data
            data_json = json.loads(data)
            user_uuid = data_json.get('user_uuid', '').decode('utf-8').encode('utf-8')
            if user_uuid == '':
                return jsonify(request_result(706))
            kwargs = dict()
            kwargs['user_uuid_arg'] = user_uuid
            kwargs['orga_uuid_arg'] = orga_uuid
        except Exception as msg:
            return jsonify(request_result(710, ret=msg.message))

        return jsonify(self.create_org_user(kwargs))


    @staticmethod
    @check_headers
    @get_userinfo_by_payload
    @check_default_orga
    @check_orga_uuid_arg_is_orga_uuid
    def orgs_user_list(kwargs):

        # orga_uuid_arg  orga_uuid
        return get_orga_user_list(kwargs['orga_uuid_arg'])


    def get(self, orga_uuid):
        """
        @apiGroup OrganizationUser

        @apiDescription     获取组织下用户列表
        @apiVersion 1.0.0
        @apiHeader {String} token 请求接口的token,放在请求头中
        @api {get} /api/v1.0/usercenter/orgs/<string:orga_uuid>/users  获取组织下用户列表

        @apiSuccessExample {json} 修改组织用户属性:
            {
                "status": 0,
                "msg": "OK",
                "result":
                [
                    {
                        "uid": "acbd323",
                        "email": "test@126.com",
                        ... ...
                    },
                    {
                        "uid": "acbd3e2223",
                        "email": "test232@126.com",
                        ... ...
                    },
                    ... ...
                ]
            }

        @apiParam {String} orga_uuid      组织id
        """
        kwargs = dict()
        kwargs['orga_uuid_arg'] = orga_uuid
        return jsonify(self.orgs_user_list(kwargs))


class OrganizationUserHandle(Resource):

    @staticmethod
    @check_headers
    @get_userinfo_by_payload
    @check_default_orga
    def modify_org_user(kwargs):

        # 不是管理员
        if int(kwargs['role_uuid']) > int(kwargs['role_uuid_arg']):  # 权限超出自己权限范围
            return request_result(806)

        if kwargs['orga_uuid_arg'] != kwargs['orga_uuid']:  # 要操作的组织和token不符
            return request_result(806)


        try:

            g.db_session.query(OrgsUser).filter(
                OrgsUser.org_id == kwargs['orga_uuid'],
                OrgsUser.uid == kwargs['user_uuid_arg']
            ).update({"role": kwargs['role_uuid_arg']})

            g.db_session.commit()
            return request_result(0)
        except Exception as msg:
            return request_result(403)


    def put(self, orga_uuid, user_uuid):
        """
        @apiGroup OrganizationUserHandle
        @apiDescription       修改组织成员属性,只有组织拥有者可以修改其他成员的属性
        @apiVersion 1.0.0
        @apiHeader {String} token 请求接口的token,放在请求头中
        @api {put} /api/v1.0/usercenter/orgs/<string:orga_uuid>/users/<string:user_uuid>  修改组织成员属性

        @apiParamExample {json} Request-Param-Example:
            {
                "role_uuid": "1"
            }

            1: 管理员
            2: 开发者

            SystemGod = 100  # 系统管理员
            OrgaMaster = 200  # 群主;组织拥有者
            OrgaAdmin = 210   # 群管理员
            OrgaDevelop = 400  # 群开发者


        @apiSuccessExample {json} 修改组织用户属性:
            {
                "status": 0,
                "msg": "OK",
                "result": "some msg"
            }

        @apiParam {String} orga_uuid   组织id
        @apiParam {String} user_uuid   用户id
        @apiParam {String} role_uuid 修改用户权限, 添加成员时该参数可以为空
        """
        try:
            data = request.data
            data_json = json.loads(data)
            role_uuid_arg = data_json.get('role_uuid', '').decode('utf-8').encode('utf-8')
            print role_uuid_arg
            if role_uuid_arg == '' or role_uuid_arg not in [str(OrgaRole.OrgaAdmin.value), str(OrgaRole.OrgaMaster.value),
                                                            str(OrgaRole.OrgaDevelop.value)]:
                return jsonify(request_result(706))
            kwargs = dict()
            kwargs['role_uuid_arg'] = role_uuid_arg
            kwargs['user_uuid_arg'] = user_uuid
            kwargs['orga_uuid_arg'] = orga_uuid
        except Exception as msg:
            return jsonify(request_result(710, ret=msg.message))

        return jsonify(self.modify_org_user(kwargs=kwargs))



    @staticmethod
    @check_headers
    @get_userinfo_by_payload
    @check_default_orga
    def get_org_user_msg(kwargs):
        if kwargs['orga_uuid_arg'] != kwargs['orga_uuid']:
            return request_result(806)
        try:

            orgs_u = g.db_session.query(OrgsUser).filter(
                OrgsUser.org_id == kwargs['orga_uuid'],
                OrgsUser.uid == kwargs['user_uuid_arg']).first()

            user = g.db_session.query(UserBase).filter(
                UserBase.user_id == kwargs['user_uuid_arg']).first()

            if orgs_u is None or user is None:
                return request_result(808)

            user_msg = dict()
            user_msg['username'] = user.username
            user_msg['email'] = user.email
            user_msg['logo'] = user.logo
            user_msg['orga_role'] = orgs_u.role

            return request_result(0, ret=user_msg)
        except Exception as msg:
            return request_result(403)

    def get(self, orga_uuid, user_uuid):
        """
        @apiGroup OrganizationUserHandle

        @apiDescription     获取组织下某一个用户的信息
        @apiVersion 1.0.0
        @apiHeader {String} token 请求接口的token,放在请求头中
        @api {get} /api/v1.0/usercenter/orgs/<string:orga_uuid>/users/<string:user_uuid>  获取组织某一个用户的信息

        @apiSuccessExample {json} 修改组织用户属性:
            {
                "status": 0,
                "msg": "OK",
                "result":
                [
                    "uid": "acbd323",
                    "email": "test@126.com"
                ]
            }

        @apiParam {String} orga_uuid      组织id
        @apiParam {String} user_uuid   用户id

        """
        try:
            kwargs = dict()
            kwargs['user_uuid_arg'] = user_uuid
            kwargs['orga_uuid_arg'] = orga_uuid
        except Exception as msg:
            return jsonify(request_result(710, ret=msg.message))
        return jsonify(self.get_org_user_msg(kwargs))



    @staticmethod
    @check_headers
    @get_userinfo_by_payload
    @check_default_orga
    def delete_org_user(kwargs):

        #
        orgs_u = g.db_session.query(OrgsUser).filter(
            OrgsUser.org_id == kwargs['orga_uuid_arg'],
            OrgsUser.uid == kwargs['user_uuid_arg'], OrgsUser.is_delete == '0').first()

        if orgs_u is None:
            return request_result(808)


        # 不是管理员
        if int(kwargs['role_uuid']) < int(orgs_u.role) is False:  # 权限超出自己权限范围
            return request_result(806)

        if kwargs['orga_uuid_arg'] != kwargs['orga_uuid']:  # 要操作的组织和token不符
            return request_result(806)

        try:
            now = get_now_time()
            g.db_session.query(OrgsUser).filter(
                OrgsUser.org_id == kwargs['orga_uuid'], OrgsUser.uid == kwargs['user_uuid_arg']).update(
                {"is_delete": '1', "update_time": now})
            g.db_session.commit()

            return request_result(0)
        except Exception as msg:
            print msg.message
            print msg.args

            for va in msg.args:
                print va
            return request_result(403)

    def delete(self, orga_uuid, user_uuid):
        """
        @apiGroup OrganizationUserHandle

        @apiDescription     删除组织成员
        @apiVersion 1.0.0
        @apiHeader {String} token 请求接口的token,放在请求头中
        @api {delete} /api/v1.0/usercenter/orgs/<string:orga_uuid>/users/<string:user_uuid>  删除组织成员

        @apiSuccessExample {json} 删除组织成员
            {
                "status": 0,
                "msg": "OK",
                "result": "some msg"
            }
        @apiParam {String} orga_uuid      组织id
        @apiParam {String} user_uuid   用户id
        """
        try:
            kwargs = dict()
            kwargs['user_uuid_arg'] = user_uuid
            kwargs['orga_uuid_arg'] = orga_uuid
        except Exception as msg:
            return jsonify(request_result(710, ret=msg.message))
        return jsonify(self.delete_org_user(kwargs))



