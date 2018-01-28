#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/12/6 10:07
"""
import os

from flask_restful import Resource
from flask import jsonify, request
import json

from authServer.pyTools.tools.codeString import request_result


from authServer.common.image.image import CreatePutRetUrl


from authServer.common.decorate import check_headers

@check_headers
def doCreateImage(kwargs=dict()):
    try:
        data = request.data
        data_json = json.loads(data)
    except Exception as msg:
        return request_result(710, ret=msg.message)

    name = data_json.get('name', '').decode('utf-8').encode('utf-8')
    if name == '':
        return request_result(706, 'name is null')

    from authServer.conf.conf import OssHost

    image_dir = CreatePutRetUrl(name)
    if image_dir:
        ret = dict()
        ret['oss_host'] = OssHost
        ret['image_dir'] = image_dir
        ret['image_url'] = OssHost + os.path.sep + image_dir


        return request_result(0, ret=ret)
    else:
        return request_result(100)


class CreateImage(Resource):

    def post(self):
        """
        @apiGroup imageServer
        @apiDescription       生成一个图片并获取在oss中的地址
        @apiVersion 1.0.0
        @apiHeader {String} token 请求接口的token,放在请求头中

        @api {post} /api/v1.0/otherserver/images 生成图片

        @apiExample {post} Example usage:

            {
                "name": "rere"
            }

        @apiParamExample {json} Request-Param-Example:
            {
                "msg": "OK",
                "result":
                {
                    "image_dir": "repository/1480992116391rere.png",
                    "image_url": "http://boxlinker-develop.oss-cn-shanghai.aliyuncs.com/repository/1480992116391rere.png",
                    "oss_host": "http://boxlinker-develop.oss-cn-shanghai.aliyuncs.com"
                },
                "status": 0
            }
            成功时,result返回用户推荐镜像列表

        @apiParam {String} name    需要生成图片的字符
        @apiParam {String} image_dir  图片在oss的相对路径
        @apiParam {String} image_url  绝对路径
        @apiParam {String} oss_host   oss 图片外网访问地址
        """

        # CreatePutRetUrl(sss)

        return jsonify(doCreateImage())