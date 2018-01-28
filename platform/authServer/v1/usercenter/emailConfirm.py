#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/12/9 10:25
"""


import requests
import json

from flask import jsonify, g, request, render_template, redirect
from flask_restful import Resource

from authServer.pyTools.tools.codeString import request_result
from authServer.models.hub_db_meta import OrgsUser, OrgsBase, UserBase, ActionCode

class EmailConfirm(Resource):
    def get(self, opcode, action):
        """
        @apiGroup UserSignup
        @apiDescription     用户注册, 邮件确认
        @apiVersion 1.0.0
        @api {get} /api/v1.0/usercenter/users/email/<string:opcode>/<string:action>  邮件确认

        @apiParam {String} opcode  操作码
        @apiParam {String} action  动作
        """

        ac_opt = g.db_session.query(ActionCode).filter(
            ActionCode.opcode == opcode, ActionCode.action == action).first()

        if ac_opt is None:
            return jsonify(request_result(806, ret='The confirmation code is invalid or is already in use'))

        try:
            g.db_session.query(UserBase).filter(UserBase.user_id == ac_opt.user_id).update(
                {"is_active": '1'}
            )
            g.db_session.query(ActionCode).filter(
                ActionCode.opcode == opcode, ActionCode.action == action).delete()

            g.db_session.commit()
            ret = request_result(0)
        except Exception as msg:
            ret = request_result(403, ret=msg.message)
        finally:

            # 处理初始化余额

            # from authServer.common.usercenter.token import get_login_token
            #
            # from authServer.conf.conf import INITBILLING
            #
            # retdict = get_login_token(username=ac_opt.user_id, isuuid=True)
            #
            # print "EmailConfirm - get_login_token"
            # print "EmailConfirm : " + retdict
            #
            # try:
            #     headers = {
            #         'token': retdict['result']['token']
            #     }
            #     bolret = requests.post(url=INITBILLING, headers=headers, timeout=5)
            # except Exception as msg:
            #     print "EmailConfirm :" + msg.message
            #     return request_result(100, ret=bolret)
            #
            # print "EmailConfirm : " + bolret

            return redirect('/login')