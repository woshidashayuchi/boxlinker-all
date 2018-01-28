#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/11/10 10:23
"""

import json

from flask import g, request
from authServer.pyTools.token.token import gen_token, get_payload, make_random_key
import authServer.conf.openOauth as openOauth
from authServer.pyTools.tools.codeString import request_result
from authServer.models.hub_db_meta import CodeRepo

from hashlib import sha1
import hmac

def SetGitHook(git_name, var_box, access_token, uid, del_hooks=False):
    """
    设置一个项目的 web hooks 权限
    :param git_name: github 用户名
    :param var_box:  github 用户项目名
    :param access_token: github token
    :param uid:   平台用户id
    :return:
    """

    if del_hooks:
        from authServer.common.oauthclient.HubApi import DelGithubHooks
        DelGithubHooks(git_name=git_name, repo_name=var_box, token=access_token)

    random_key = make_random_key()

    from authServer.common.oauthclient.HubApi import SetGithubHook

    retbool, response_json = SetGithubHook(
        git_name=git_name, repo_name=var_box, token=access_token, payload_url=None, secret=random_key)
    if retbool is False:
        return request_result(100, ret=response_json)

    try:
        g.db_session.query(CodeRepo).filter(CodeRepo.uid == uid,
                                            CodeRepo.repo_name == var_box).update(
            {'is_hook': '1', 'repo_hook_token': random_key})
        g.db_session.commit()
        ret = request_result(0, ret=response_json)
    except Exception as msg:
        ret = request_result(403, ret=msg.message)
    finally:
        return ret


def GithubWebHookInfo():
    request_headers = dict(request.headers)
    for kk in request_headers:
        print "kk: " + str(kk)
        print "kk: " + str(kk) + "     value: " + str(request_headers[kk])

    x_hub_signature = request_headers['X-Hub-Signature']
    sha_name, signature = x_hub_signature.split('=')
    if sha_name != 'sha1':
        print 'error sha_name type'
        return {'msg': 'error sha_name type'}

    x_github_delivery = request_headers['X-Github-Delivery']
    x_github_event = request_headers['X-Github-Event']

    if x_github_event == 'ping':
        return {'msg': 'pong'}

    if x_github_event != 'push':
        return {'msg': 'no do somethings'}

    try:
        payload = json.loads(request.data)
        print '-----plyload----'
        print type(payload)
        repo_id = payload['repository']['id']  # github中的项目id
        repo_name = payload['repository']['name']
        ssh_url = payload['repository']['ssh_url']
        print payload
    except Exception as msg:
        print msg.message
        return request_result(100, ret=msg.message)

    try:
        code_repo = g.db_session.query(CodeRepo).filter(CodeRepo.repo_id == str(repo_id),
                                                        CodeRepo.src_type == 'github').first()
        if code_repo is None:
            return request_result(405)
        secret = code_repo.repo_hook_token
    except Exception as msg:
        print 'Webhooks   g.db_session.query(GitHubRepo) is error'
        print msg.message
        return request_result(404, ret=msg.message)

    mac = hmac.new(str(secret), msg=request.data, digestmod=sha1).hexdigest()
    if mac != signature:
        print 'mac != signature'
        return {'msg': 'error signature'}
    print 'mac == signature'

    from authServer.oauth.send_build_msg import github_Webhooks
    ret = github_Webhooks(repo_id)
    return ret