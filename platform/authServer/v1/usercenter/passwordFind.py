#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/12/5 17:10
@func: 找回密码
"""

import json
import time
from flask import request, jsonify, g
from flask_restful import Resource
from authServer.tools.db_check import is_email

from authServer.pyTools.tools.codeString import request_result
from authServer.models.hub_db_meta import OrgsUser, OrgsBase, UserBase, ActionCode
from authServer.pyTools.token.token import get_password_by_name_password_salt, GenerateRandomString
from authServer.pyTools.tools.timeControl import get_now_time

FindPassword = 100

VerifyEmail = 200


ActionCodeDict = dict()
# ActionCode['FindPassword'] = FindPassword()  # 找回密码
# ActionCode['VerifyEmail'] = VerifyEmail()    # 验证邮箱



import requests
from authServer.conf.conf import SEND_EMAIL_URL

from flask import render_template


def SentEmail(to, title, text, html):
    data = {
        "to": to,
        "title": title,
        "text": text,
        "html": html
    }

    headers = {
        'content-type': "application/json"
    }

    try:
        data = json.JSONEncoder().encode(data)
        ret = requests.request(method='POST', url=SEND_EMAIL_URL, data=data, headers=headers)

        print 'SentEmail ret'
        print ret.content

        ret_status = json.loads(ret.content)

        if 'status' in ret_status and 0 == ret_status['status']:
            return True, request_result(0, ret=ret.content)
        return False, request_result(100, ret=ret.content)
    except Exception as msg:
        return False, request_result(100, ret=ret.content)




def GenerateActionCode(func):
    """ 根据用户名 生成唯一的 code """
    def _deco(username, **kwargs):
        if is_email(username):
            userBase = g.db_session.query(UserBase).filter(UserBase.email == username).first()
        else:
            userBase = g.db_session.query(UserBase).filter(UserBase.username == username).first()

        if userBase is None:
            return request_result(701)

        email = userBase.email
        user_id = userBase.user_id
        password = GenerateRandomString(32)
        opcode = get_password_by_name_password_salt(
            name=userBase.email.decode('utf-8').encode('utf-8'),
            password=password,
            salt=userBase.salt.decode('utf-8').encode('utf-8')
        )
        kwargs['opcode'] = opcode
        kwargs['user_id'] = user_id
        kwargs['email'] = email
        return func(username, **kwargs)
    return _deco



def SetActionCode(user_id, opcode, action):

    creation_time = get_now_time()
    expire_time = get_now_time(time.time() + 60 * 60 * 24)

    try:

        ac_opt = g.db_session.query(ActionCode).filter(
            ActionCode.user_id == user_id, ActionCode.action == action).first()

        if ac_opt is None:
            AC = ActionCode(
                user_id=user_id,
                opcode=opcode,
                action=action,
                creation_time=creation_time,
                expire_time=expire_time
            )

            g.db_session.add(AC)
        else:
            g.db_session.query(ActionCode).filter(ActionCode.user_id == user_id, ActionCode.action == action).update(
                {"creation_time": creation_time, "expire_time": expire_time, 'opcode': opcode})
        g.db_session.commit()
        return True, request_result(0)
    except Exception as msg:
        return False, request_result(403, ret=msg.message)




@GenerateActionCode
def SendFindEmail(username, **kwargs):
    retbool, retmsg = SetActionCode(user_id=kwargs['user_id'], opcode=kwargs['opcode'], action=kwargs['action'])

    if retbool is False:
        return retmsg
    # "http://boxlinker.com/?opcode=$OPCODE&action=$ACTION"
    FindPasswordUrl = kwargs['callback_url'].replace('$OPCODE', kwargs['opcode']).replace('$ACTION', kwargs['action'])

    # FindPasswordUrl = kwargs['callback_url'] + '/?opcode=' + kwargs['opcode'] + '&action=' + kwargs['action']

    rethtml = render_template(kwargs['email_template'], ActionCodeConfirm=FindPasswordUrl)

    retbool, retmsg = SentEmail(to=kwargs['email'], title='boxlinker password help', text='', html=rethtml)
    if retbool is False:
        return retmsg


    return request_result(0, ret=FindPasswordUrl)



class PasswordFindEmail(Resource):
    """ 获取通过邮箱找回密码链接 """
    def post(self):
        """
        @apiGroup Password
        @apiDescription 找回密码
        @apiVersion 1.0.0
        @api {post} /api/v1.0/usercenter/passwords/email  获取找回密码,链接
        @apiExample {get} Example usage:
        get http://auth.boxlinker.com/api/v1.0/usercenter/passwords/email  Example:
            {
                "user_name": asss,
                "callback_url: "http://boxlinker.com/?opcode=$OPCODE&action=$ACTION"
            }


