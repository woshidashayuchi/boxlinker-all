#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/10/17 10:09
"""

import json

from flask import jsonify, g, request
from flask_restful import Resource

from authServer.pyTools.tools.codeString import request_result
from authServer.common.decorate import check_headers, get_userinfo_by_payload

from authServer.common.usercenter.orgs import org_name_exist
from authServer.common.role import OrgaRole
from authServer.models.hub_db_meta import OrgsBase, OrgsUser
from authServer.pyTools.tools.timeControl import get_now_time

import uuid

from authServer.common.usercenter.token import get_login_token

from authServer.conf.conf import Mask_Public


def make_orgs(uid, user_name, org_name):
    """ 组织数据表中添加数据"""
    org_id = uuid.uuid3(uuid.NAMESPACE_DNS, org_name).__str__()
    now_time = get_now_time()
    try:

        org_base = OrgsBase(org_id=org_id, org_name=org_name, creation_time=now_time)
        g.db_session.add(org_base)
        g.db_session.commit()
    except Exception as msg:
        return request_result(401, ret=msg.message)

    try:
        org_user = OrgsUser(org_id=org_id, uid=uid, username=user_name,
                            role=OrgaRole.OrgaMaster.value,
                            creation_time=now_time, update_time=now_time)
        g.db_session.add(org_user)
        g.db_session.commit()
        return request_result(0, ret=org_id)
    except Exception as msg:
        org_base = OrgsBase(org_id=org_id)
        g.db_session.delete(org_base)
        g.db_session.commit()
        return request_result(401, ret=msg.message)


class OrganizationBase(Resource):

    @staticmethod
    @check_headers
    @get_userinfo_by_payload
    def create_org(kwargs):
        org_name = kwargs['orga_name_arg']
        if org_name_exist(org_name):
            return request_result(702, ret='org_name is exist')
        return make_orgs(uid=kwargs['uid'], user_name=kwargs['user_name'], org_name=org_name)

    def post(self):
        """
        @apiGroup OrganizationBase
        @apiDescription 创建组织

        @apiHeader {String} token   请求接口的token,放在请求头中
        @api {post} /api/v1.0/usercenter/orgs   创建组织

        @apiExample {POST} Example usage:
            post http://localhost/api/v1.0/usercenter/orgs
            {
                "orga_name": "sdsd"
            }

        @apiSuccessExample {json} Create-Org:
            {
                "status": 0,
                "msg": "OK",
                "result": "1deca42474872abcdefef34"  # 组织唯一id
            }
        @apiParam {String} org_name      组织名
        """

        try:
            data = request.data
            data_json = json.loads(data)
            org_name = data_json.get('orga_name', '').decode('utf-8').encode('utf-8')
            if org_name == '':
                return request_result(706)
            kwargs = dict()
            kwargs['orga_name_arg'] = org_name
        except Exception as msg:
            return request_result(710, ret=msg.message)


        return jsonify(self.create_org(kwargs=kwargs))



    @staticmethod
    @check_headers
    @get_userinfo_by_payload
    def get_user_orgas(kwargs):

        print kwargs['uid']

        try:
            orgs_all = g.db_session.query(OrgsUser).filter(
                OrgsUser.uid == kwargs['uid'], OrgsUser.is_delete == '0').all()

            if orgs_all is None:
                return request_result(809)

            orga_list = list()
            for organode in orgs_all:
                orgs_d = dict()
                orgs_d['org_id'] = organode.org_id
                orgs_d['role'] = organode.role
                orgs_d['creation_time'] = organode.creation_time
                orgs_d['update_time'] = organode.update_time


                orgs_base = g.db_session.query(OrgsBase).filter(
                    OrgsBase.org_id == organode.org_id).first()

                if orgs_base is not None:
                    orgs_d['orga_name'] = orgs_base.org_name
                    orgs_d['orga_detail'] = orgs_base.org_detail
                    orgs_d['is_public'] = orgs_base.is_public

                orga_list.append(orgs_d)


            return request_result(0, ret=orga_list)
        except Exception as msg:
            return request_result(403)

    def get(self):
        """
        @apiGroup OrganizationBase
        @apiDescription     获取一个用户下的组织列表;所属的所有组织信息
        @apiVersion 1.0.0
        @apiHeader {String} token 请求接口的token,放在请求头中
        @api {get} /api/v1.0/usercenter/orgs  用户组织列表

        @apiSuccessExample {json} 组织列表
            {
                "status": 0,
                "msg": "OK",
                "result":
                [
                    {
                        "org_id": "...",
                        "role": "...",
                        "creation_time": "...",
                        "update_time": "...",
                        "orga_name": "...",
                        "orga_detail": "...",
                        "is_public": "..."
                    },
                    ... ...
                ]
            }
        """
        try:
            kwargs = dict()
        except Exception as msg:
            return jsonify(request_result(710, ret=msg.message))
        return jsonify(self.get_user_orgas(kwargs))


    @staticmethod
    @check_headers
    @get_userinfo_by_payload
    def modify_org(kwargs):
        try:
            data = request.data
            data_json = json.loads(data)
            org_detail = data_json.get('orga_detail', '')  #.decode('utf-8').encode('utf-8')
            is_public = data_json.get('is_public', '').decode('utf-8').encode('utf-8')
            if org_detail == '' or is_public not in Mask_Public:
                return request_result(706)
        except Exception as msg:
            return request_result(710, ret=msg.message)

        try:
            print 'ssssss'
            print kwargs['orga_uuid']
            print kwargs['uid']
            orgs_user = g.db_session.query(OrgsUser).filter(
                OrgsUser.org_id == kwargs['orga_uuid'], OrgsUser.role == OrgaRole.OrgaMaster.value, OrgsUser.uid == kwargs['uid']).first()

            if orgs_user is None:
                return request_result(806)

            g.db_session.query(OrgsBase).filter(OrgsBase.org_id == kwargs['orga_uuid']).update(
                {"org_detail": org_detail, "is_public": is_public})
            g.db_session.commit()
            return request_result(0)
        except Exception as msg:
            return request_result(403, ret=msg.message)

    def put(self):
        """
        @apiName put
        @apiGroup OrganizationBase
        @apiDescription 修改组织信息,只有组织拥有者可以调用该接口(token 中含有  组织id --> orga_uuid )

        @apiHeader {String} token 请求接口的token,放在请求头中
        @api {put} /api/v1.0/usercenter/orgs  修改组织信息

        @apiExample {PUT} Example usage: 修改组织信息
            put http://localhost/api/v1.0/usercenter/orgs
            {
                "orga_detail": "...ab23def...",
                "is_public": "0",
            }

        @apiSuccessExample {json} Create-Org:
            {
                "status": 0,
                "msg": "OK",
                "result": "some msg"
            }
        @apiParam {String} org_detail    组织描述介绍
        @apiParam {String} is_public     是否公开组织信息
        """
        k = dict()
        return jsonify(self.modify_org(k))


# token中是不可以是默认组织, 而且参数和token中组织id需要相同
def check_orga_uuid(func):
    def _deco(kwargs=dict()):
        try:

            # 用户中心, 需要操作的组织id,不能和 默认组织id相同
            if kwargs['orga_uuid'] == kwargs['uid'] and kwargs['orga_uuid_arg'] != kwargs['orga_uuid']:
                return func(kwargs)

            if kwargs['orga_uuid'] != kwargs['uid'] and kwargs['orga_uuid_arg'] == kwargs['orga_uuid']:
                return func(kwargs)


            # role_uuid

            return request_result(813)

        except Exception as msg:
            return request_result(100, ret=msg.message)

    return _deco




# token中是不可以是默认组织, 而且参数和token中组织id需要相同
def check_orga_uuid_admin(func):
    def _deco(kwargs=dict()):
        try:

            print kwargs['role_uuid']
            print type(kwargs['role_uuid'])

            # 系统管理员默认具有全部操作; 此步必须先行判断
            if int(kwargs['role_uuid']) == OrgaRole.SystemGod.value:
                return func(kwargs)

            # 用户中心, 需要操作的组织id,不能和 默认组织id相同
            if kwargs['orga_uuid'] == kwargs['uid'] and kwargs['orga_uuid_arg'] != kwargs['orga_uuid']:
                return func(kwargs)

            if kwargs['orga_uuid'] != kwargs['uid'] and kwargs['orga_uuid_arg'] == kwargs['orga_uuid']:
                return func(kwargs)


            # role_uuid

            return request_result(813)

        except Exception as msg:
            return request_result(100, ret=msg.message)

    return _deco




def user_get_org_msg(kwargs):  # 普通用户获取组织信息
    try:
        orgs_user = g.db_session.query(OrgsUser).filter(
            OrgsUser.org_id == kwargs['orga_uuid_arg'],
            OrgsUser.uid == kwargs['uid'],
            OrgsUser.is_delete == '0').first()

        if orgs_user is None:
            return request_result(806)

        orga_msg = dict()
        orga_msg['role'] = orgs_user.role

        orgs_b = g.db_session.query(OrgsBase).filter(
            OrgsBase.org_id == kwargs['orga_uuid_arg'], OrgsBase.is_delete == '0').first()

        if orgs_b is None:
            return request_result(100, ret='no org msg , this is error')

        orga_msg['orga_name'] = orgs_b.org_name
        orga_msg['orga_detail'] = orgs_b.org_detail
        orga_msg['is_public'] = orgs_b.is_public
        orga_msg['creation_time'] = orgs_b.creation_time
        orga_msg['delete_time'] = orgs_b.delete_time

        return request_result(0, ret=orga_msg)
    except Exception as msg:
        return request_result(403, ret=msg.message)


def admin_get_org_msg(kwargs):  # 系统管理员获取组织信息
    try:
        orga_msg = dict()

        orgs_b = g.db_session.query(OrgsBase).filter(
            OrgsBase.org_id == kwargs['orga_uuid_arg']).first()

        if orgs_b is None:
            return request_result(100, ret='no org msg , this is error')

        orga_msg['orga_name'] = orgs_b.org_name
        orga_msg['orga_detail'] = orgs_b.org_detail
        orga_msg['is_public'] = orgs_b.is_public
        orga_msg['creation_time'] = orgs_b.creation_time
        orga_msg['delete_time'] = orgs_b.delete_time
        orga_msg['is_delete'] = orgs_b.is_delete

        return request_result(0, ret=orga_msg)
    except Exception as msg:
        return request_result(403, ret=msg.message)


@check_headers
@get_userinfo_by_payload
# @check_orga_uuid
@check_orga_uuid_admin  # 系统管理员可以操作
def get_org_msg(kwargs):  # 获取组织信息

    # 系统管理员默认具有全部操作; 此步必须先行判断
    if int(kwargs['role_uuid']) == OrgaRole.SystemGod.value:
        return admin_get_org_msg(kwargs)

    return user_get_org_msg(kwargs)



@check_headers
@get_userinfo_by_payload
@check_orga_uuid
def leave_orga(kwargs):  # 离开组织
    try:
        orgs_user = g.db_session.query(OrgsUser).filter(
            OrgsUser.org_id == kwargs['orga_uuid_arg'], OrgsUser.uid == kwargs['uid'],
            OrgsUser.is_delete == '0').first()

        if orgs_user is None:
            return request_result(806)

        if orgs_user.role == str(OrgaRole.OrgaMaster.value):  # 群主不能离开组织
            return request_result(810)

        g.db_session.query(OrgsUser).filter(
            OrgsUser.org_id == kwargs['orga_uuid_arg'], OrgsUser.uid == kwargs['uid']).update(
            {"is_delete": '1', "update_time": get_now_time()})
        g.db_session.commit()

        return get_login_token(kwargs['user_name'])  # 离开组织,给用户返回token
        # return request_result(0, ret=retdict)
    except Exception as msg:
        return request_result(403, ret=msg.message)


@check_headers
@get_userinfo_by_payload
@check_orga_uuid
def delete_org(kwargs):  # 删除组织
    try:

        # 这里需要  判断组织下是否还有,运行的资源与服务  需要外部提供接口
        orgs_user = g.db_session.query(OrgsUser).filter(
            OrgsUser.org_id == kwargs['orga_uuid_arg'], OrgsUser.role == OrgaRole.OrgaMaster.value,
            OrgsUser.uid == kwargs['uid']).first()

        if orgs_user is None:
            return request_result(806)

        g.db_session.query(OrgsBase).filter(OrgsBase.org_id == kwargs['orga_uuid_arg']).update(
            {"is_delete": '1'})
        g.db_session.query(OrgsUser).filter(OrgsUser.org_id == kwargs['orga_uuid_arg']).update(
            {"is_delete": '1'})
        g.db_session.commit()
        # return request_result(0)
        return get_login_token(kwargs['user_name'])  # 返回用户token
    except Exception as msg:
        return request_result(403, ret=msg.message)


class OrganizationBaseMsg(Resource):
    def get(self, orga_uuid):
        """
        @apiName get
        @apiGroup OrganizationBaseMsg
        @apiDescription     获取组织信息(仅仅只有组织信息,组织内部成员皆可以获取该信息)
        @apiVersion 1.0.0
        @apiHeader {String} token 请求接口的token,放在请求头中
        @api {get} /api/v1.0/usercenter/orgs/<string:orga_uuid>  获取组织信息

        @apiSuccessExample {json} 获取组织信息:
            {
                "status": 0,
                "msg": "OK",
                "result":
                {
                    "role": "1deca42474872abcdefef34",  # 当前用户在该组织中的角色
                    "orga_name": "org_name",             # 组织名
                    "orga_detail": "org_detail",         # 组织详情
                    "is_public": "0",                   # 是否公开
                    "creation_time": "20123-23-23-2-",  # 组织创建日期
                }
            }

        @apiParam {String} orga_uuid 组织id
        """
        k = dict()
        k['orga_uuid_arg'] = orga_uuid
        print "OrganizationBaseMsg"
        print orga_uuid
        return jsonify(get_org_msg(k))


    def put(self, orga_uuid):
        """
        @apiName put
        @apiGroup OrganizationBaseMsg
        @apiDescription       离开组织(在用户界面就可以操作调用该接口,自己主动离开组织,组织拥有者不可以离开组织)
        @apiVersion 1.0.0
        @apiHeader {String} token 请求接口的token,放在请求头中
        @api {put} /api/v1.0/usercenter/orgs/<string:orga_uuid>  离开组织

        @apiSuccessExample {json} 获取组织信息:
            {
                "status": 0,
                "msg": "OK",
                "result":{}
            }
        @apiParam {String} orga_uuid 组织id
        """
        k = dict()
        k['orga_uuid_arg'] = orga_uuid
        return jsonify(leave_orga(k))

    def delete(self, orga_uuid):
        """
        @apiName delete
        @apiGroup OrganizationBaseMsg
        @apiDescription     解散组织,只有组织拥有者才可以删除组织
        @apiVersion 1.0.0
        @apiHeader {String} token 请求接口的token,放在请求头中
        @api {delete} /api/v1.0/usercenter/orgs/<string:orga_uuid>/users  解散组织

        @apiSuccessExample {json} :
            {
                "status": 0,
                "msg": "OK",
                "result": "some msg"
            }

        @apiParam {String} org_id 组织id
        """
        k = dict()
        k['orga_uuid_arg'] = orga_uuid
        return jsonify(delete_org(k))
