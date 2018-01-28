#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/10/25 16:28
"""


from flask import g

from authServer.models.hub_db_meta import ImageRepository, GitHubOauth, ImageRepositoryBuild, CodeRepo,UserBase
from authServer.pyTools.tools.codeString import request_result


# 获取代码构建项目
def get_repository_build(user_name, uid):
    """
    获取用户 代码 自动构建项目
    """
    image_repo = g.db_session.query(ImageRepository).filter(
        ImageRepository.uid == str(uid), ImageRepository.deleted == '0', ImageRepository.is_code == '1').all()

    if image_repo is None:
        return request_result(0)

    retmsg = list()
    for image_repo_node in image_repo:
        tep_d = dict()
        tep_d['uuid'] = image_repo_node.uuid  # 镜像uuid
        tep_d['repository'] = image_repo_node.repository  # 镜像名 boxlinker/xxx
        tep_d['uid'] = image_repo_node.uid  # 用户id
        tep_d['creation_time'] = image_repo_node.creation_time
        tep_d['update_time'] = image_repo_node.update_time
        tep_d['is_public'] = image_repo_node.is_public
        tep_d['short_description'] = image_repo_node.short_description
        tep_d['detail'] = image_repo_node.detail
        tep_d['download_num'] = image_repo_node.download_num
        tep_d['enshrine_num'] = image_repo_node.enshrine_num
        tep_d['review_num'] = image_repo_node.review_num
        tep_d['version'] = image_repo_node.version
        tep_d['latest_version'] = image_repo_node.latest_version
        tep_d['pushed'] = image_repo_node.pushed

        try:
            image_repo_build = g.db_session.query(ImageRepositoryBuild).filter(
                ImageRepositoryBuild.image_repository_id == image_repo_node.uuid).first()

            if image_repo_build is None:
                continue
        except Exception as msg:
            continue

            # GitHubOauth
        try:
            git_oauth = g.db_session.query(GitHubOauth).filter(GitHubOauth.uid == str(uid)).first()

            code_repo = g.db_session.query(CodeRepo).filter(CodeRepo.id == image_repo_build.code_repo_id).first()
        except Exception as msg:
            return request_result(405, ret=msg.message)

        # git@github.com:cabernety/boxlinker.git
        # git@github.com:liuzhangpei/webhook_test.git
        if git_oauth is None or code_repo is None:
            tep_d['src_url'] = 'git' + git_oauth
        else:
            tep_d['src_url'] = 'git@github.com:' + git_oauth.git_name + '/' + code_repo.repo_name + '.git'

        tep_d['repo_branch'] = image_repo_build.repo_branch
        tep_d['code_repo_id'] = image_repo_build.code_repo_id  # 关联代码id
        tep_d['images_name'] = image_repo_node.repository
        tep_d['dockerfile_path'] = image_repo_build.dockerfile_path
        tep_d['dockerfile_name'] = image_repo_build.dockerfile_name
        tep_d['auto_build'] = image_repo_build.auto_build
        tep_d['image_tag'] = image_repo_build.image_tag
        tep_d['build_status'] = image_repo_build.build_status # 构建状态 1:构建成功, 2:构建构建中,  3:构建失败  0: 还未构建
        tep_d['use_time'] = image_repo_build.use_time
        tep_d['last_build'] = image_repo_build.last_build
        retmsg.append(tep_d)

    return request_result(0, ret=retmsg)