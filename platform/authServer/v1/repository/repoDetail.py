#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/12/1 09:59
"""

import json
from flask import g, jsonify, request
from flask_restful import Resource

from authServer.models.hub_db_meta import ImageRepository, RepositoryEvents

from authServer.common.decorate import check_headers, get_userinfo_by_payload
from authServer.pyTools.tools.codeString import request_result

@check_headers
@get_userinfo_by_payload
def modifyRepoDetail(kwargs={}):
    try:
        data = request.data
        data_json = json.loads(data)
    except Exception as msg:
        return request_result(710, ret=msg.message)

    # ['short_description', 'detail']



    if 'is_public' == kwargs['detail_type']:
        try:
            detail = data_json.get('detail', '').decode('utf-8').encode('utf-8')
            if (str(detail) == '1' or str(detail) == '0') is False:
                return request_result(706, ret='is_public is 0 or 1')
        except Exception as msg:
            return request_result(706, ret='is_public encode is error')

    else:
        detail = data_json.get('detail', '')  # .decode('utf-8').encode('utf-8')


    try:
        # 不可以修改他人的镜像详情

        image_repo = g.db_session.query(ImageRepository).filter(ImageRepository.uuid == kwargs['repoid']).first()

        if image_repo is None:
            return request_result(809, ret="image no have")

        # 使用组织id 20170106
        # if image_repo.uid != kwargs['uid']:
        if image_repo.uid != kwargs['orga_uuid']:
            return request_result(806)

        g.db_session.query(ImageRepository).filter(
            # 使用组织id 20170106
            # ImageRepository.uid == kwargs['uid'], ImageRepository.uuid == kwargs['repoid']).update(
            ImageRepository.uid == kwargs['orga_uuid'], ImageRepository.uuid == kwargs['repoid']).update(
            {kwargs['detail_type']: detail}
        )
        g.db_session.commit()
        return request_result(0)
    except Exception as msg:
        return request_result(403, ret=msg.message)



# 等到一个镜像的详情
@check_headers
@get_userinfo_by_payload
def GetRepoDetail(kwargs={}):


    image_repo = g.db_session.query(ImageRepository).filter(
        ImageRepository.uuid == str(kwargs['repoid']),
        #ImageRepository.uid == str(uid),
        ImageRepository.deleted == 0).first()

    if image_repo is None:
        return request_result(809, ret="Resources does not exist or has been deleted")

    # 使用组织id 20170106
    # if image_repo.uid != kwargs['uid'] and str(image_repo.is_public) != '1':
    if image_repo.uid != kwargs['orga_uuid'] and str(image_repo.is_public) != '1':
        print 'GetRepoDetail'
        print image_repo.uid
        print image_repo.is_public
        print type(image_repo.is_public)
        return request_result(806, ret='Resources not is public or ower')

    ret_d = dict()
    ret_d['repository'] = image_repo.repository
    ret_d['creation_time'] = image_repo.creation_time
    ret_d['update_time'] = image_repo.update_time
    ret_d['is_public'] = image_repo.is_public
    ret_d['short_description'] = image_repo.short_description
    ret_d['detail'] = image_repo.detail
    ret_d['download_num'] = image_repo.download_num
    ret_d['enshrine_num'] = image_repo.enshrine_num
    ret_d['review_num'] = image_repo.review_num
    ret_d['pushed'] = image_repo.pushed
    ret_d['is_code'] = image_repo.is_code
    ret_d['logo'] = image_repo.logo

    # 图片
    from authServer.conf.conf import OssHost
    if image_repo.logo == '' or image_repo.logo is None:
        ret_d['logo'] = OssHost + '/' + 'repository/default.png'
    else:
        ret_d['logo'] = OssHost + '/' + image_repo.logo

    ret_d['download_num'] = image_repo.download_num  # 下载次数


    repo_event = g.db_session.query(RepositoryEvents).filter(RepositoryEvents.repository == image_repo.repository).all()

    repo_tags = list()
    for repo_event_node in repo_event:
        tag_temp = dict()
        tag_temp['url'] = repo_event_node.url
        tag_temp['length'] = repo_event_node.length
        tag_temp['tag'] = repo_event_node.tag
        tag_temp['actor'] = repo_event_node.actor
        tag_temp['action'] = repo_event_node.action
        tag_temp['digest'] = repo_event_node.digest

        tag_temp['repo_id'] = repo_event_node.repo_id

        tag_temp['creation_time'] = repo_event_node.creation_time
        tag_temp['update_time'] = repo_event_node.update_time
        repo_tags.append(tag_temp)

    ret_d['tags'] = repo_tags

    return request_result(0, ret=ret_d)



@check_headers
@get_userinfo_by_payload

def delRepo(kwargs={}): # 删除镜像
    print 'ss'
    try:
        image_repo = g.db_session.query(ImageRepository).filter(ImageRepository.uuid == kwargs['repoid']).first()

        if image_repo is None:
            return request_result(809, ret="image no have")

        # if image_repo.uid != kwargs['uid']:
        if image_repo.uid != kwargs['orga_uuid']:
            return request_result(806)

        g.db_session.query(ImageRepository).filter(ImageRepository.uuid == kwargs['repoid'],
                                                   # ImageRepository.uid == kwargs['uid']
                                                   ImageRepository.uid == kwargs['orga_uuid']
                                                   ).update({"deleted": '1'})
        g.db_session.commit()
    except Exception as msg:
        return request_result(403, ret=msg.message)

    return request_result(0)

class RepoDetail(Resource):

    def put(self, repoid, detail_type):
        """
        @apiGroup Repository
        @apiDescription       修改镜像详情
        @apiVersion 1.0.0
        @apiHeader {String} token 请求借口的token
        @api {put} /api/v1.0/repository/repos/<string:repoid>/detail/<string:detail_type> 修改镜像详情
        @apiExample {put} Example usage:
            data = {
                "detail": "ubuntu office images",
            }

            headers = {
                'token': token,
                'content-type': "application/json",
            }

        @apiParam {String} repoid  镜像id
        @apiParam {String} detail  详细描述 或 简单描述
        @apiParam {String} detail_type    short_description:简单介绍, detail:详细描述,

        """
        d = dict()
        d['repoid'] = repoid
        detail_type = detail_type.decode('utf-8').encode('utf-8')

        # is public 20170113
        Type = ['short_description', 'detail', 'is_public']

        print type(detail_type)
        if detail_type not in Type:
            return jsonify(request_result(706, ret='detail_type is short_description or detail'))

        d['detail_type'] = detail_type
        return jsonify(modifyRepoDetail(kwargs=d))

    def get(self, repoid):
        """
        @apiGroup Repository
        @apiDescription       获取一个镜像详情
        @apiVersion 1.0.0
        @apiHeader {String} token 请求token
        @api {get} /api/v1.0/repository/repos/<string:repoid>/detail 获取一个镜像详情


        @apiParam {String} repoid  镜像id
        @apiParam {String} detail_type   detail:详细描述,

        """
        d = dict()
        d['repoid'] = repoid

        return jsonify(GetRepoDetail(kwargs=d))


    def delete(self, repoid):  # 删除镜像
        d = dict()
        d['repoid'] = repoid.decode('utf-8').encode('utf-8')

        return jsonify(delRepo(kwargs=d))
