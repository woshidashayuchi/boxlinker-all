#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/11/10 11:11
"""


from flask import g
from authServer.pyTools.token.token import gen_token, get_payload, make_random_key
import authServer.conf.openOauth as openOauth
from authServer.pyTools.tools.codeString import request_result
from authServer.models.hub_db_meta import CodeRepo



def SetWebHook(git_name, repo_name, access_token, uid, src_type):
    """
    设置一个项目的 web hooks 权限
    :param git_name: github 用户名
    :param var_box:  github 用户项目名
    :param access_token: github token
    :param uid:   平台用户id
    :return:
    """

    random_key = make_random_key()

    from authServer.common.oauthclient.CodingApi import WebHookAdd, RsaKeyAdd
    from authServer.conf.openOauth import OAUTH_WEBHOOKS

    retbool, result = WebHookAdd(
        user_name=git_name, project_name=repo_name,
        access_token=access_token, hook_url=OAUTH_WEBHOOKS, hook_token=random_key)

    if retbool is False:
        return request_result(100, ret=result)


    try:
        g.db_session.query(CodeRepo).filter(CodeRepo.uid == uid,
                                            CodeRepo.repo_name == repo_name,
                                            CodeRepo.src_type == src_type).update(
            {'is_hook': '1', 'repo_hook_token': random_key})
        g.db_session.commit()
        # 设置部署公钥

        retbool, result = RsaKeyAdd(user_name=git_name, project_name=repo_name, access_token=access_token)
        if retbool is False:
            return request_result(100, ret=result)

        return request_result(0)
    except Exception as msg:
        return request_result(403, ret=msg.message)
