#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/11/24 17:14
"""

import json
import requests
from authServer.pyTools.tools.codeString import request_result

api_url = 'https://api.github.com'

# hook_url = "http://index.boxlinker.com:8080/oauth/webhook"




def GetGithubRepoList(token, username):
    """ 列出github一个用户的repo列表; 只能是自己的 """
    # /users/:username/repos
    headers = {
        'authorization': 'token ' + str(token),
        'accept': 'application/json'
    }
    try:
        request_url = api_url + '/users/{0}/repos'.format(username)
        response = requests.get(url=request_url, headers=headers, timeout=3)

        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json()

    except Exception as msg:
        return False, request_result(100, ret=msg.message)


def GetGithubRepoListOnlyName(token, username):
    """ 获取一个用户的项目列表; 只含有项目名 """
    retbool, retjson = GetGithubRepoList(token=token, username=username)

    repo_list = []
    if retbool is False:
        return retbool, repo_list

    for reponode in retjson:
        print reponode
        name = reponode['name']
        print name
        repo_list.append(name)

    return True, repo_list

# retbool, repo_list



def SetGithubHook(git_name, repo_name, token, payload_url=None, secret=None):
    """
    创建一个web hook
    'https://api.github.com/repos/livenowhy/3des/hooks'
    """

    github_repos_hooks = 'https://api.github.com/repos/{0}/{1}/hooks'
    request_url = github_repos_hooks.format(git_name, repo_name)

    payload = {
        "name": "web",  # 必须是web
        # "url": "http://index.boxlinker.com/oauth/webhook",
        "active": True,
        "events": [
            "push",
            "pull_request"
        ],
        "id": 1,
        "config": {
            "url": "http://auth.boxlinker.com/api/v2.0/oauths/webhoos",
            "content_type": "json",
            "secret": "boxlinker-secret-test"
        }
    }
    headers = {
        'authorization': 'token ' + str(token),
        'accept': 'application/json'
    }

    loc_payload = payload
    if payload_url is not None:
        loc_payload['config']['url'] = payload_url

    if secret is not None:
        loc_payload['config']['secret'] = secret
        loc_payload = json.dumps(loc_payload)

    response = requests.post(url=request_url, headers=headers, data=loc_payload, json=loc_payload)
    print response.status_code
    print response.json()
    if response.status_code == 401:  # Bad credentials, token 不对
        return False, response.json()
    else:
        return True, response.json()


def DelGithubHooks(git_name, repo_name, token, del_hooks_url):
    """
    删除一个项目下webhook hookurl 满足要求的所有webhook
    'https://api.github.com/repos/livenowhy/3des/hooks'
    """

    github_repos_hooks = 'https://api.github.com/repos/{0}/{1}/hooks'
    request_url = github_repos_hooks.format(git_name, repo_name)

    headers = {
        'authorization': 'token ' + str(token),
        'accept': 'application/json'
    }

    try:

        response = requests.get(url=request_url, headers=headers, timeout=4)
        if response.status_code != 200:
            return False
        print response.json()
    except Exception as msg:
        return False

    ret_bool = True

    for hook in response.json():
        # print hook
        config_url = hook['config']['url']
        print config_url

        if config_url == del_hooks_url:
            print hook['url']
            web_hook_url = hook['url']
            response_delete = requests.delete(url=web_hook_url, headers=headers, timeout=4)
            if response_delete.status_code == 204:
                print "delete hook is ok"
            else:
                ret_bool = False

            print response_delete

    return ret_bool



def DelGithubAllWebHooks(username, token, del_hooks_url):
    retbool, repo_list = GetGithubRepoListOnlyName(token=token, username=username)

    if retbool is False:
        return request_result(100)

    for reponode in  repo_list:
        DelGithubHooks(git_name=username, repo_name=reponode, token=token, del_hooks_url=del_hooks_url)




def GetGithubALLRepoList(token, username):
    """ 列出github一个用户的repo列表;公开或私有 """
    # /users/:username/repos
    headers = {
        'authorization': 'token ' + str(token),
        'accept': 'application/json'
    }
    try:
        request_url = api_url + '/user/repos'

        response = requests.get(url=request_url, headers=headers, timeout=3)

        print "begin GetGithubALLRepoList"
        print response.content
        print "end   GetGithubALLRepoList"
        print "begin   GetGithubALLRepoList json"
        print response.json()
        print "end     GetGithubALLRepoList json"

        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json()

    except Exception as msg:
        print msg.message
        print msg.args
        return False, request_result(100, ret=msg.message)




def GetGithubRepoListALLOnlyName(token, username):
    """ 获取一个用户的项目列表; 只含有项目名; 公开或私有 """
    retbool, retjson = GetGithubALLRepoList(token=token, username=username)

    repo_list = []
    if retbool is False:
        return retbool, repo_list

    for reponode in retjson:
        print reponode
        name = reponode['name']
        print name
        repo_list.append(name)

    return True, repo_list


if __name__ == '__main__':
    token = 'a60afed042d84297fde3e9b5e9791727058c33f7'
    token = '7c577c595c594932ec75b93a4f0304b0b1fe9431'
    username = 'liuzhangpei'

    # from authServer.conf.openOauth import OAUTH_WEBHOOKS
    # del_hooks_url = OAUTH_WEBHOOKS

    retbool, result = GetGithubALLRepoList(token, username)
    print result

    for node in result:
        print node
    # DelGithubAllWebHooks(username=username, token=token, del_hooks_url=del_hooks_url)