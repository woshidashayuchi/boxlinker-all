#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 17/2/22 14:47
"""
from common.logs import logging as log

import json
import requests

TIMEOUT = 4


deploy_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDBpPkCTBQTRLgSa6SWYctE9JQdbB54thzr3RZ1w9ryYpdyYPFUxSsEWw3fYA81aYQZ3PHO8RrXBFNzgfhgRMoAPhmJaKgAV7QIeiEoNxsLlyxf4vOW+dyAEtEbimzCn20mq9BWT+dGP3B/408CZRV/NIatdqjQNqgxCz8LWsJckqT2g+m7PBU3aRmXPMwEKq9kbCClr70GOIXkEyv2ERcDCDpJnmA/2n1WgDYp7X0HW+QZsPIK8sJj/v0nnlu+JasuRb6e0w4VC9v+SdSD0MPEyyI9YYbGdK9KNhapyy6dVPYI5jhzRKK51bMMZoh/q5Wf2VpbdOXzYsAGW9e/eaYP liuzhangpei@126.com"  # string 公钥内容

webhook_data = {
    'hook_url': None,  # string webhook 链接
    'token': None,  # string 自定义 webhook 秘钥
    'type_push': True,  # boolean push代码 通知开关
    'type_mr_pr': False,  # boolean MR/PR 通知开关
    'type_topic': False,  # boolean 发布讨论 通知开关
    'type_member': False,  # boolean 成员变动 通知开关
    'type_comment': False,  # boolean 发表评论 通知开关
    'type_document': False,  # boolean 文档 通知开关
    'type_watch': False,  # boolean 项目被关注 通知开关
    'type_star': False,  # boolean 项目被加星 通知开关
    'type_task': False,  # boolean 项目任务 通知开关
}

def ApiRequest(url, params=None):
    try:
        # response = requests.get(url=url, timeout=TIMEOUT, kwargs=kwargs)
        response = requests.get(url=url, timeout=TIMEOUT)
        return True, response.content
    except requests.Timeout as msg:
        return False, msg.message
    except Exception as msg:
        return False, msg.message


def ApiRequestPost(url, data=None, json=None):
    try:
        response = requests.post(url=url, data=data, json=json, timeout=TIMEOUT)
        return True, response.content
    except requests.Timeout as msg:
        return False, msg.message
    except Exception as msg:
        return False, msg.message


def ApiRequestPut(url, data=None):
    try:
        response = requests.put(url=url, data=data, timeout=TIMEOUT)
        return True, response.content
    except requests.Timeout as msg:
        return False, msg.message
    except Exception as msg:
        return False, msg.message


def ApiRequestDelete(url):
    try:
        response = requests.delete(url=url, timeout=TIMEOUT)
        return True, response.content
    except requests.Timeout as msg:
        return False, msg.message
    except Exception as msg:
        return False, msg.message

def MakeJson(content):
    resp_json = json.loads(content)

    if 'code' in resp_json and resp_json['code'] == 0:
        return True, resp_json
    else:
        return False, content


def OpenApiGet(url):
    retbool, response = ApiRequest(url=url)

    if retbool is False:
        return False, response

    retbool, user_info = MakeJson(response)
    if retbool is False:
        log.info('OpenApiGet user_info: %s' % (user_info))
        return False, user_info
    return True, user_info


def OpenApiPost(url, data=None, json=None):
    retbool, response = ApiRequestPost(url=url, data=data, json=json)

    if retbool is False:
        return False, response

    retbool, user_info = MakeJson(response)
    if retbool is False:
        log.info('OpenApiGet user_info: %s' % (user_info))
        return False, user_info

    return True, user_info


def OpenApiPut(url, data=None):
    retbool, response = ApiRequestPut(url=url, data=data)

    if retbool is False:
        return False, response

    retbool, user_info = MakeJson(response)
    if retbool is False:
        log.info('OpenApiGet user_info: %s' % (user_info))
        return False, user_info

    return True, user_info


def OpenApiDelete(url):
    retbool, response = ApiRequestDelete(url=url)

    if retbool is False:
        return False, response

    retbool, user_info = MakeJson(response)
    if retbool is False:
        log.info('OpenApiGet user_info: %s' % (user_info))
        return False, user_info

    return True, user_info

def GetUserInfo(access_token):
    """ 获取用户信息 """
    open_url = "https://coding.net/api/current_user?access_token={0}"
    url = open_url.format(access_token)
    retbool, user_info = OpenApiGet(url=url)
    log.info('OpenApiGet user_info: %s' % (user_info))

    return retbool, user_info

def get_coding_user_some_info(access_token):
    status_code, json_ret = GetUserInfo(access_token=access_token)

    if status_code is False:
        return False, None, None, None

    try:
        git_name = json_ret['data']['global_key']
        git_uid = json_ret['data']['id']
        git_emain = ''
        return True, git_name, git_uid, git_emain
    except Exception, e:
        log.error('get_coding_user_some_info is error: %s' % (e))
        return False, None, None, None


def GetRepoList(access_token):
    """ 用户的项目列表 """
    open_url = "https://coding.net/api/user/projects?page=1&pageSize=1000&type=all&access_token={0}"
    # open_url = "https://coding.net/api/user/projects?access_token={0}"

    url = open_url.format(access_token)

    retbool, repo_list = OpenApiGet(url=url)


    return retbool, repo_list

def GetRepoListOnlyName(access_token):
    """ 返回用户的项目列表;只有项目名 """
    retbool, repo_list = GetRepoList(access_token=access_token)
    repolists = []

    if retbool is False:
        return retbool, repolists

    totalRow = repo_list['data']['totalRow']
    if totalRow <= 0:
        return retbool, repolists

    repos = repo_list['data']['list']

    for repo in repos:
        name = repo['name']
        repolists.append(name)
        log.info('GetRepoListOnlyName : %s' % (name))
    return True, repolists




def WebHookList(user_name, project_name, access_token):
    """ webhook 列表 """
    open_url = "https://coding.net/api/user/{user_name}/project/{project_name}/git/hooks?access_token={access_token}"
    url = open_url.format(user_name=user_name, project_name=project_name, access_token=access_token)
    retbool, hooks = OpenApiGet(url=url)
    return retbool, hooks

def WebHookListOnlyHookID(user_name, project_name, access_token):
    """ 获取一个项目的 webhook 的 hook url 和 id;仅仅只有 URL 和 id """
    retbool, hooks = WebHookList(user_name, project_name, access_token)

    if retbool is False:
        return retbool, None

    hooks_data = hooks['data']
    hooks_list = [(hooknode['hook_url'], hooknode['id']) for hooknode in hooks_data]
    return True, hooks_list




def DellAllWebHooksByProjectName(user_name, project_name, access_token, hook_url_del):
    """ 删除一个项目下的所有hook_url为hook_url的webhooks ;"""
    retbool, hooks_list = WebHookListOnlyHookID(user_name=user_name, project_name=project_name, access_token=access_token)

    if retbool:
        for hook_node in hooks_list:
            hook_url, hook_id = hook_node
            if hook_url_del == hook_url:
                log.info('DellAllWebHooks--> hook_id: %s, hook_url: %s' % (hook_id, hook_url))
                WebHookDelete(user_name=user_name, project_name=project_name, hook_id=hook_id, access_token=access_token)



def WebHookAdd(user_name, project_name, access_token, hook_url, hook_token):
    """ 增加 webhook """
    # 官方给出的文档地址不对
    open_url = "https://coding.net/api/user/{user_name}/project/{project_name}/git/hook?access_token={access_token}"
    url = open_url.format(user_name=user_name, project_name=project_name, access_token=access_token)

    data = webhook_data
    data['hook_url'] = hook_url    # string webhook 链接
    data['token'] = hook_token     # string 自定义 webhook 秘钥

    retbool, result = OpenApiPost(url=url, data=data, json=data)
    return retbool, result



def WebHookMsg(user_name, project_name, hook_id, access_token):
    """ 获取 webhook, hook_id 指定hook的id """
    open_url = "https://coding.net/api/user/{user_name}/project/{project_name}/git/hook/{hook_id}?access_token={access_token}"
    url = open_url.format(user_name=user_name, project_name=project_name, hook_id=hook_id, access_token=access_token)
    retbool, repo_list = OpenApiGet(url=url)
    return repo_list



def WebHookModify(user_name, project_name, hook_id, access_token, hook_url, hook_token):
    """ 增加 webhook """
    open_url = "https://coding.net/api/user/{user_name}/project/{project_name}/git/hook/{hook_id}?access_token={access_token}"
    url = open_url.format(user_name=user_name, project_name=project_name, hook_id=hook_id, access_token=access_token)

    data = webhook_data
    data['hook_url'] = hook_url    # string webhook 链接
    data['token'] = hook_token     # string 自定义 webhook 秘钥
    retbool, repo_list = OpenApiPut(url=url, data=data)
    return repo_list


def WebHookDelete(user_name, project_name, hook_id, access_token):
    """ 删除 webhook, hook_id 指定hook的id """

    open_url = "https://coding.net/api/user/{user_name}/project/{project_name}/git/hook/{hook_id}?access_token={access_token}"
    url = open_url.format(user_name=user_name, project_name=project_name, hook_id=hook_id, access_token=access_token)
    retbool, repo_list = OpenApiDelete(url=url)
    return repo_list


def RsaKeyAdd(user_name, project_name, access_token):
    """ 生成部署公钥, 部署之后, 既可以下载私有项目代码 """

    open_url = "https://coding.net/api/user/{user_name}/project/{project_name}/git/deploy_key?access_token={access_token}"
    url = open_url.format(user_name=user_name, project_name=project_name, access_token=access_token)

    data = {
        'title': "webhook-test",  # string 公钥名
        'content': deploy_key   # string 公钥内容
    }

    retbool, result = OpenApiPost(url=url, data=data, json=data)
    return retbool, result


def DellAllWebHooks(user_name, access_token, hook_url_del):
    """ 删除一个用户的所有hook_url为hook_url的webhooks ;"""
    retbool, result = GetRepoListOnlyName(access_token=access_token)
    if retbool is False:
        return retbool, result

    for repo in result:
        retbool, hooks_list = WebHookListOnlyHookID(user_name=user_name, project_name=repo, access_token=access_token)

        if retbool:
            for hook_node in hooks_list:
                hook_url, hook_id = hook_node
                if hook_url_del == hook_url:
                    log.info('DellAllWebHooks--> hook_id: %s, hook_url: %s' % (hook_id, hook_url))
                    WebHookDelete(user_name=user_name, project_name=repo, hook_id=hook_id, access_token=access_token)


def get_token_by_code(client_id, client_secret, code):
    try:
        headers = {'accept': 'application/json'}
        coding_access_token_url = "https://coding.net/api/oauth/access_token?client_id=" + client_id + \
                                  "&client_secret=" + client_secret + "&grant_type=authorization_code&code={0}"

        token_url = coding_access_token_url.format(code)
        response = requests.post(token_url, headers=headers)

        log.info('callback_coding response: %s' % (response.json()))
        # token = response.json()['access_token']

        response_json = response.json()
        if 'access_token' in response_json:
            token = response_json['access_token']
        else:
            log.error('callback_coding is error no get token   token is none')
            return None
        return token
    except Exception, e:
        log.error('callback_coding is error: %s' % (e))
        return None


if __name__ == '__main__':
    DellAllWebHooks(user_name='livenowhy', access_token='281ee4c97e0b4e26b7316e973d84962d', hook_url_del='http://coding.livenowhy.com:8080/api/v2.0/oauths/webhooks')

    #
    # GetUserInfo("3064350b47dc42719de62b28b1e4fcb7")
    # GetRepoList("3064350b47dc42719de62b28b1e4fcb7")
    # # WebHookList("livenowhy", "secret", "3064350b47dc42719de62b28b1e4fcb7")
    #
    # from authServer.conf.openOauth import OAUTH_WEBHOOKS
    # WebHookAdd(user_name="livenowhy", project_name="secret",
    #            access_token="3064350b47dc42719de62b28b1e4fcb7", hook_url=OAUTH_WEBHOOKS, hook_token="sewsws")

    # WebHookMsg(user_name="livenowhy", project_name="secret", hook_id='17092', access_token="3064350b47dc42719de62b28b1e4fcb7")
    #
    # WebHookModify(user_name="livenowhy", project_name="secret", hook_id='17092', access_token="3064350b47dc42719de62b28b1e4fcb7")
    # RsaKeyAdd(user_name="livenowhy", project_name="secret", access_token="3064350b47dc42719de62b28b1e4fcb7")
    # WebHookDelete(user_name="livenowhy", project_name="secret", hook_id='17092', access_token="3064350b47dc42719de62b28b1e4fcb7")
    # print 'sss'