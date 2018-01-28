#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/9/2 下午1:41
"""

import json

from flask_restful import Resource
from flask import request, jsonify, g

from authServer.pyTools.docker.registry.docker_registry import *
from authServer.common.decorate import get_token_from_headers

from authServer.models.hub_db_meta import ImageRepository



from authServer.common.usercenter.token import token_authentication

from authServer.registry.registryToken import get_jwt_token

from authServer.pyTools.tools.codeString import request_result



from collections import namedtuple

Scope = namedtuple('Scope', ['type', 'image', 'actions'])


# https://docs.docker.com/registry/spec/api/#listing-image-tags


def _get_catalog(username='boxlinker', password='QAZwsx123'):
    url = 'http://index.boxlinker.com'
    url = 'http://192.168.211.189'


    reg = Registry(url=url,
                   username=username,
                   password=password,
                   verify_ssl=False)

    try:
        #reg.get_tags('ubuntu')
        reg.get_catalog()
        #reg.get_manifest('boxlinker/ubuntu', 'python_05')
    except AuthenticationError:
        print('Authentication error')
        sys.exit(2)



@get_token_from_headers
@token_authentication
def get_catalog(payload):

    #  这里需要判断用户名的权限, 暂时不做控制
    #ret = _get_catalog()

    scopes = 'registry:catalog:*'

    ret = get_jwt_token(account='', service='token-service', scopes=scopes)
    #url = '{0}/v2/{1}'.format(self.url, endpoint)
    #url = 'http://192.168.211.189/v2/_catalog'
    url = 'http://index.boxlinker.com/v2/_catalog'
    auth = BearerAuth(ret['token'])

    # Try to use previous bearer token
    r = requests.get(url, auth=auth, verify=False)
    print url

    # If necessary, try to authenticate and try again
    if r.status_code == 401:
        print '401'
    json = r.json()
    print json
    if r.status_code != 200:
        raise RegistryError.from_json(json)

    ret = request_result(0, ret=json)

    return ret


class Get_Catalog(Resource):
    def get(self):
        """
        @apiDescription 获取镜像库列表
        @apiVersion 1.0.0
        @apiHeader {String} token 请求接口的token,放在请求头中
        @api {get} /registry/v2/catalog
        """
        return jsonify(get_catalog())



@get_token_from_headers
@token_authentication
def get_tags(payload):

    payload = json.loads(payload)
    # isinstance(payload, dict):

    user_name = payload.get('user_name', '')
    imagename = request.args.get('imagename', '').decode('utf-8').encode('utf-8')

    if user_name == '' or imagename == '':
        return request_result(706)

    # 使用user_name 和 imagename 验证  资源分配权限

    # 自动拼接 scopes ,镜像库升级可能导致该值发生改变,到时候需要调整
    scopes = 'repository:{0}:pull'.format(imagename)

    ret = get_jwt_token(account='', service='token-service', scopes=scopes)

    #url = 'http://192.168.211.189/v2/' + imagename + '/tags/list'
    url = 'http://index.boxlinker.com/v2/' + imagename + '/tags/list'

    auth = BearerAuth(ret['token'])

    # Try to use previous bearer token
    r = requests.get(url, auth=auth, verify=False)
    print url

    # If necessary, try to authenticate and try again
    if r.status_code == 401:
        return request_result(205, ret=r.json())
    jsons = r.json()
    print jsons
    if r.status_code != 200:
        return request_result(712, ret=jsons)
        # raise RegistryError.from_json(jsons)

    # 从数据库获取,时间和描述
    try:
        image_project = g.db_session.query(ImageRepository).filter(ImageRepository.repository == imagename,
                                                                   ImageRepository.deleted == '0').first()
        if image_project is not None:
            print type(jsons)
            jsons['repositories'] = image_project.repositories
            jsons['creation_time'] = image_project.creation_time
            jsons['update_time'] = image_project.update_time
            jsons['is_public'] = image_project.is_public

            jsons['short_description'] = image_project.short_description  # 简单描述
            jsons['detail'] = image_project.detail  # 详细描述
            jsons['type'] = image_project.is_code  # 0-->手动推送;   1-->代码构建

            # jsons['auto_build'] = image_project.auto_build  # 是否自动构建
            return request_result(0, ret=jsons)

        return request_result(0, ret=jsons)

    except Exception as msg:
        ret = request_result(602, ret=msg.message)







class Get_Tags(Resource):
    def get(self):
        """
        @apiDescription 获取某个镜像的详情
        @apiVersion 1.0.0
        @apiHeader {String} token 请求接口的token,放在请求头中
        @api {get} /registry/v2/tags?imagename=<imagename>

        @apiExample {curl} Example usage:
        get http://auth.boxlinker.com/registry/v2/tags?imagename=boxlinker/centos-k8sapis
        imagename在url中

        @apiParam {String} imagename  镜像名
        """
        return jsonify(get_tags())


# 删除镜像
def delete_images():
    # http://index.boxlinker.com/v2/
    imagename = 'boxlinker/0928'

    # 自动拼接 scopes ,镜像库升级可能导致该值发生改变,到时候需要调整
    # repository:boxlinker/0928:push,pull
    scopes = 'repository:{0}:push,pull'.format(imagename)
    #scopes = 'repository:{0}:*'.format(imagename)

    scopes = 'repository:boxlinker/0928:*'

    imagename = 'boxlinker/centos-k8sapis'
    scopes = 'repository:boxlinker/centos-k8sapis:*'

    ret = get_jwt_token(account='', service='token-service', scopes=scopes)

    url = 'http://index.boxlinker.com/v2/' + imagename + '/manifests/sha256:d2582b9d0ed619709ba1c55255d3d38e9ec7f013a3204e727ea559cfee43da73'

    auth = BearerAuth(ret['token'])

    # Try to use previous bearer token
    r = requests.delete(url, auth=auth, verify=False)
    print url

    # If necessary, try to authenticate and try again
    if r.status_code == 401:
        print '401'
        return request_result(205, ret=r.json())
    # jsons = r.json()
    # print jsons

    print r.text
    if r.status_code != 200:
        print 'r.status_code'


        #raise RegistryError.from_json(json)


    return "dd"



def get_manifests():

    imagename = 'boxlinker/centos-k8sapis'
    scopes = 'repository:boxlinker/centos-k8sapis:*'

    ret = get_jwt_token(account='', service='token-service', scopes=scopes)

    print ret

    # GET	/v2/<name>/manifests/<reference>

    url = 'http://index.boxlinker.com/v2/' + imagename + '/manifests/1.0'
    auth = BearerAuth(ret['token'])

    # Try to use previous bearer token
    r = requests.get(url, auth=auth, verify=False)

    print r.text

    # If necessary, try to authenticate and try again
    if r.status_code == 401:
        print '401'
        return request_result(205, ret=r.json())
    # jsons = r.json()
    # print jsons

    print r.text
    if r.status_code != 200:
        print 'r.status_code'

    return 'sdsds'

class V2Images(Resource):
    def delete(self):
        # 删除镜像
        return jsonify(delete_images())

    def get(self):
        # 获取 manifest
        return jsonify(get_manifests())



if __name__ == '__main__':
    get_catalog()

