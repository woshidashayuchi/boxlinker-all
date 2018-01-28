#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/10/25 14:23
"""

import json
from flask import request, jsonify, g
from flask_restful import Resource

from authServer.common.decorate import check_headers, get_userinfo_by_payload
from authServer.pyTools.tools.codeString import request_result


from authServer.models.hub_db_meta import ImageRepository, CodeRepo, ImageRepositoryBuild, RepositoryEvents,UserBase



from authServer.conf.conf import Mask_Public


class RepositoryBuild(Resource):
    @staticmethod
    @check_headers
    @get_userinfo_by_payload
    def modify_repo_build(kwargs):
        try:
            data = request.data
            data_json = json.loads(data)
            dockerfile_path = data_json.get('dockerfile_path', '').decode('utf-8').encode('utf-8')
            repo_branch = data_json.get('repo_branch', '').decode('utf-8').encode('utf-8')
            auto_build = data_json.get('auto_build', '').decode('utf-8').encode('utf-8')
            if dockerfile_path == '' or repo_branch == '' or auto_build not in Mask_Public:
                return request_result(706)
        except Exception as msg:
            return request_result(710, ret=msg.message)

        try:
            image_repo = g.db_session.query(ImageRepository).filter(
                ImageRepository.uuid == kwargs['repository_uuid_arg'],
                ImageRepository.uid == kwargs['uid'],
                ImageRepository.deleted == '0',
                ImageRepository.is_code == '1'
            ).first()

            if image_repo is None:
                return request_result(809)

            g.db_session.query(ImageRepositoryBuild).filter(
                ImageRepositoryBuild.image_repository_id == kwargs['repository_uuid_arg']
            ).update(
                {"repo_branch": repo_branch, "dockerfile_path": dockerfile_path, "auto_build": auto_build}
            )
            g.db_session.commit()
            return request_result(0)
        except Exception as msg:
            return request_result(403, ret=msg.message)

    def put(self, repository_uuid):
        """
        @apiGroup RepositoryBuild
        @apiDescription 修改构建镜像,基本配置

        @apiHeader {String} token   请求接口的token,放在请求头中
        @api {put} /api/v1.0/repository/repositorybuilds/<string:repository_uuid>  修改构建镜像配置

        @apiExample {PUT} Example usage:
            {
                "dockerfile_path": "/dockder",
                "repo_branch": "develop",
                "auto_build": "1"
            }

        @apiParam {String} repository_uuid   镜像id
        @apiParam {String} dockerfile_path   Dockerfile位置
        @apiParam {String} repo_branch       默认代码分支
        @apiParam {String} auto_build        自动构建
        """

        k = dict()
        k['repository_uuid_arg'] = repository_uuid

        return jsonify(self.modify_repo_build(k))



class RepositoryBuildInstant(Resource):
    @staticmethod
    @check_headers
    @get_userinfo_by_payload  # 此时 varbox 里传入的是 自动构建数据库记录的 id
    def github_rightaway_build(kwargs):
        try:
            image_repo = g.db_session.query(ImageRepository).filter(
                ImageRepository.uuid == kwargs['repository_uuid_arg'],
                ImageRepository.uid == kwargs['uid']
            ).first()

            if image_repo is None:
                return request_result(809, "uid->.repository_uuid_arg != repository_uuid_arg")
        except Exception as msg:
            return request_result(404, ret=msg.message)

        from authServer.oauth.send_build_msg import send_build_rabbit_by_repouuid
        return send_build_rabbit_by_repouuid(kwargs['repository_uuid_arg'])

    def put(self, repository_uuid):
        """
        @apiGroup RepositoryBuild
        @apiDescription 立即构建镜像;代码构建

        @apiHeader {String} token   请求接口的token,放在请求头中
        @api {put} /api/v1.0/repository/repositorybuilds/<string:repository_uuid>  立即构建镜像

        @apiParam {String} repository_uuid   镜像id
        """
        k = dict()
        k['repository_uuid_arg'] = repository_uuid

        return jsonify(self.github_rightaway_build(k))



class MDIF(Resource):
    def get(self):

        image_repo = g.db_session.query(ImadgeRepository).filter(ImageRepository.uid == "").all()

        for irepo in image_repo:
            image = irepo.repository
            print image

            imagelist = image.split('/')
            if len(imagelist) != 2:  # 镜像地址不合法
                break


            repositoryname, imagename = imagelist  # 前缀  可能是   组织名
            print "repositoryname, imagename = imagelist"
            from authServer.tools.db_check import login_username, get_uuid_by_name, get_orgsuuid_by_name
            user_uuid = get_orgsuuid_by_name(username=repositoryname)
            print user_uuid

            g.db_session.query(ImageRepository).filter(ImageRepository.repository == image).update(
                {"uid": user_uuid})
            g.db_session.commit()


        return jsonify(request_result(0))