#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/12/1 15:33
"""


from flask_restful import Resource
from authServer.registry.registryToken import get_jwt_token
from authServer.pyTools.docker.registry.docker_registry import *
from authServer.pyTools.tools.codeString import request_result


def getManifests(imagename):

    scopes = 'repository:' + imagename + ':*'

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



class RepoManifests(Resource):
    def put(self):
        print 'ss'

    def get(self, repoid, reference):
        # <string:repoid>/manifests/<string:reference>
        getManifests('liuzhangpei/alpine')

        return request_result(0)