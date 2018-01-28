#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 17/3/14 13:08
"""

import requests
from imageAuth.manager.userTools import username_password_authentication

# image_repo_prefix = 'https://registrytoken.boxlinker.com:8843'
image_repo_prefix = 'http://101.200.45.76:8765'
# image_repo_prefix = 'http://localhost:8928'
retbool, token = username_password_authentication(username='boxlinker', password='QAZwsx123')



if retbool is False:
    exit(2)

print token
verify_crt = '/root/v1.0/registry/ssl/ca.crt'
verify_key = '/root/v1.0/registry/ssl/ca.key'

def test_get_file():
    """ 镜像名得到镜像id """
    url_suffix = '/api/v1.0/files/team_uuid'
    url = image_repo_prefix + url_suffix
    headers = {'token': token}
    data = """
    {
        "queryparameter" :
            [
                {
                    "team_uuid": "39828489-1bf6-334b-acdb-6a15bbd7c5a3s",
                    "resource_type": "UserAvatars",
                    "resource_uuid": "cabb719f-4a9a-475f-89f1-717231ae7eb5",
                    "resource_domain": "39828489-1bf6-334b-acdb-6a15bbd7c5a3s"
                },
                {
                    "team_uuid": "39828489-1bf6-334b-acdb-6a15bbd7c5a3s",
                    "resource_type": "UserAvatars",
                    "resource_uuid": "cabb719f-4a9a-475f-89f1-717231ae7eb5",
                    "resource_domain": "39828489-1bf6-334b-acdb-6a15bbd7c5a3s"
                }
            ]
    }
    """
    ret = requests.post(url, data=data, headers=headers, timeout=5, cert=(verify_crt, verify_key), verify=True)
    print ret
    print ret.json()


def test_get_file_no_team_uuid():
    """ 镜像名得到镜像id """
    url_suffix = '/api/v1.0/files'
    url = image_repo_prefix + url_suffix
    headers = {'token': token}
    data = """
    {
        "queryparameter" :
            [
                {
                    "resource_type": "UserAvatars",
                    "resource_uuid": "cabb719f-4a9a-475f-89f1-717231ae7eb5",
                    "resource_domain": "39828489-1bf6-334b-acdb-6a15bbd7c5a3s"
                },
                {
                    "resource_type": "UserAvatars",
                    "resource_uuid": "cabb719f-4a9a-475f-89f1-717231ae7eb5",
                    "resource_domain": "39828489-1bf6-334b-acdb-6a15bbd7c5a3s"
                }
            ]
    }
    """
    ret = requests.post(url, data=data, headers=headers, timeout=5, cert=(verify_crt, verify_key), verify=True)
    print ret
    print ret.json()


def GetFileByLocation(team_uuid, resource_type, resource_uuid, resource_domain):
    """ 镜像名得到镜像id """
    url_suffix = '/api/v1.0/files/' + team_uuid + '/' + resource_type + '/' + resource_uuid + '/' + resource_domain
    url = image_repo_prefix + url_suffix
    headers = {'token': token}
    ret = requests.get(url, headers=headers, timeout=5, cert=(verify_crt, verify_key), verify=True)

    if ret.json()['status'] != 0:
        return False

    if len(ret.json()['result']) == 0:
        print len(ret.json()['result'])
        return False
    return True

def GetFileByResource(resource_type, resource_uuid, resource_domain):
    """ 镜像名得到镜像id """
    url_suffix = '/api/v1.0/files/' + '/' + resource_type + '/' + resource_uuid + '/' + resource_domain
    url = image_repo_prefix + url_suffix
    headers = {'token': token}
    ret = requests.get(url, headers=headers, timeout=5, cert=(verify_crt, verify_key), verify=True)
    print ret
    print ret.json()

# /api/v1.0/files/{team_uuid}/{resource_type}/{resource_uuid}/{resource_domain}
def SetFileUrlSave(team_uuid, resource_type, resource_uuid, resource_domain):
    """ 镜像名得到镜像id """
    url_suffix = '/api/v1.0/files/' + team_uuid + '/' + resource_type + '/' + resource_uuid + '/' + resource_domain
    url = image_repo_prefix + url_suffix
    headers = {'token': token}
    data = """
    {
        "file_url": "file_urltest"
    }
    """
    ret = requests.post(url, data=data, headers=headers, timeout=5, cert=(verify_crt, verify_key), verify=True)
    print ret
    print ret.json()


if __name__ == '__main__':
    # test_get_file()
    # test_get_file_no_team_uuid()

    GetFileByLocation(team_uuid='39828489-1bf6-334b-acdb-6a15bbd7c5a3s',
                      resource_type='UserAvatars',
                      resource_uuid='cabb719f-4a9a-475f-89f1-717231ae7eb5',
                      resource_domain='39828489-1bf6-334b-acdb-6a15bbd7c5a3s')

    # GetFileByResource(resource_type='UserAvatars',
    #               resource_uuid='cabb719f-4a9a-475f-89f1-717231ae7eb5',
    #               resource_domain='39828489-1bf6-334b-acdb-6a15bbd7c5a3s')

    # SetFileUrlSave(
    #     team_uuid='39828489-1bf6-334b-acdb-6a15bbd7c5a3s',
    #     resource_type='UserAvatars',
    #     resource_uuid='cabb719f-4a9a-475f-89f1-717231ae7eb5',
    #     resource_domain='39828489-1bf6-334b-acdb-6a15bbd7c5a3s')