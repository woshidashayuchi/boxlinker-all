#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/12/2 14:09
"""

#
#
import json
from flask import g, jsonify, request
from flask_restful import Resource
#
from authServer.models.hub_db_meta import ImageRepository
#
# # from authServer.common.decorate import check_headers, get_userinfo_by_payload
from authServer.pyTools.tools.codeString import request_result


from authServer.common.image.image import setRepoLogo

def AutoSetLogo(repositoryname):
    try:
        print 'logo AutoSetLogo :' + repositoryname
        dd = setRepoLogo(repositoryname)

        if dd is False:
            return request_result(403)

        g.db_session.query(ImageRepository).filter(ImageRepository.repository == repositoryname).update(
            {'logo': dd}
        )
        g.db_session.commit()
        return request_result(0)
    except Exception as msg:
        return request_result(403)



class RepoLogo(Resource):
    def post(self, repoid):
        """ 是是是 """
        print repoid

        image_repo = g.db_session.query(ImageRepository).filter(ImageRepository.uuid == repoid).first()
        if image_repo is None:
            return request_result(809)

        if image_repo.logo == '' or image_repo.logo is None:  # 判断logo 是否为空
            print 'image_repo.logo == null'
            AutoSetLogo(repositoryname=image_repo.repository)
            return jsonify(AutoSetLogo(repositoryname=image_repo.repository))
        else:
            print 'logo image_repo.logo != null'
            print image_repo.logo
            return jsonify(request_result(0))

        # image_repo = g.db_session.query(ImageRepository).filter(ImageRepository.deleted == '0').all()
        #
        # for imageNode in image_repo:
        #     print imageNode.uuid
        #     repoid = imageNode.uuid
        #
        #     image_repo = g.db_session.query(ImageRepository).filter(ImageRepository.uuid == repoid).first()
        #     if image_repo is None:
        #         return request_result(809)
        #
        #     if image_repo.logo == '' or image_repo.logo is None:  # 判断logo 是否为空
        #         print 'image_repo.logo == null'
        #         AutoSetLogo(repositoryname=image_repo.repository)
        #         # return jsonify(AutoSetLogo(repositoryname=image_repo.repository))
        #     else:
        #         print 'logo image_repo.logo != null'
        #         print image_repo.logo
        #         # return jsonify(request_result(0))





