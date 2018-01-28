#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/12/6 10:05
"""

from flask import Blueprint
from flask_restful import Api

otherserver = Blueprint('otherserver', __name__, url_prefix='/api/v1.0/otherserver')

api = Api()


from authServer.v1.otherServer.imageServer import CreateImage
api.add_resource(CreateImage, '/images')   # 图片服务



api.init_app(otherserver)