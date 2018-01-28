#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/9/23 10:56
"""

import os
import json
from flask import jsonify, request
from flask_restful import Resource
from werkzeug.utils import secure_filename


from authServer.common.decorate import get_token_from_headers_check
from authServer.tools.decorate import get_username_uid_by_payload
from authServer.pyTools.tools.codeString import request_result
from authServer.pyTools.tools.timeControl import get_timestamp_13

from authServer.user.UserBaseHandle import UserBaseHandle


def get_json_data(func):
    def _deco():
        try:
            data = request.data
        except Exception as msg:
            return request_result(710, ret=msg.message)
        return func(data)
    return _deco

def get_oldp_newp():
    """
    从请求中获取 原始密码和新密码, old_p 和 new_p
    {
        old_p: "old_password",
        new_p: "new_password"
    }
    :return:
    """
    try:
        data = request.data

        print data
        data_json = json.loads(data)
    except Exception as msg:
        return False, None, None, request_result(710, ret=msg.message)

    if 'old_p' in data_json and 'new_p' in data_json:
        return True, data_json['old_p'].decode('utf-8').encode('utf-8'), data_json['new_p'].decode('utf-8').encode('utf-8'), None
    else:
        return False, None, None, request_result(706)




from authServer.common.decorate import check_headers, get_userinfo_by_payload

@check_headers
@get_userinfo_by_payload
def change_password(kwargs={}):

    retbool, old_p, new_p, msg = get_oldp_newp()
    if not retbool:
        return msg




    UserBhandle = UserBaseHandle()
    UserBhandle.get_user_base(kwargs['user_name'])

    if UserBhandle.login_username(old_p) is False:
        return request_result(705)

    return UserBhandle.change_password(new_pwd=new_p)


class PassWord(Resource):
    """ 密码相关操作 """
    def post(self):
        """
        @apiDescription   修改密码操作
        @apiVersion 1.0.0
        @apiHeader {String} token 请求接口的token,放在请求头中
        @api {post} /user/password
        @apiParam {String} old_p  原始密码
        @apiParam {String} new_p  新密码
        @apiParamExample {json} Request-Example: data 数据
        {"old_p": "admin", "new_p": "admin"}
        """
        return jsonify(change_password())



ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = '/Users/lzp/Desktop/PythonTools/authServer/user'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def file_suffix(filename):
    if '.' in filename:
        return filename.rsplit('.', 1)[1]
    return None


@get_token_from_headers_check
@get_username_uid_by_payload
def upload_logo(user_name, uid):
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        image_suffix = file_suffix(filename)

        image_name = 'logo' + str(get_timestamp_13()) + '.' + image_suffix

        user_log_path = os.path.join(UPLOAD_FOLDER, user_name)

        if os.path.exists(user_log_path) is False:
            os.mkdir(user_log_path)

        file.save(os.path.join(user_log_path, image_name))
        UserBhandle = UserBaseHandle(user_name=user_name)
        return UserBhandle.change_logo(image_name)
    else:
        return request_result(100, ret='file name is error')


@get_token_from_headers_check
@get_username_uid_by_payload
def get_logo(user_name, uid):
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        image_suffix = file_suffix(filename)

        image_name = 'logo' + str(get_timestamp_13()) + '.' + image_suffix

        user_log_path = os.path.join(UPLOAD_FOLDER, user_name)

        if os.path.exists(user_log_path) is False:
            os.mkdir(user_log_path)

        file.save(os.path.join(user_log_path, image_name))
        UserBhandle = UserBaseHandle(user_name=user_name)
        return UserBhandle.change_logo(image_name)
    else:
        return request_result(100, ret='file name is error')



class PersonalHead(Resource):
    def post(self):
        """
        @apiDescription   个人头像
        @apiVersion 1.0.0
        @apiHeader {String} token 请求接口的token,放在请求头中
        @api {post} /user/personalhead
        """
        return jsonify(upload_logo())

    def get(self):
        """
        @apiDescription   获取个人头像地址
        @apiVersion 1.0.0
        @apiHeader {String} token 请求接口的token,放在请求头中
        @api {get} /user/personalhead
        """
        return jsonify(get_logo())