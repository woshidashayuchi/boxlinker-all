#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/8/16 10:05
@func: 用户注册视图
"""

from flask import request, jsonify
from flask_restful import Resource

from authServer.user.user import UserHandle
from authServer.pyTools.tools.codeString import request_result


def request_form_get_username_email_password(func):
    """ form 表单中只有 username 和 password 参数"""
    def _deco():
        try:
            username = request.form.get('username', '').decode('utf-8').encode('utf-8')  # 用户名
            email = request.form.get('email', '').decode('utf-8').encode('utf-8')  # 邮箱
            password = request.form.get('password', '').decode('utf-8').encode('utf-8')  # 密码
        except Exception as msg:
            ret = request_result(601, ret={'msg': msg.message})
            return ret

        # 传入的参数有问题
        if username == '' or password == '' or email == '':
            ret = request_result(706)
            return ret
        return func(username=username, email=email, password=password)
    return _deco


@request_form_get_username_email_password
def _signup(username, email, password):
    user = UserHandle(username=username, email=email, password=password)
    return user.sign_up()


class signup(Resource):
    def post(self):
        """
        @apiDescription 注册用户操作
        @apiVersion 1.0.0
        @api {post} /user/signup
        @apiExample {post} Example usage: 数据放进 form 中
        post http://auth.boxlinker.com/user/signup Python Example

            def test_signup(username, password, email):
                urltag = url + '/user/signup'
                data = {
                    'username': username,
                    'password': password,
                    'email': email
                }
                response = requests.request('POST', url=urltag, data=data)
                return response.text.decode('utf-8').encode('utf-8')

        JavaScript Example:
            var form = new FormData();
            form.append("username", "2232");   // 用户名
            form.append("password", "QAZwsx123");   // 密码
            form.append("email", "wweswww3s@223w23w2.com");  // 邮箱

            var settings = {
              "async": true,
              "crossDomain": true,

              // 本机测试服务器地址 http://127.0.0.1:5000   ,阿里云服务地址 http://123.56.9.18:8080
              "url": "http://127.0.0.1:5000/user/signup",
              "method": "POST",
              "headers": {
                "cache-control": "no-cache",
                "postman-token": "3e2180d2-2a0f-9126-004b-77412051f5d2"
              },
              "processData": false,
              "contentType": false,
              "mimeType": "multipart/form-data",
              "data": form
            }

            $.ajax(settings).done(function (response) {
              console.log(response);
            });

        @apiParam {String} username  用户名
        @apiParam {String} password  用户密码
        @apiParam {String} email     用户邮箱(唯一)
        """
        return jsonify(_signup())