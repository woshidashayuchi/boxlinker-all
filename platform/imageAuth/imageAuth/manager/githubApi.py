#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 17/2/22 14:44
"""

import json

import requests

from common.logs import logging as log


api_url = 'https://api.github.com'


def get_github_user_info(token):
    """ 请求得到用户信息 """
    headers = {
        'authorization': 'token ' + str(token)
    }
    try:
        r = requests.get('https://api.github.com/user', headers=headers, timeout=5)
        return r.status_code, r.json()
    except Exception as msg:
        return 300, msg.message


def get_github_user_some_info(token):
    """ 请求得到用户部分信息 """
    status_code, json_ret = get_github_user_info(token=token)
    if status_code != 200:
        return False, None, None, None

    try:
        git_name = json_ret['login']
        git_uid = json_ret['id']
        git_emain = json_ret['email']
        return True, git_name, git_uid, git_emain
    except Exception, e:
        log.error('get_github_user_some_info is error: %s' % (e))
        return False, None, None, None


def get_token_by_code(code, client_id, client_secret):
    """ 通过授权回调返回的code 码, 得到token """
    headers = {'accept': 'application/json'}

    params = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret
    }

    access_token_url = 'https://github.com/login/oauth/access_token'  # 请求token地址
    try:
        response = requests.post(url=access_token_url, params=params, headers=headers)
        token = response.json()['access_token']
        log.info('get_token_by_code is ok token: %s' % (token))
        return token
    except Exception, e:
        log.info('get_token_by_code is error: %s' % (e))
        return None


def GetGithubRepoList(token, username):
    """ 列出github一个用户的repo列表; 只能是自己的; 别人邀请的不能使用该方法 """
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
        return False, None


def GetGithubRepoListOnlyName(token, username):
    """ 获取一个用户的项目列表; 只含有项目名 """
    retbool, retjson = GetGithubRepoList(token=token, username=username)

    repo_list = []
    if retbool is False:
        return retbool, repo_list

    for reponode in retjson:
        name = reponode['name']
        repo_list.append(name)

    return True, repo_list


def ListHooks(owner, repo, token):
    """ 列出一个项目的web hook"""
    repos_hooks = api_url + '/repos/{0}/{1}/hooks'
    request_url = repos_hooks.format(owner, repo)
    headers = {
        'authorization': 'token ' + str(token),
        'accept': 'application/json'
    }
    print request_url
    try:
        response = requests.get(url=request_url, headers=headers, timeout=4)
        print response
        if response.status_code != 200:
            return False
        log.info('response.json: %s' % (response.json()))
    except Exception, e:
        log.error('ListHooks error: %s' % (e))
        return False


def SetGithubHook(git_name, repo_name, token, payload_url=None, secret=None):
    """
    创建一个web hook
    'https://api.github.com/repos/livenowhy/3des/hooks'
    """
    github_repos_hooks = 'https://api.github.com/repos/{0}/{1}/hooks'
    request_url = github_repos_hooks.format(git_name, repo_name)
    log.info('')
    log.info('SetGithubHook url: %s' % (request_url))

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
    log.info('SetGithubHook response.status_code : %s' % (response.status_code))
    log.info('SetGithubHook response.json : %s' % (response.json()))
    if response.status_code == 401:  # Bad credentials, token 不对
        return False, response.json()
    else:
        return True, response.json()


def DelGithubHooks(git_name, repo_name, token, del_hooks_url):
    """
    删除一个项目下webhook hookurl 满足要求的所有webhook
    'https://api.github.com/repos/livenowhy/3des/hooks'
    """

    repos_hooks = 'https://api.github.com/repos/{0}/{1}/hooks'
    request_url = repos_hooks.format(git_name, repo_name)

    headers = {
        'authorization': 'token ' + str(token),
        'accept': 'application/json'
    }

    try:

        response = requests.get(url=request_url, headers=headers, timeout=4)
        if response.status_code != 200:
            return False
        log.info('response.json: %s' % (response.json()))
    except Exception as msg:
        return False

    ret_bool = True

    for hook in response.json():
        # print hook
        config_url = hook['config']['url']

        if config_url == del_hooks_url:
            web_hook_url = hook['url']
            response_delete = requests.delete(url=web_hook_url, headers=headers, timeout=4)
            if response_delete.status_code == 204:
                log.info('delete hook is ok')
            else:
                ret_bool = False
    return ret_bool



def DelGithubAllWebHooks(username, token, del_hooks_url):
    retbool, repo_list = GetGithubRepoListOnlyName(token=token, username=username)

    if retbool is False:
        return False

    for reponode in  repo_list:
        DelGithubHooks(git_name=username, repo_name=reponode, token=token, del_hooks_url=del_hooks_url)


def GetGithubALLRepoList(token):
    """ 列出github一个用户的repo列表;公开或私有 """
    # /users/:username/repos
    headers = {
        'authorization': 'token ' + str(token),
        'accept': 'application/json'
    }

    log.info('GetGithubALLRepoList token: %s' % (token))
    try:
        request_url = api_url + '/user/repos'
        response = requests.get(url=request_url, headers=headers, timeout=3)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json()
    except Exception, e:
        log.error('GetGithubALLRepoList is error: %s' % (e))
        return False, None


def GetGithubRepoListALLOnlyName(token, username):
    """ 获取一个用户的项目列表; 只含有项目名; 公开或私有 """
    retbool, retjson = GetGithubALLRepoList(token=token, username=username)

    repo_list = []
    if retbool is False:
        return retbool, repo_list

    for reponode in retjson:
        name = reponode['name']
        repo_list.append(name)

    log.info('retjson--->')
    log.info('%s' % (str(retjson)))
    log.info('retjson--->')

    print retjson

    return True, repo_list


if __name__ == '__main__':
    token = 'a810a8c18997ad9825713928e806fb655544aff9'
    token = 'd769b2320e13aa8d86ff1d58738a0aadb17e4298'
    token = 'a810a8c18997ad9825713928e806fb655544aff9'
    token = '70e6209f57cab04bb391f924bdf3f03a48b6d618'
    token = 'ef021819bbc40a844103ffd920f15a164102265f'
    username = 'livenowhy'
    username = 'liuzhangpei'

    token = 'd024c75559dfe99b2f30032c91e014d5423548b1'
    # from authServer.conf.openOauth import OAUTH_WEBHOOKS
    # del_hooks_url = OAUTH_WEBHOOKS

    #retbool, result = GetGithubALLRepoList(token)
    #print result
    # for node in result:
    #     print "---->"
    #     print node
    SetGithubHook(git_name=username, repo_name='3des', token=token)
    #ListHooks(owner=username, repo='3des', token=token)
    # DelGithubAllWebHooks(username=username, token=token, del_hooks_url=del_hooks_url)
