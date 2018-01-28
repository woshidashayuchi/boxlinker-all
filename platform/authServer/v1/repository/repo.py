#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/11/29 10:03
"""


from flask import g, jsonify, request
from flask_restful import Resource

from authServer.models.hub_db_meta import ImageRepository

from authServer.common.decorate import check_headers, get_userinfo_by_payload
from authServer.pyTools.tools.codeString import request_result

from authServer.conf.conf import OssHost


@check_headers
@get_userinfo_by_payload
def repoFuzzy(kwargs):
    from sqlalchemy import or_
    repovalue = '%' + kwargs['repo_fuzzy'] + '%'

    offset = (kwargs['page'] - 1) * kwargs['page_size']
    limit = kwargs['page_size']

    if offset < 0 or limit <= 0:
        return request_result(706, "page or page_size is error")

    try:

        count = g.db_session.query(ImageRepository).filter(
            or_(ImageRepository.repository.like(repovalue),
                ImageRepository.short_description.like(repovalue),
                ImageRepository.detail.like(repovalue)
                ), ImageRepository.is_public == '1', ImageRepository.deleted == '0'
        ).count()

        print "dfdfsfd"
        print count
        print "count"

        image_repo = g.db_session.query(ImageRepository).filter(
            or_(ImageRepository.repository.like(repovalue),
                ImageRepository.short_description.like(repovalue),
                ImageRepository.detail.like(repovalue)
                ), ImageRepository.is_public == '1', ImageRepository.deleted == '0'
        ).offset(offset).limit(limit)
    except Exception as msg:
        return request_result(404, ret=msg.message)

    return retImageRepo(page=kwargs['page'], page_size=kwargs['page_size'], count=count, repolist=image_repo)



RepoImageResult = {
    'count': None,
    "page": None,
    "page_size": None,
    "result": None,
    'current_size': None
}



def retImageRepo(page, page_size, count, repolist):
    global RepoImageResult
    RepoImageResult['page'] = page
    RepoImageResult['page_size'] = page_size
    RepoImageResult['count'] = count

    retlist = list()
    current_size = 0
    for image_project_node in repolist:
        temp_d = dict()
        temp_d['uuid'] = image_project_node.uuid
        temp_d['repository'] = image_project_node.repository
        temp_d['creation_time'] = image_project_node.creation_time
        temp_d['update_time'] = image_project_node.update_time
        temp_d['is_public'] = image_project_node.is_public
        temp_d['short_description'] = image_project_node.short_description  # 简单描述
        temp_d['detail'] = image_project_node.detail  # #  # 详细描述
        # temp_d['auto_build'] = image_project_node.auto_build  # 是否自动构建
        temp_d['type'] = image_project_node.is_code  # 0-->手动推送;   1-->代码构建
        temp_d['download_num'] = image_project_node.download_num  # 下载次数

        # 图片
        if image_project_node.logo == '' or image_project_node.logo is None:
            temp_d['logo'] = OssHost + '/' + 'repository/default.png'
        else:
            temp_d['logo'] = OssHost + '/' + image_project_node.logo


        retlist.append(temp_d)
        current_size += 1

    RepoImageResult['current_size'] = current_size

    RepoImageResult['result'] = retlist

    return request_result(0, ret=RepoImageResult)

@check_headers
@get_userinfo_by_payload
def publicImage(kwargs):  # 平台公开镜像
    try:
        offset = (kwargs['page'] - 1) * kwargs['page_size']
        limit = kwargs['page_size']

        if offset < 0 or limit <= 0:
            return request_result(706, "page or page_size is error")

        from sqlalchemy import func
        count = g.db_session.query(ImageRepository).filter(
            ImageRepository.deleted == '0',
            ImageRepository.is_public == '1'
        ).count()

        print "dfdfsfd"
        print count
        print "count"

        image_repo = g.db_session.query(ImageRepository).filter(
                ImageRepository.deleted == '0',
                ImageRepository.is_public == '1').offset(offset).limit(limit)
    except Exception as msg:
        print msg.message
        return request_result(404, ret=msg.message)

    return retImageRepo(page=kwargs['page'], page_size=kwargs['page_size'], count=count, repolist=image_repo)



class RepoFuzzy(Resource):
    def get(self, page, page_size):
        """
        @apiGroup Repository
        @apiDescription       镜像搜索
        @apiVersion 1.0.0
        @apiHeader {String} token 请求接口的token,放在请求头中
        @api {get} /api/v1.0/repository/repos/<int:page>/<int:page_size>/?repo_fuzzy=library%2Fnginx   平台镜像; 镜像搜索


        @apiParamExample {json} Request-Param-Example:
            {
                "msg": "OK",
                "result":
                {
                    "count": 2,         # 符合要求的数据总数
                    "current_size": 1,  # 当前页返回的数据量; 每页请求的数据条数(实际数据,已返回为准)
                    "page": 1,
                    "page_size": 10,
                    "result":
                    [
                        {
                            "creation_time": "Tue, 29 Nov 2016 05:18:30 GMT",
                            "detail": "Push the mirror between terminals",
                            "download_num": 172,
                            "is_public": 1,
                            "repository": "cabernety/chat-demo",
                            "short_description": "Push the mirror between terminals",
                            "type": 0,
                            "update_time": "Tue, 29 Nov 2016 05:18:30 GMT",
                            "uuid": "1359447b-3327-3a69-bec0-cdf7d4f6c6df"
                        }
                    ]
                },
                "status": 0
            }
            成功时,result搜索到的镜像列表
            @apiParam {int} page           分页数据的第几页(从1开始)
            @apiParam {int} page_size      每页请求的数据条数(实际数据,已返回为准)

            @apiParam {String} repo_fuzzy  搜索信息;如果为空则获取平台镜像
        """

        k = dict()

        k['page'] = page
        k['page_size'] = page_size

        repo_fuzzy = request.args.get('repo_fuzzy')

        print repo_fuzzy
        print 'repo_fuzzy'

        if repo_fuzzy is None:  # 平台镜像
            return jsonify(publicImage(kwargs=k))
        k['repo_fuzzy'] = repo_fuzzy

        return jsonify(repoFuzzy(kwargs=k))

@check_headers
@get_userinfo_by_payload
def downloadRepo(kwargs):
    from sqlalchemy import desc
    Image_repo = g.db_session.query(ImageRepository).filter(
        ImageRepository.is_public == '1', ImageRepository.deleted == '0').order_by(
        desc(ImageRepository.download_num)).limit(20)

    repo_list = list()
    for ImageBase in Image_repo:
        ImageNode = dict()
        ImageNode['uuid'] = ImageBase.uuid
        ImageNode['uid'] = ImageBase.uid
        ImageNode['repository'] = ImageBase.repository
        ImageNode['creation_time'] = ImageBase.creation_time
        ImageNode['update_time'] = ImageBase.update_time
        ImageNode['is_public'] = ImageBase.is_public
        ImageNode['short_description'] = ImageBase.short_description
        ImageNode['detail'] = ImageBase.detail
        ImageNode['download_num'] = ImageBase.download_num
        ImageNode['is_code'] = ImageBase.is_code
        ImageNode['src_type'] = ImageBase.src_type

        # 图片
        if ImageBase.logo == '' or ImageBase.logo is None:
            ImageNode['logo'] = OssHost + '/' + 'repository/default.png'
        else:
            ImageNode['logo'] = OssHost + '/' + ImageBase.logo
        repo_list.append(ImageNode)


    return request_result(0, ret=repo_list)

class DownloadRepo(Resource):
    def get(self):
        """
        @apiGroup Repository
        @apiDescription       推荐镜像
        @apiVersion 1.0.0
        @apiHeader {String} token 请求接口的token,放在请求头中
        @api {get} /api/v1.0/repository/repos/ranks   推荐镜像(按下载次数排名)

        @apiParamExample {json} Request-Param-Example:
            {
                "msg": "OK",
                "result": [
                    {
                        "creation_time": "Tue, 29 Nov 2016 05:18:30 GMT",
                        "detail": "Push the mirror between terminals",
                        "download_num": 5,
                        "is_code": 0,
                        "is_public": 1,
                        "repository": "cabernety/chat-demo",
                        "short_description": "Push the mirror between terminals",
                        "src_type": null,
                        "uid": "8a9feb9e-9e4d-37a6-b4a5-93d00ef35900",
                        "update_time": "Tue, 29 Nov 2016 05:18:30 GMT",
                        "uuid": "1359447b-3327-3a69-bec0-cdf7d4f6c6df"
                    }
                    ... ...
                ],
                "status": 0
            }
            成功时,result返回用户推荐镜像列表
        """

        return jsonify(downloadRepo(kwargs={}))




@check_headers
@get_userinfo_by_payload
def myselfImage(kwargs):  # 平台公开镜像
    try:
        offset = (kwargs['page'] - 1) * kwargs['page_size']
        limit = kwargs['page_size']

        if offset < 0 or limit <= 0:
            return request_result(706, "page or page_size is error")

        from sqlalchemy import func
        count = g.db_session.query(ImageRepository).filter(
            ImageRepository.deleted == '0',
            ImageRepository.uid == kwargs['orga_uuid']
        ).count()


        image_repo = g.db_session.query(ImageRepository).filter(
            ImageRepository.deleted == '0',
            ImageRepository.uid == kwargs['orga_uuid']).offset(offset).limit(limit)  # 组织id区分镜像
            # ImageRepository.uid == kwargs['uid']).offset(offset).limit(limit)
    except Exception as msg:
        print msg.message
        return request_result(404, ret=msg.message)

    return retImageRepo(page=kwargs['page'], page_size=kwargs['page_size'], count=count, repolist=image_repo)



@check_headers
@get_userinfo_by_payload
def myselfImageFuzzy(kwargs):  # 我的镜像搜索
    from sqlalchemy import or_
    repovalue = '%' + kwargs['repo_fuzzy'] + '%'

    offset = (kwargs['page'] - 1) * kwargs['page_size']
    limit = kwargs['page_size']

    if offset < 0 or limit <= 0:
        return request_result(706, "page or page_size is error")

    try:

        count = g.db_session.query(ImageRepository).filter(
            or_(ImageRepository.repository.like(repovalue),
                ImageRepository.short_description.like(repovalue),
                ImageRepository.detail.like(repovalue)
                ), ImageRepository.deleted == '0', ImageRepository.uid == kwargs['orga_uuid']
                # ), ImageRepository.deleted == '0', ImageRepository.uid == kwargs['uid']
        ).count()

        image_repo = g.db_session.query(ImageRepository).filter(
            or_(ImageRepository.repository.like(repovalue),
                ImageRepository.short_description.like(repovalue),
                ImageRepository.detail.like(repovalue)
                ), ImageRepository.deleted == '0', ImageRepository.uid == kwargs['orga_uuid']
                # ), ImageRepository.deleted == '0', ImageRepository.uid == kwargs['uid']
        ).offset(offset).limit(limit)
    except Exception as msg:
        return request_result(404, ret=msg.message)

    return retImageRepo(page=kwargs['page'], page_size=kwargs['page_size'], count=count, repolist=image_repo)




class OwnRepo(Resource):
    def get(self, page, page_size):
        """
        @apiGroup Repository
        @apiDescription       我的镜像
        @apiVersion 1.0.0
        @apiHeader {String} token 请求接口的token,放在请求头中
        @api {get} /api/v1.0/repository/user/repos/<int:page>/<int:page_size>   我的镜像


        @apiParamExample {json} Request-Param-Example:
            {
                "msg": "OK",
                "result":
                {
                    "count": 2,         # 符合要求的数据总数
                    "current_size": 1,  # 当前页返回的数据量; 每页请求的数据条数(实际数据,已返回为准)
                    "page": 1,
                    "page_size": 10,
                    "result":
                    [
                        {
                            "creation_time": "Tue, 29 Nov 2016 05:18:30 GMT",
                            "detail": "Push the mirror between terminals",
                            "download_num": 172,
                            "is_public": 1,
                            "repository": "cabernety/chat-demo",
                            "short_description": "Push the mirror between terminals",
                            "type": 0,
                            "update_time": "Tue, 29 Nov 2016 05:18:30 GMT",
                            "uuid": "1359447b-3327-3a69-bec0-cdf7d4f6c6df"
                        }
                    ]
                },
                "status": 0
            }
            成功时,result搜索到的镜像列表
            @apiParam {int} page           分页数据的第几页(从1开始)
            @apiParam {int} page_size      每页请求的数据条数(实际数据,已返回为准)
        """

        k = dict()

        k['page'] = page
        k['page_size'] = page_size

        repo_fuzzy = request.args.get('repo_fuzzy')

        if repo_fuzzy is None:
            return jsonify(myselfImage(kwargs=k))  # 我的镜像

        k['repo_fuzzy'] = repo_fuzzy

        return jsonify(myselfImageFuzzy(kwargs=k))