FindPasswordUrl = kwargs['callback_url'] + '/?opcode=' + kwargs['opcode'] + '&action=' + kwargs['action']


        @apiSuccessExample {json} 返回token信息:
        {
            "msg": "OK",
            "result": []
            "status": 0
        }
        @apiParam {String} user_name  用户名（其中user_name可以是用户名或邮箱）
        """
        try:
            data = request.data
            data_json = json.loads(data)
            user_name = data_json.get('user_name', '').decode('utf-8').encode('utf-8')
            callback_url = data_json.get('callback_url', '').decode('utf-8').encode('utf-8')
            if user_name == '' or callback_url == '':
                return request_result(706)

            if '$OPCODE' not in callback_url or '$ACTION' not in callback_url:
                return request_result(706, ret='$OPCODE and $ACTION not in callback_url')
        except Exception as msg:
            return request_result(710, ret=msg.message)

        return jsonify(SendFindEmail(user_name,
                                     action='FindEmail',
                                     callback_url=callback_url,
                                     email_template='findpassword.html'
                                     ))


    def get(self, opcode, action):
        """
        @apiGroup Password
        @apiDescription 验证操作码
        @apiVersion 1.0.0
        @api {get} /api/v1.0/usercenter/passwords/email/<string:opcode>/<string:action>  验证操作吗的正确性
        @apiExample {get} Example usage:
        get http://auth.boxlinker.com/api/v1.0/usercenter/passwords/email/<string:opcode>/<string:action>  Example:

        @apiSuccessExample {json} 返回token信息:
        {
            "msg": "OK",
            "result": []
            "status": 0
        }

        @apiParam {String} opcode  操作码
        @apiParam {String} action  动作

        """
        ac_opt = g.db_session.query(ActionCode).filter(
            ActionCode.opcode == opcode, ActionCode.action == action).first()

        if ac_opt is None:
            return jsonify(request_result(809))

        return jsonify(request_result(0))

    def put(self, opcode, action):
        """
        @apiGroup Password
        @apiDescription 修改密码
        @apiVersion 1.0.0
        @api {put} /api/v1.0/usercenter/passwords/email/<string:opcode>/<string:action> 修改密码
        @apiExample {put} Example usage:
        put http://auth.boxlinker.com/api/v1.0/usercenter/passwords/email/<string:opcode>/<string:action>  Example:

            {
                "new_password": "ssss"
            }

        @apiSuccessExample {json} 返回token信息:
        {
            "msg": "OK",
            "result": []
            "status": 0
        }

        @apiParam {String} opcode  操作码
        @apiParam {String} action  动作

        """
        try:
            data = request.data
            data_json = json.loads(data)
            new_password = data_json.get('new_password', '').decode('utf-8').encode('utf-8')
            if new_password == '':
                return request_result(706)
        except Exception as msg:
            return request_result(710, ret=msg.message)


        ac_opt = g.db_session.query(ActionCode).filter(
            ActionCode.opcode == opcode, ActionCode.action == action).first()

        if ac_opt is None:
            return jsonify(request_result(806))

        import authServer.pyTools.token.token as TK
        salt = TK.GenerateRandomString(randlen=32)
        save_password = TK.encrypy_pbkdf2(new_password, salt)

        try:
            g.db_session.query(UserBase).filter(UserBase.user_id == ac_opt.user_id).update(
                {"password": save_password, 'salt': salt}
            )

            g.db_session.query(ActionCode).filter(
                ActionCode.opcode == opcode, ActionCode.action == action).delete()

            g.db_session.commit()
            ret = request_result(0)


        except Exception as msg:
            ret = request_result(403, ret=msg.message)
        finally:
            return jsonify(ret)




#
#
# class EmailActionCode(Resource):
#     """ 验证操作码是否正确 """
#     def post(self):
#         """
#         @apiGroup Password
#         @apiDescription 找回密码
#         @apiVersion 1.0.0
#         @apiName 找回密码
#         @api {post} /api/v1.0/usercenter/passwords/email  获取找回密码,链接
#         @apiExample {get} Example usage:
#         get http://auth.boxlinker.com/api/v1.0/usercenter/passwords/email  Example:
#             {
#                 "user_name": asss,
#                 "callback_url: "boxlinker.com"
#             }
#
#         @apiSuccessExample {json} 返回token信息:
#         {
#             "msg": "OK",
#             "result": []
#             "status": 0
#         }
#         @apiParam {String} user_name  用户名（其中user_name可以是用户名或邮箱）
#         """
#         try:
#             data = request.data
#             data_json = json.loads(data)
#             user_name = data_json.get('user_name', '').decode('utf-8').encode('utf-8')
#             if user_name == '':
#                 return request_result(706)
#         except Exception as msg:
#             return request_result(710, ret=msg.message)
#
#         return jsonify(SendFindEmail(user_name))