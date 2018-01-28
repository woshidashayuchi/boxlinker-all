#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/8/30 2:20
@镜像库操作接口
"""

import json
import time

from flask import jsonify, request, g

from flask_restful import Resource

from authServer.models.hub_db_meta import AccessToken, Session
from authServer.conf.conf import GLOBALS_TOKEN
from authServer.pyTools.token.token import get_payload
from authServer.pyTools.tools.codeString import request_result

from authServer.registry.image_repository import delete_image_project, list_image_project, modify_image_project



def check_token_ret_bool(func):
    """ 校验token """
    def _deco(tokenid, token):
        if tokenid in GLOBALS_TOKEN and GLOBALS_TOKEN[tokenid] == token:  # 此时系统token符合
            return func(token)

        if tokenid not in GLOBALS_TOKEN:
            ret = g.db_session.query(AccessToken).filter(AccessToken.token_uuid == tokenid, AccessToken.deleted=='0').first()
            if ret is not None and ret.token == token:
                return func(token)
        return False
    return _deco

def get_uid_by_token(func):
    """ 通过token取得token中的uid, 传入下一个函数 """
    def _deco(token):
        ret = get_payload(token=token)
        if ret['status'] != 0:
            return request_result(102)

        payload = ret['result']['payload']
        uid = json.loads(payload)['uid']
        user_name = json.loads(payload)['user_name']
        return func(uid=uid, user_name=user_name)
    return _deco



class ImageRepositoryHandle(Resource):
    def post(self):
        """
        @apiDescription 创建镜像仓库项目
        @apiVersion 1.0.0
        @apiHeader {String} token 请求借口的token
        @api {post} /registry/image_repository
        @apiExample {post} Example usage:
        post http://auth.boxlinker.com/registry/image_repository

            新建(镜像仓库,不是代码自动构建项目)
            urltag = url + '/registry/image_repository'
            data = {
                "is_public": "1",
                "detail": "ubuntu office images",
                "repository": "ubuntu",
                "short_description": "sdsds",
                "is_code": "0"
            }

            新建(镜像仓库,代码自动构建项目)
            {
                "is_public": "1",
                "detail": "ubuntu office images",
                "repository": "1545431",
                "short_description": "sdsdes",
                "is_code": "1",

                "repo_name": "webhook_test",
                "repo_branch": "master",
                "image_tag": "last",
                "dockerfile_path": "/docker",
                "dockerfile_name": "Dockerfile",
                "auto_build": "1",
                "src_type": "coding"  # github、coding
            }

        @apiParam {String} is_public  公有还是私有
        @apiParam {String} short_description  简单描述
        @apiParam {String} detail  详细描述
        @apiParam {String} repository  镜像名   ubuntu 验证 repository 是否存在
        @apiParam {String} is_code  是否是代码构建项目

        @apiParam {String} repo_name  代码项目名
        @apiParam {String} repo_branch  代码分支
        @apiParam {String} image_tag  镜像标签
        @apiParam {String} dockerfile_path  dockerfile 路径
        @apiParam {String} dockerfile_name  dockerfile 文件名
        @apiParam {String} auto_build  是否自动构建(代码更新时,收到web hook通知后自动构建)
        @apiParam {String} src_type    代码源类型, github, coding
        """
        from authServer.registry.image_repository import ImageRepositoryCreate
        return jsonify(ImageRepositoryCreate(kwargs={}))

    def delete(self):
        """
        @apiDescription 删除镜像
        @apiVersion 1.0.0
        @apiHeader {String} token 请求接口的token,放在请求头中
        @api {delete} /registry/image_repository?imagename=boxlinker/sdsds
        @apiParam {String} imagename 镜像名
        """
        return jsonify(delete_image_project())


    def get(self):
        """
        @apiDescription 获取镜像库列表
        @apiVersion 1.0.0
        @apiHeader {String} token 请求接口的token,放在请求头中
        @api {get} /registry/image_repository
        @apiExample {get} Example usage:
        get /registry/image_repository?is_public=true  获取平台镜像
        get /registry/image_repository              获取用户自己镜像

        get /registry/image_repository?is_code=true 获取自动构建项目列表
        --> 原始地址: /oauth/githubbuild return jsonify(get_github_build())


        get /registry/image_repository?only=true&repository_id=151d5b0d-146e-3f6b-9283-f4cec260dbd4 单独获取某个镜像的详情
        --> 原始地址: /v2/tags

        @apiSuccessExample {json} Success-Response:
            {
              "msg": "OK",
              "result": [
                {
                  "auto_build": "1",
                  "creation_time": "Sun, 09 Oct 2016 14:24:26 GMT",
                  "detail": "detail... ...",
                  "is_public": "0",
                  "repositories": "boxlinker/rererer",
                  "short_description": "jian dan miao shu",
                  "type": "1",
                  "update_time": "Sun, 09 Oct 2016 14:24:26 GMT"
                }
                ... ... ... ...
              ],
              "status": 0
            }
            auto_build: 有代码自动构建的镜像存在此字段;创建的镜像项目不存在该字段
            type: 0-->手动推送;   1-->代码构建
        """
        return jsonify(list_image_project())

    def put(self):
        """
        @apiDescription put 修改镜像详情
        @apiVersion 1.0.0
        @apiHeader {String} token 请求借口的token
        @api {put} /registry/create
        @apiExample {post} Example usage:
        post http://auth.boxlinker.com/registry/create

            urltag = url + '/registry/create'
            data = {
                "is_public": "1",
                "detail": "ubuntu office images",
                "name": "ubuntu",
                "repositories": "boxlinker/ubuntu",
                "uuid": "02920191-3663-367d-8df1-79479f931f46"
            }

            headers = {
                'token': token,
                'content-type': "application/json",
            }
            response = requests.request('PUT', url=urltag, data=json.dumps(data), headers=headers)
            return response.text.decode('utf-8').encode('utf-8')


        @apiParam {String} uuid  镜像id
        @apiParam {String} is_public  公有还是私有
        @apiParam {String} short_description  简单描述
        @apiParam {String} detail  详细描述
        @apiParam {String} repositories  镜像名   boxlinker/ubuntu 验证 repositories 是否存在
        """
        return jsonify(modify_image_project())