#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/11/10 17:00
"""


from flask import Response, jsonify, g
from flask_restful import Resource
import authServer.conf.openOauth as openOauth

from authServer.pyTools.tools.codeString import request_result
from authServer.common.decorate import check_headers, get_userinfo_by_payload

from authServer.conf.openOauth import OAUTH_WEBHOOKS

from authServer.models.hub_db_meta import GitHubOauth, CodeRepo, ImageRepositoryBuild, ImageRepository


@check_headers
@get_userinfo_by_payload
def DelOauth(kwargs):
    """
    1. github_oauth 得到 access_token 等信息
    2. code_repo 得到 repo
    3. image_repository_build    repo_id
    :param kwargs:
    :return:
    """

    if kwargs['user_uuid_arg'] != kwargs['uid']:
        return request_result(806)


    # 获取该用户,对应平台下的所有代码项目
    codeRepos = g.db_session.query(CodeRepo).filter(
        CodeRepo.uid == kwargs['user_uuid_arg'], CodeRepo.src_type == kwargs['src_type_arg']).all()

    # 删除关联代码自动构建项目的配置信息  ImageRepositoryBuild
    for code_repo in codeRepos:
        print code_repo.repo_id
        image_build = ImageRepositoryBuild(code_repo_id=code_repo.repo_id)
        g.db_session.query(ImageRepositoryBuild).filter(ImageRepositoryBuild.code_repo_id == code_repo.repo_id).delete()
        g.db_session.commit()

    # 删除所有代码记录
    g.db_session.query(CodeRepo).filter(CodeRepo.uid == kwargs['user_uuid_arg'], CodeRepo.src_type == kwargs['src_type_arg']).delete()
    g.db_session.commit()


    # 标记所有与该平台相关的镜像全部是  非自动构建项目
    g.db_session.query(ImageRepository).filter(
        ImageRepository.uid == kwargs['user_uuid_arg'], ImageRepository.src_type == kwargs['src_type_arg']
    ).update({'src_type': '', 'is_code': '0'})
    g.db_session.commit()


    # 删除webhook记录; 遍历
    oauth = g.db_session.query(GitHubOauth).filter(GitHubOauth.uid == kwargs['user_uuid_arg'],
                                                   GitHubOauth.src_type == kwargs['src_type_arg']).first()

    # 该步骤;需要单独开启一个进程处理; 时间比较长
    if oauth is not None:
        if 'github' == kwargs['src_type_arg']:

            from authServer.common.oauthclient.HubApi import DelGithubAllWebHooks

            DelGithubAllWebHooks(username=oauth.git_name, token=oauth.access_token, del_hooks_url=OAUTH_WEBHOOKS)
            print 'githu'
        elif 'coding' == kwargs['src_type_arg']:
            from authServer.common.oauthclient.CodingApi import DellAllWebHooks

            DellAllWebHooks(user_name=oauth.git_name, access_token=oauth.access_token, hook_url_del=OAUTH_WEBHOOKS)

    # 删除授权记录
    g.db_session.query(GitHubOauth).filter(GitHubOauth.uid == kwargs['user_uuid_arg'],
                                           GitHubOauth.src_type == kwargs['src_type_arg']).delete()
    g.db_session.commit()

    return request_result(0)



class Oauth(Resource):
    def put(self, src_type, user_uuid):
        """
        @apiGroup  Oauth
        @apiDescription   解除绑定
        @apiVersion 1.0.0

        @api {put} /api/v2.0/oauths/oauth/<string:src_type>/<string:user_uuid> 解除第三方绑定

        @apiHeader {String} token  请求接口的token,放在请求头中

        @apiParam {String} src_type   代码源类型;github or coding
        @apiParam {String} user_uuid  用户uuid
        """

        if src_type not in openOauth.OpenType:
            return jsonify(request_result(706, ret='src_type is error'))

        k = dict()
        k['src_type_arg'] = src_type
        k['user_uuid_arg'] = user_uuid

        return jsonify(DelOauth(kwargs=k))