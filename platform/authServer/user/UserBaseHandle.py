#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/9/23 10:23
"""

from flask import g
import uuid
from authServer.models.hub_db_meta import UserBase, OrgsBase, OrgsUser
from authServer.pyTools.tools.codeString import request_result
import authServer.pyTools.token.token as TK
from authServer.pyTools.tools.timeControl import get_now_time

from authServer.v1.usercenter.orgs_base import make_orgs


from authServer.conf.conf import CONFIRM_EMAIL

# 初始化余额失败;数据回滚;   这种处理太麻烦
def SigupFailure(org_id, user_id):
    try:
        # 删除组织中的人
        org_user = OrgsUser(org_id=org_id, uid=user_id)
        g.db_session.delete(org_user)
        g.db_session.commit()

        # 删除组织
        org_base = OrgsBase(org_id=org_id)
        g.db_session.delete(org_base)
        g.db_session.commit()

        # 删除用户
        user_b = UserBase(user_id=user_id)
        g.db_session.delete(user_b)
        g.db_session.commit()
        return request_result(0)

    except Exception as msg:
        return request_result(401, ret=msg.message)

# 加解密注意;存取数据到数据库中的格式
class UserBaseHandle:

    def __init__(self):
        pass


    def siggup_init(self, user_name, email, password):  # 注册初始化
        self.user_name = user_name
        self.email = email
        self.salt = self.get_salt()
        self.save_password = self.get_save_password(password, self.salt)

        print "------000---"
        print self.user_name
        print self.salt
        print self.save_password

        self.uuid = uuid.uuid3(uuid.NAMESPACE_DNS, self.user_name).__str__()
        now_time = get_now_time()

        try:
            user_base = UserBase(
                user_id=self.uuid,
                username=self.user_name,
                email=self.email,
                password=self.save_password,
                creation_time=now_time,
                update_time=now_time,
                salt=self.salt)
            g.db_session.add(user_base)
            g.db_session.commit()
        except Exception as msg:
            return request_result(401, ret=msg.message)


        from authServer.v1.usercenter.passwordFind import SendFindEmail
        from authServer.conf.conf import callback_url

        if CONFIRM_EMAIL:
            print 'callback_url'
            print callback_url

            sendret = SendFindEmail(self.user_name,
                           action='ConfirmEmail',
                           callback_url=callback_url,
                           email_template='email_confirm.html'
                           )

            print 'sendret'
            print sendret

        try:
            ret = make_orgs(uid=self.uuid, user_name=self.user_name, org_name=self.user_name)

            if 'status' in ret and ret['status'] == 0:
                return ret
        except Exception as msg:

            print 'error'
            print msg.message
            user_b = UserBase(user_id=self.uuid)
            g.db_session.delete(user_b)
            g.db_session.commit()

            return request_result(401, ret=msg.message)



    @staticmethod
    def get_salt():  #  获取一个干扰种子
        return TK.GenerateRandomString(randlen=32)

    @staticmethod
    def get_save_password(clear_pwd, salt):  # 根据明文密码和种子, 得到存储密码
        return TK.encrypy_pbkdf2(clear_pwd, salt)

    def get_user_base(self, user_name):
        """ 从数据库中获取基本信息 """
        user_base = g.db_session.query(UserBase).filter(UserBase.username == user_name).first()
        if user_base is not None:
            self.user_name = user_name
            self.email = user_base.email   # 用户邮箱
            self.save_password = user_base.password  # 用户密码(转加密之后的存储密码)
            self.deleted = user_base.deleted   # 是否被删除
            self.salt = user_base.salt  # 密码加密时的 salt
            self.logo = user_base.logo


    def change_password(self, new_pwd):
        """
        修改密码, 修改密码时同时把 密码干扰种子 更新一次
        :type new_pwd: 新密码
        """

        # self.get_user_base()
        # if self.login_username(old_p) is False:
        #     return request_result(705)

        self.salt = self.get_salt()
        self.save_password = self.get_save_password(new_pwd, self.salt)

        try:
            g.db_session.query(UserBase).filter(UserBase.username == self.user_name).update(
                {"password": self.save_password , 'salt': self.salt}
            )
            g.db_session.commit()
            ret = request_result(0)
        except Exception as msg:
            ret = request_result(403, ret=msg.message)
        finally:
            return ret

    def login_username(self, password):
        """
        使用用户名登录
        :return : 成功返回True, 失败返回False
        """

        save_password = self.get_save_password(password, self.salt.decode('utf-8').encode('utf-8'))

        print "save_password"
        print password
        print type(password)
        print save_password
        print self.save_password
        print self.user_name
        print self.salt

        # self.salt
        # 020f6ef14709d00676eae931ffe5f761

        # self.save_password
        # c8138b48928789a46cd40c5cc61f5998
        # == == =

        if self.save_password  == save_password:
            return True
        return False

    def change_logo(self, new_logo):

        try:
            g.db_session.query(UserBase).filter(UserBase.username == self.user_name).update(
                {"logo": new_logo})
            g.db_session.commit()
            self.logo = new_logo
            ret = request_result(0)
        except Exception as msg:
            ret = request_result(403, ret=msg.message)
        finally:
            return ret

