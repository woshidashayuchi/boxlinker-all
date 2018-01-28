#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/9/12 下午1:57
"""

import json

from flask import g

from authServer.code_build.common.rabbitmq_client import RabbitmqClient
from authServer.conf.conf import queue_name, exchange_name
from authServer.models.hub_db_meta import GitHubOauth, UserBase, CodeRepo, ImageRepository, ImageRepositoryBuild
from authServer.pyTools.tools.codeString import request_result

class Send_Build_Msg(object):

    def __init__(self):
        self.rmq_client = RabbitmqClient()
        self.queue_name = queue_name
        self.exchange_name = exchange_name
        self.timeout = 60

    def send_msg(self, dict_data):
        try:
            json_data = json.dumps(dict_data)
            # ret = self.rmq_client.rpc_cast_client(self.queue_name, json_data)
            ret = self.rmq_client.broadcast_client(self.exchange_name, json_data)  # 广播
            print ret
            return ret
        except Exception, e:
            print 'sssssss'
            print e.message
            print e.args
            return request_result(598)


def github_Webhooks(repo_id):
    """
    :param repo_id: github  repo id
    """
    try:
        code_repo = g.db_session.query(CodeRepo).filter(CodeRepo.repo_id == str(repo_id),
                                                        CodeRepo.src_type == 'github').first()
        if code_repo is None:
            return request_result(405)
    except Exception as msg:
        print 'github_Webhooks g.db_session.query(GitHubRepo) is error'
        return request_result(404, ret=msg.message)

    try:
        image_repo_build = g.db_session.query(ImageRepositoryBuild).filter(ImageRepositoryBuild.code_repo_id == code_repo.id).all()
        if image_repo_build is None:
            return request_result(405)
    except Exception as msg:
        print 'g.db_session.query(build_image) is error'
        return request_result(404, ret=msg.message)

    for image_repo_build_node in image_repo_build:
        print "github_Webhooks --->build_image_node.id"
        print image_repo_build_node.image_repository_id
        send_build_rabbit_by_repouuid(image_repo_build_node.image_repository_id)
    return request_result(0)



def get_build_msg(func):
    """ 根据 build id  获取 BuildImage, 数据记录 """
    def _deco(build_id):
        try:

            ret = g.db_session.query(BuildImage).filter(BuildImage.id == str(build_id)).first()
        except Exception as msg:
            print 'get_build_msg g.db_session.query(GitHubRepo) is error'
            print msg.message
            return request_result(404, ret=msg.message)

        if ret is None:
            print 'no git repo'
            return request_result(405)

        print ''
        return func(ret)
    return _deco


@get_build_msg
def send_build_rabbit(build_image):  # 根据 BuildImage 项目id, 启动构建项目程序
    try:
        response_d = dict()
        try:
            ret = g.db_session.query(GitHubOauth).filter(GitHubOauth.uid == str(build_image.uid)).first()
        except Exception as msg:
            print 'send_build_rabbit g.db_session.query(GitHubRepo) is error'
            print msg.message
            return request_result(404, ret=msg.message)

        if ret is None:
            print 'no git repo'
            return request_result(405)

        response_d['git_name'] = ret.git_name   # github 用户名

        uid = ret.uid
        try:
            user_base_ret = g.db_session.query(UserBase).filter(UserBase.user_id == str(uid)).first()
        except Exception as msg:
            print 'g.db_session.query(UserBase) is error'
            print msg.message
            return request_result(404, ret=msg.message)

        if user_base_ret is None:
            print 'no git repo'
            return request_result(405)
        response_d['user_name'] = user_base_ret.username  # 系统平台name

        print 'user_base_ret.username ' + str(uid)
        print 'user_base_ret.username ' + user_base_ret.username

        try:
            code_repo_id = build_image.code_repo_id
            code_repo = g.db_session.query(CodeRepo).filter(CodeRepo.id == str(code_repo_id)).first()
            if code_repo is None:
                return request_result(405)
        except Exception as msg:
            print 'g.db_session.query(UserBase) is error'
            print msg.message
            return request_result(404, ret=msg.message)

        # 20160921
        response_d['id'] = build_image.id

        response_d['git_uid'] = code_repo.repo_uid
        response_d['repo_id'] = code_repo.repo_id
        response_d['repo_name'] = code_repo.repo_name
        response_d['repo_hook_token'] = code_repo.repo_hook_token  # web hooks token
        response_d['is_hook'] = code_repo.is_hook
        response_d['src_type'] = code_repo.src_type

        response_d['repo_branch'] = build_image.repo_branch
        response_d['images_name'] = build_image.images_name
        response_d['dockerfile_path'] = build_image.dockerfile_path
        response_d['dockerfile_name'] = build_image.dockerfile_name
        response_d['auto_build'] = build_image.auto_build
        response_d['image_tag'] = build_image.image_tag


        print 'response_d'
        print response_d

        sbm = Send_Build_Msg()
        sbm.send_msg(response_d)
        return request_result(0, ret=response_d)
    except Exception as msg:
        return request_result(602, ret=msg.message)


def send_build_rabbit_by_repouuid(image_repo_uuid):  # 根据 BuildImage 项目id, 启动构建项目程序
    response_d = dict()

    try:
        image_repo = g.db_session.query(ImageRepository).filter(ImageRepository.uuid == str(image_repo_uuid)).first()
    except Exception as msg:
        return request_result(404, ret=msg.message)

    if image_repo is None:  # 记录为空
        return request_result(405)

    if str(image_repo.is_code) != '1':
        return request_result(713)

    response_d['images_name'] = image_repo.repository

    # 代码构建配置信息
    try:
        image_repo_build = g.db_session.query(ImageRepositoryBuild).filter(
            ImageRepositoryBuild.image_repository_id == str(image_repo_uuid)).first()

        if image_repo_build is None:  # 记录为空
            return request_result(405)
    except Exception as msg:
        return request_result(404, ret=msg.message)

    response_d['repo_branch'] = image_repo_build.repo_branch  # 项目名,分支
    response_d['dockerfile_path'] = image_repo_build.dockerfile_path
    response_d['dockerfile_name'] = image_repo_build.dockerfile_name
    response_d['auto_build'] = image_repo_build.auto_build
    response_d['image_tag'] = image_repo_build.image_tag

    # 获取用户信息
    uid = image_repo.uid
    try:
        user_base_ret = g.db_session.query(UserBase).filter(UserBase.user_id == str(uid)).first()
    except Exception as msg:
        return request_result(404, ret=msg.message)

    if user_base_ret is None:
        return request_result(405)

    response_d['user_name'] = user_base_ret.username  # 系统平台name
    response_d['id'] = image_repo_uuid

    # 获取github 信息
    try:
        ret = g.db_session.query(GitHubOauth).filter(GitHubOauth.uid == str(uid)).first()
    except Exception as msg:
        print 'send_build_rabbit g.db_session.query(GitHubRepo) is error'
        print msg.message

    if ret is None:
        return request_result(405)

    response_d['git_name'] = ret.git_name  # github 用户名

    try:
        code_repo_id = image_repo_build.code_repo_id  # 关联代码id
        code_repo = g.db_session.query(CodeRepo).filter(CodeRepo.id == str(code_repo_id)).first()
        if code_repo is None:
            return request_result(405)
    except Exception as msg:
        print 'g.db_session.query(UserBase) is error'
        print msg.message
        return request_result(404, ret=msg.message)

    response_d['repo_name'] = code_repo.repo_name  # code项目名
    response_d['repo_hook_token'] = code_repo.repo_hook_token  # web hooks token
    response_d['is_hook'] = code_repo.is_hook
    response_d['src_type'] = code_repo.src_type
    response_d['git_uid'] = code_repo.repo_uid  # github 用户id
    response_d['repo_id'] = code_repo.repo_id  # 项目名,分支

    try:
        sbm = Send_Build_Msg()
        sbm.send_msg(response_d)
        return request_result(0, ret=response_d)
    except Exception as msg:
        return request_result(602, ret=msg.message)

