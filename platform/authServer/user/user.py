#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/8/11 下午5:25
"""

import json
import uuid
from flask import jsonify, g

from flask_restful import Resource
import authServer.pyTools.token.token as TK

from authServer.models.hub_db_meta import Session
from authServer.models.hub_db_meta import UserBase, GitHubOauth
from authServer.tools.db_check import check_args
from authServer.pyTools.tools.codeString import request_result
from authServer.pyTools.tools.timeControl import get_now_time





@check_args(existIsOK=False)
def do_sign_up(uuid, username, email, password, deleted,
             creation_time, update_time, sysadmin_flag, salt):
    try:
        retdict = request_result(0)
        # 主服务系统注册
        new_user_hub = UserBase(user_id=uuid, username=username, email=email, password=password,
                        deleted=deleted,
                        creation_time=creation_time, update_time=update_time,
                        sysadmin_flag=sysadmin_flag, salt=salt)

        g.db_session.add(new_user_hub)
        g.db_session.commit()
    except Exception as msg:
        retdict = request_result(601, ret={'msg': msg.message})
    finally:
        return retdict




# 用户操作
class UserHandle:
    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password

    def init_sigin_up(self):
        """ 注册用户信息初始化 """
        self.set_deleted()
        self.set_sysadmin_flag()
        self.set_salt()
        self.set_save_password()
        self.set_creation_time()
        self.set_update_time()
        self.uuid = uuid.uuid3(uuid.NAMESPACE_DNS, self.username).__str__()


    # 用户注册
    def sign_up(self):
        self.init_sigin_up()
        ret = do_sign_up(
            uuid=self.uuid,
            username=self.username, email=self.email, password=self.save_password,
            deleted=self.deleted, creation_time=self.creation_time, update_time=self.update_time,
            sysadmin_flag=self.sysadmin_flag, salt=self.salt)
        return ret

    def login(self):
        """ 用户登录 """
        pass


    # 设置用户名
    def set_username(self, username):
        self.username = username

    # 设置邮箱
    def set_email(self, email):
        self.email = email

    # 设置密码
    def set_password(self, password):
        self.password = password


    # 系统管理员账号标志
    def set_sysadmin_flag(self):
        self.sysadmin_flag = 0

    def set_creation_time(self):
        self.creation_time = get_now_time()

    def set_update_time(self):
        self.update_time = get_now_time()

    # # 用户在数据库中编号(主键)
    # def get_user_id(self):
    #     self.user_id =

    # 用户是否被删除 1是删除
    def set_deleted(self, default=0):
        self.deleted = default


    def set_salt(self):
        self.salt = TK.GenerateRandomString(randlen=24) + '-0242ac120004'

    def set_save_password(self):
        self.save_password = TK.encrypy_pbkdf2(self.password, self.salt)






class UserInfo(Resource):
    def get(self):
        from authServer.common.usercenter.users import get_user_info
        return jsonify(get_user_info())