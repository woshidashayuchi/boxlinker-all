#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/9/8 下午6:07
"""

import requests
import json
import time

import authServer.conf.conf as TESTCONF



# 测试添加代码构建项目
def test_githubbuild(repo_branch='master', repo_name='webhook_test', images_name='webhook_test_test',
                     dockerfile_path='/docker', dockerfile_name='Dockerfile', auto_build='1', image_tag='auto'):
    urltag = TESTCONF.hostname + '/oauth/githubbuild'
    data = {
        'repo_name': repo_name,
        'repo_branch': repo_branch,   # 分支
        'images_name': images_name,   # 构建镜像的名称
        'dockerfile_path': dockerfile_path,
        'dockerfile_name': dockerfile_name,
        'auto_build': auto_build,
        'image_tag': image_tag  # 镜像标签

    }
    headers = {
        'token': TESTCONF.testtoken
    }


    response = requests.request('POST', url=urltag, data=data, headers=headers)
    print response.json()
    return response.text.decode('utf-8').encode('utf-8')


# 授权平台可以对某个项目具有 hooks 权限
def test_githubhooks(repo_name='test'):
    urltag = TESTCONF.hostname + '/oauth/githubhooks'

    headers = {
        'token': TESTCONF.testtoken,
        'varbox': str(repo_name)
    }

    print headers

    response = requests.request('POST', url=urltag, headers=headers, data=headers)
    print response.json()
    return response.text.decode('utf-8').encode('utf-8')


# 获取用户github项目列表
def test_githubrepo(refresh=False):
    if refresh:
        urltag = TESTCONF.hostname + '/oauth/githubrepo?refresh=true'
    else:
        urltag = TESTCONF.hostname + '/oauth/githubrepo'

    headers = {
        'token': TESTCONF.testtoken
    }

    print headers

    response = requests.request('GET', url=urltag, headers=headers, data=headers)
    print response.json()
    return response.text.decode('utf-8').encode('utf-8')




if __name__ == '__main__':
    # print test_githubrepo()




    headers = {
        'authorization': 'token ' + '87b6d528bcc55f859fd874ca071c12096fd47247'
    }
    r = requests.get('https://api.github.com/user', headers=headers)

    print r.status_code
    print r.json()

    exit(-1)


    print test_githubhooks('webhook_test')

    print test_githubbuild()