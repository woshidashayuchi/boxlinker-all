#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 17/2/28 10:51
"""

import requests

import sys
import os
from imageAuth.manager.userTools import username_password_authentication

# image_repo_prefix = 'https://registrytoken.boxlinker.com:8843'
image_repo_prefix = 'http://192.168.1.6:8843'
# image_repo_prefix = 'http://localhost:8928'
retbool, token = username_password_authentication(username='boxlinker', password='QAZwsx123')



if retbool is False:
    exit(2)

print token
verify_crt = '/root/v1.0/registry/ssl/ca.crt'
verify_key = '/root/v1.0/registry/ssl/ca.key'

def test_OauthUrl(src_type='github'):
    """ 镜像名得到镜像id """
    url_suffix = '/api/v1.0/oauthclient/url'
    url = image_repo_prefix + url_suffix
    headers = {'token': token}
    data = """{
        "src_type": "$SRCTYPE",
        "redirect_url": "http://test.boxlinker.com/building/create"
        }"""
    data = data.replace('$SRCTYPE', src_type)
    print data
    ret = requests.post(url, data=data, headers=headers, timeout=5, cert=(verify_crt, verify_key), verify=True)
    print ret
    print ret.json()


def test_refresh_OauthCodeRepo(src_type='github'):
    """ 刷新项目列表 """
    url_suffix = '/api/v1.0/oauthclient/repos/' + src_type
    url = image_repo_prefix + url_suffix
    headers = {'token': token}
    ret = requests.put(url, headers=headers, timeout=5, cert=(verify_crt, verify_key), verify=True)
    print ret
    print ret.json()



def test_OauthCodeRepo(src_type='github'):
    """ 重新获取项目列表 """
    url_suffix = '/api/v1.0/oauthclient/repos/' + src_type
    url = image_repo_prefix + url_suffix
    headers = {'token': token}
    ret = requests.get(url, headers=headers, timeout=5, cert=(verify_crt, verify_key), verify=True)
    print ret
    print ret.json()

def test_WebHook(src_type, repo_name):
    url_suffix = '/api/v1.0/oauthclient/webhooks/' + src_type + '/' + repo_name
    url = image_repo_prefix + url_suffix

    headers = {'token': token}
    ret = requests.post(url, headers=headers, timeout=5, cert=(verify_crt, verify_key), verify=True)
    print ret
    print ret.json()


    # /api/v1.0/oauthclient/oauth/<string:src_type>

def test_del(src_type):
    url_suffix = '/api/v1.0/oauthclient/oauth/' + src_type
    url = image_repo_prefix + url_suffix

    headers = {'token': token}
    print url
    ret = requests.delete(url, headers=headers, timeout=20) #, cert=(verify_crt, verify_key), verify=True)
    print ret
    print ret.json()


def test_OauthStatus():
    url_suffix = '/api/v1.0/oauthclient/oauth'
    url = image_repo_prefix + url_suffix

    headers = {'token': token}
    print url
    ret = requests.get(url, headers=headers, timeout=20) #, cert=(verify_crt, verify_key), verify=True)
    print ret
    print ret.json()


if __name__ == '__main__':
    # test_OauthUrl(src_type="github")
    test_OauthCodeRepo(src_type="github")
    # test_refresh_OauthCodeRepo(src_type='github')
    # test_WebHook(src_type='github', repo_name='SmartQQBot')
    # test_del(src_type='coding')
    # test_OauthStatus()


    # eyJzcmNfdHlwZSI6ICJjb2RpbmciLCAiZXhwaXJlcyI6IDE0OTEzOTExOTIuNjQwNDUzLCAic2FsdCI6ICIwLjE5MDc2OTIyMTE0NSIsICJ0ZWFtX3V1aWQiOiAiMmU4ZTdiMzctYTk1Ny00NzcwLTkwNzUtYWFhNjdlYWE0OWNlIiwgInJlZGlyZWN0X3VybCI6ICJodHRwOi8vdGVzdC5ib3hsaW5rZXIuY29tL2J1aWxkaW5nL2NyZWF0ZSJ9YipBFOC7bdFOXrurK2RLKQ==