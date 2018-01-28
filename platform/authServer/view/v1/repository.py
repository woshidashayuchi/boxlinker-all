#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/10/25 14:13
"""

from flask import Blueprint
from flask_restful import Api

from authServer.v1.repository.RepositoryBuild import RepositoryBuild, RepositoryBuildInstant, MDIF

repository = Blueprint('repository', __name__, url_prefix='/api/v1.0/repository')

api = Api()



api.add_resource(MDIF, '/modifybug')   # 修复bug,临时用

# /api/v1.0/repository/repositorybuilds/<string:repository_uuid>
api.add_resource(RepositoryBuild, '/repositorybuilds/<string:repository_uuid>')   # 修改构建详情


from authServer.v1.repository.repo import RepoFuzzy, DownloadRepo, OwnRepo
# /api/v1.0/repository/repos/<int:page>/<int:page_size>/<string:repo_fuzzy>
# api.add_resource(RepoFuzzy, '/repos/search/<string:repo_fuzzy>')   # 镜像列表模糊查询
# /repos/<int:page>/<int:page_size>  平台镜像
# /repos/<int:page>/<int:page_size>/?repo_fuzzy=library%2Fnginx   镜像列表模糊查询
api.add_resource(RepoFuzzy, '/repos/<int:page>/<int:page_size>', '/repos/<int:page>/<int:page_size>/')

# 我的镜像; 我的镜像  搜索
api.add_resource(OwnRepo, '/user/repos/<int:page>/<int:page_size>', '/user/repos/<int:page>/<int:page_size>/')


#http://auth.boxlinker.com/api/v1.0/repository/ranks/repos
api.add_resource(DownloadRepo, '/ranks/repos')   # 镜像排名


# /repos/<string:repoid>/detail/<string:detail_type>  修改详情
# /repos/<string:repoid>/detail 获取一个镜像的详情
from authServer.v1.repository.repoDetail import RepoDetail
api.add_resource(RepoDetail, '/repos/<string:repoid>/detail/<string:detail_type>', '/repos/<string:repoid>') # 修改镜像详情



# /repos/<string:repoid>/manifests/<string:reference>  镜像 manifests 操作
from authServer.v1.repository.repoManifests import RepoManifests
#
api.add_resource(RepoManifests, '/repos/<string:repoid>/manifests/<string:reference>')

from authServer.v1.repository.repoLogo import RepoLogo
api.add_resource(RepoLogo, '/repos/<string:repoid>/logo')  # 设置镜像图片设置



api.add_resource(RepositoryBuildInstant, '/buildsinstant/<string:repository_uuid>')   # 修改构建详情

api.init_app(repository)
