#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/8/15 2:06
@func: 装饰函数,主要用于参数校验和用户认证
"""


#from authServer.models.harbor_db_meta import User
import time

import authServer.pyTools.token.token as TK
from authServer.models.hub_db_meta import UserBase, Session, OrgsBase
from authServer.pyTools.tools.codeString import request_result

from flask import g


# 用户名是否已经存在; True 存在;  False 不存在
def username_exist(username):
    ret = g.db_session.query(OrgsBase).filter(OrgsBase.org_name == username).first()
    if ret is None:
        return False
    return True


# 邮箱是否已经被注册; True 存在;  False 不存在
def email_exist(email):
    ret = g.db_session.query(UserBase).filter(UserBase.email == email).first()
    if ret is None:
        return False
    return True


def is_email(username):
    """
    判断登录时,使用的登录id是否是邮箱
    :return : True 是邮箱; False 不是邮箱
    """
    if '@' in username:
        return True
    return False


def login_username(username, password):
    """
    使用用户名登录
    :return : 成功返回True, 失败返回False
    """

    ret = g.db_session.query(UserBase).filter(UserBase.username == username).first()
    if ret is None:
        return False
    # password = TK.encrypy_pbkdf2(self.password, self.salt)

    if ret.password == TK.encrypy_pbkdf2(password, ret.salt.decode('utf-8').encode('utf-8')):
        return True
    return False


def get_uuid_by_name(username):
    """ 通过用户名得到用户的uuid """
    ret = g.db_session.query(UserBase).filter(UserBase.username == username).first()
    if ret is None:
        return None
    return ret.user_id

def get_orgsuuid_by_name(username):
    """ 通过组织名得到组织的uuid """
    ret = g.db_session.query(OrgsBase).filter(OrgsBase.org_name == username).first()
    if ret is None:
        return None
    return ret.org_id


def login_email(email, password):
    """
    使用邮箱登录
    :return : 成功返回True, 失败返回False
    """
    session = Session()
    ret = session.query(UserBase).filter(UserBase.email == email).first()
    session.close()
    if ret is None:
        return False

    if ret.password == TK.encrypy_pbkdf2(password, ret.salt.decode('utf-8').encode('utf-8')):  # 验证密码
        return True
    return False


# 调用这个之前,先调用check_args(是否合理,是否让登录失败的用户知道自己的用户名输入错误,系统中不存在)
def check_username_password(func):
    def _deco(username, password):
        """
        登录用户名/邮箱、密码检测
        """
        retdict = request_result(705)  # 直接705 用户名或密码错误
        if is_email(username) and (login_email(email=username, password=password) is False):
            return retdict

        if (is_email(username) is False) and (login_username(username=username, password=password) is False):
            return retdict

        return func(username, password)
    return _deco




def check_args(existIsOK=True):
    """
    检查输入参数是否合法: username, email
    :param existIsOK: True 不存在返回失败信息,存在则合法(申请token);
                      False 存在返回失败信息,不存在则合法(适合注册时使用)
    :return:
    """
    def _deco(func):
        def __deco(*args, **kwargs):
            retdict = request_result(706)  # 验证参数之前,统一标记为有问题
            if 'username' in kwargs and existIsOK:
                if username_exist(kwargs['username']) is False:
                    return request_result(701)  # 用户名没被有注册

            if 'username' in kwargs and (existIsOK is False):
                if username_exist(kwargs['username']):
                    return request_result(702) # 用户名已经被注册

            if 'email' in kwargs and existIsOK:
                if email_exist(kwargs['email']) is False:
                    return request_result(703)  #邮箱没有被注册

            if 'email' in kwargs and (existIsOK is False):
                if email_exist(kwargs['email']):
                    return request_result(704) # 邮箱已经有被注册

            return func(*args, **kwargs)
        return __deco
    return _deco


def signup_check(func):
    def _deco(kwargs):
        if username_exist(kwargs['username']):
            return request_result(702)

        if email_exist(kwargs['email']):
            return request_result(704)

        return func(kwargs)
    return _deco