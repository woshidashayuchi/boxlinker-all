#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/09/01 19:00
@镜像库相关,路由接口配置
"""

from flask import Blueprint

from flask import request, jsonify
from flask_restful import Api, Resource


from authServer.registry.registryToken import ServerToken, safe_JwtToken
from authServer.registry.image_project import ImageRepositoryHandle
from authServer.registry.notifications import Notifications
from authServer.conf.conf import private_key


from authServer.registry.registry_v2 import Get_Catalog, Get_Tags, V2Images

registry = Blueprint('registry', __name__, url_prefix='/registry')


class Test(Resource):
    def get(self):
        """
        @apiDescription    /registry/* 接口测试
        @apiVersion 1.0.0
        """
        token = safe_JwtToken(account='test', service='test', scope=None, private_key=private_key)
        print 'test --> /registry/* : ' + str(token)
        return {"token": token}


api = Api()
api.add_resource(Test, '/test')

# 镜像库token认证  /registry/token
api.add_resource(ServerToken, '/token')

# notifications 通知接口
api.add_resource(Notifications, '/notifications')

# 镜像库 数据操作 v2.0 get 方法已经全部废弃
api.add_resource(ImageRepositoryHandle, '/image_repository')

# 调用镜像库api获取信息
# 获取镜像库列表
api.add_resource(Get_Catalog, '/v2/catalog')

# 查看镜像详情
api.add_resource(Get_Tags, '/v2/tags', '/')

# 删除镜像
# DELETE /v2/<name>/manifests/<reference>
api.add_resource(V2Images, '/v2/images', '/')
# 调用镜像库api获取信息

api.init_app(registry)

