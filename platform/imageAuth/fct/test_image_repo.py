#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 17/2/8 14:53
@ 测试 image_repo
"""

import requests
from imageAuth.manager.userTools import username_password_authentication


# image_repo_prefix = 'https://registrytoken.boxlinker.com:8843'
# image_repo_prefix = 'http://192.168.1.6:8843'
image_repo_prefix = 'https://imageauth.boxlinker.com'
retbool, token = username_password_authentication(username='liutest', password='123456')


verify_crt = '/root/v1.0/registry/ssl/ca.crt'
verify_key = '/root/v1.0/registry/ssl/ca.key'

def test_ImageRepoExist(imagename='boxlinker/storage'):
    """ 镜像名得到镜像id """
    url_suffix = '/api/v1.0/imagerepo/publicimage/?imagename=' + imagename
    url = image_repo_prefix + url_suffix
    headers = {'token': token}
    ret = requests.get(url, headers=headers, timeout=5, cert=(verify_crt, verify_key), verify=True)
    print ret
    print ret.json()
    # {u'msg': u'OK', u'status': 0, u'result': u'646afc75-885e-3f94-b1ee-555e587eeba8'}

def test_ImageRepoRankApi():
    """ 镜像排名 """
    url_suffix = '/api/v1.0/imagerepo/ranks'
    url = image_repo_prefix + url_suffix
    headers = {'token': token}
    ret = requests.get(url, headers=headers, timeout=5, cert=(verify_crt, verify_key), verify=True)
    if 0 != ret.json()['status']:
        print "error"
        print ret.json()['msg']





def test_ImageRepoPublic(page, page_size):
    """ 平台镜像 """
    url_suffix = '/api/v1.0/imagerepo/publicimages/' + str(page) + '/' + str(page_size)
    url = image_repo_prefix + url_suffix
    headers = {'token': token}
    ret = requests.get(url, headers=headers, timeout=5, cert=(verify_crt, verify_key), verify=True)
    print ret.json()

def test_ImageRepoPublic_Search(page, page_size, repo_fuzzy='liuzhangpei'):
    """ 平台镜像搜索 """
    url_suffix = '/api/v1.0/imagerepo/publicimages/' + str(page) + '/' + str(page_size) + '/?repo_fuzzy=' + repo_fuzzy
    url = image_repo_prefix + url_suffix
    headers = {'token': token}
    ret = requests.get(url, headers=headers, timeout=5, cert=(verify_crt, verify_key), verify=True)
    print ret.json()


def test_OwnImageRepo(page, page_size, repo_fuzzy='library%2Fnginx'):
    """ 我的镜像搜索 """
    url_suffix = '/api/v1.0/imagerepo/publicimages/' + str(page) + '/' + str(page_size) + '/?repo_fuzzy=' + repo_fuzzy
    url = image_repo_prefix + url_suffix
    headers = {'token': token}
    ret = requests.get(url, headers=headers, timeout=5, cert=(verify_crt, verify_key), verify=True)
    print ret.json()

def test_OwnImageRepo_Search(page, page_size, repo_fuzzy='library%2Fnginx'):
    """ 我的镜像搜索 """
    url_suffix = '/api/v1.0/imagerepo/ownimages/' + str(page) + '/' + str(page_size) + '/?repo_fuzzy=' + repo_fuzzy
    url = image_repo_prefix + url_suffix
    headers = {'token': token}
    ret = requests.get(url, headers=headers, timeout=5, cert=(verify_crt, verify_key), verify=True)
    print ret.json()

def test_ImageRepo(repoid):
    """ 镜像详情 """
    url_suffix = '/api/v1.0/imagerepo/image/' + repoid
    url = image_repo_prefix + url_suffix
    headers = {'token': token}
    print token
    ret = requests.get(url, headers=headers, timeout=5, cert=(verify_crt, verify_key), verify=True)
    print ret.json()


def test_ImageRepoSystem(repoid):
    """ 镜像详情 """
    url_suffix = '/api/v1.0/imagerepo/image/' + repoid + '/public_info'
    url = image_repo_prefix + url_suffix
    headers = {'token': token}
    ret = requests.get(url, headers=headers, timeout=5, cert=(verify_crt, verify_key), verify=True)
    print ret.json()



def test_ImageTag(tagid):
    """  通过tagid拿到镜像名和版本 """
    url_suffix = '/api/v1.0/imagerepo/image/tagid/' + tagid
    url = image_repo_prefix + url_suffix
    headers = {'token': token}
    ret = requests.get(url, headers=headers, timeout=5, cert=(verify_crt, verify_key), verify=True)
    print ret.json()

def test_Picture():
    """ 镜像名得到镜像id """
    url_suffix = '/api/v1.0/pictures'
    url = image_repo_prefix + url_suffix
    headers = {'token': token}
    data = """{
        "name": "sdsdsd"
        }"""
    ret = requests.post(url, data=data, headers=headers, timeout=5, cert=(verify_crt, verify_key), verify=True)
    print ret
    print ret.json()


def test_ImageRepoDetail(repoid, detail_type):
    """ 修改详情 """
    url_suffix = '/api/v1.0/imagerepo/image/' + repoid + '/detail/' + detail_type
    url = image_repo_prefix + url_suffix

    headers = {'token': token}
    data = """{"detail": "test_ImageRepoDetail modify"}"""

    ret = requests.put(url, data=data, headers=headers, timeout=5, cert=(verify_crt, verify_key), verify=True)
    print ret
    print ret.json()

def test_ImageRepoDetail_publice(repoid, detail_type):
    """ 修改详情,是否公开 """
    url_suffix = '/api/v1.0/imagerepo/image/' + repoid + '/detail/' + detail_type
    url = image_repo_prefix + url_suffix

    headers = {'token': token}
    data = """{"detail": "1"}"""
    ret = requests.put(url, data=data, headers=headers, timeout=5, cert=(verify_crt, verify_key), verify=True)
    print ret
    print ret.json()


if __name__ == '__main__':

    # print 'test_ImageRepoExist'
    # test_ImageRepoExist()
    # print '\n'

    print 'test_ImageRepoRankApi'

    for i in range(1, 10000):
        print i
        test_ImageRepoRankApi()
    print '\n'

    # print 'test_ImageRepoPublic'
    # test_ImageRepoPublic(1, 10)
    # print '\n'
    #
    # print 'test_ImageRepoPublic_Search'
    # test_ImageRepoPublic_Search(1, 10)
    # print '\n'
    #
    # print 'test_OwnImageRepo'
    # test_OwnImageRepo(1, 10)
    # print '\n'
    #
    # print 'test_OwnImageRepo'
    # test_OwnImageRepo_Search(1, 10)
    # print '\n'
    #

    # print 'test_ImageRepo'
    # test_ImageRepo('4c64fc3e-3cef-3b02-8ebf-f63aab009874')
    # print '\n'
    #
    # print 'test_ImageRepoSystem'
    # test_ImageRepoSystem('4bd1ca3f-1752-33e6-b8d0-b9348a58ced7')
    # print '\n'

    # print 'test_ImageRepoDetail'
    # test_ImageRepoDetail('86a3c651-2fe7-3ea1-9e61-fb663f4afafa', 'detail')
    # print '\n'


    # print 'test_ImageRepoDetail'
    # test_ImageRepoDetail_publice('bf1f9123-d5c9-31c5-988a-d417bfb37915', 'is_public')
    # print '\n'



    # print 'test_ImageTag'
    # test_ImageTag('4')
    # print '\n'

    # test_Picture()

    # import uuid
    #
    # image = 'sdsds/sds'
    # repo_uuid = uuid.uuid3(uuid.NAMESPACE_DNS, image).__str__()
    #
    # print type(repo_uuid)
    # print repo_uuid
    #
    #
    # # test_image_repo_public(token='789a495f-2314-44c8-ae5b-be80c1a09c78', page=4, pagesize=4)
    # test_image_repo_public_fuzzy(token='789a495f-2314-44c8-ae5b-be80c1a09c78', page=4, pagesize=4)
