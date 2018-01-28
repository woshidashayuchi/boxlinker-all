#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/8/22 1:21
@请求预处理函数,装饰函数
"""

import json
from flask import request, g

from authServer.models.hub_db_meta import ImageRepository

from authServer.pyTools.tools.codeString import request_result
from authServer.pyTools.token.token import get_payload
from authServer.common.checktoken import system_check_token





def get_username_uid_by_payload(func):
    """ 通过 payload 获取用户名和用户id"""
    def _deco(payload):
        try:
            payload_d = json.loads(payload)
        except Exception as msg:
            return request_result(206, ret=msg.message)  # payload 中没有需要的信息

        if 'user_name' in payload_d and 'uid' in payload_d:
            return func(user_name=payload_d['user_name'].decode('utf-8').encode('utf-8'),
                        uid=payload_d['uid'].decode('utf-8').encode('utf-8'))
        return request_result(206)  # payload 中没有需要的信息
    return _deco




# 从请求头中获取一个参数的数据,需要验证token之后
# 用于请求token中含有两个参数, 1.token 2.参数
# 其中参数是用来执行其他操作需要的一个参数, 为了方便统一命名 var_box
def get_varbox_from_headers(func):
    def _deco(payload):
        try:
            print 'sdsdsdsds'
            var_box = request.headers.get('varbox', default='').decode('utf-8').encode('utf-8')
        except Exception as msg:
            retdict = request_result(601, ret={'msg': msg.message})
            return retdict
        print 'var_box :' + str(var_box)
        if var_box == '':
            retdict = request_result(706, ret='no var_box')
            return retdict

        return func(payload, var_box)
    return _deco





def request_form_get_username_password(func):
    """ form 表单中只有 username 和 password 参数"""
    def _deco():
        try:
            # 用户名/也可能是邮箱 需要后台判断
            username = request.form.get('user_name', '').decode('utf-8').encode('utf-8')
            password = request.form.get('password', '').decode('utf-8').encode('utf-8')  # 密码
        except Exception as msg:
            retdict = request_result(601, ret={'msg': msg.message})
            return retdict

        # 传入的参数有问题
        if username == '' or password == '':
            retdict = request_result(706)
            return retdict
        return func(username=username, password=password)
    return _deco


def request_create_image_project(func):
    """ 获取新建仓库的名称、公有还是私有、简单描述、详细描述,进行装饰器解析, 并且验证 repositories 是否存在 """
    def _deco(*args, **kwargs):
        try:
            data = request.data
            data_json = json.loads(data)
            is_public = data_json.get('is_public', '').decode('utf-8').encode('utf-8')
            short_description = data_json.get('short_description', '').decode('utf-8').encode('utf-8')
            detail = data_json.get('detail', '').decode('utf-8').encode('utf-8')
            repositories = data_json.get('repositories', '').decode('utf-8').encode('utf-8')
        except Exception as msg:
            return request_result(710, ret=msg.message)


        # 传入的参数有问题
        if str(is_public) != '0' and str(is_public) != '1':
            return request_result(706, ret='is_public is error')

        kwargs['is_public'] = str(is_public)
        kwargs['short_description'] = short_description
        kwargs['detail'] = detail

        repositories = kwargs['user_name'] + '/' + repositories  # 前端页面传进来是不含有  用户名 和 /
        kwargs['repositories'] = repositories

        imagelist = repositories.split('/')
        if len(imagelist) != 2:  # 镜像地址不合法
            return request_result(706, ret='repositories is error')

        ret = g.db_session.query(ImageRepository).filter(ImageRepository.repository == repositories).first()

        if ret is not None:
            return request_result(706, ret='repository_name is exist')

        return func(*args, **kwargs)
    return _deco


# 自动构建
def request_form_git_build(func):
    """ form 表单中只有 username 和 password 参数"""
    def _deco(payload):
        try:
            # github 项目名称、镜像构建的名称、dockerfile路径、dockerfile文件名、是否自动构建(push)
            repo_name = request.form.get('repo_name', '').decode('utf-8').encode('utf-8')
            repo_branch = request.form.get('repo_branch', '').decode('utf-8').encode('utf-8')
            images_name = request.form.get('images_name', '').decode('utf-8').encode('utf-8')
            image_tag = request.form.get('image_tag', '').decode('utf-8').encode('utf-8')  # 镜像标签
            dockerfile_path = request.form.get('dockerfile_path', '').decode('utf-8').encode('utf-8')
            dockerfile_name = request.form.get('dockerfile_name', '').decode('utf-8').encode('utf-8')
            auto_build = request.form.get('auto_build', '').decode('utf-8').encode('utf-8')
        except Exception as msg:
            retdict = request_result(601, ret={'msg': msg.message})
            return retdict

        # 传入的参数有问题
        if (repo_name and repo_branch and images_name and image_tag
            and dockerfile_path and dockerfile_name and auto_build) is '':
            retdict = request_result(706)
            return retdict

        if (str(auto_build) == '0' or str(auto_build) == '1') is False:
            retdict = request_result(706)
            return retdict

        return func(payload=payload, repo_name=repo_name, repo_branch=repo_branch, image_tag=image_tag,
                    images_name=images_name, dockerfile_path=dockerfile_path,
                    dockerfile_name=dockerfile_name, auto_build=auto_build)
    return _deco





def image_repository_is_exist(image_repository):
    """ 验证镜像仓库是否存在; 存在 True; 不存在 False; """

    image_repo = g.db_session.query(ImageRepository).filter(ImageRepository.repository == image_repository).first()
    if image_repo is not None:
        return True
    return False


def request_image_project(func):
    def _deco():
        try:
            data = request.data
            data_json = json.loads(data)
        except Exception as msg:
            return request_result(710, ret=msg.message)

        return func()

    return _deco
