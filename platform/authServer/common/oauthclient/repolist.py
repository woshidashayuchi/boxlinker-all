#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/11/9 15:29
"""


from flask import g

from authServer.models.hub_db_meta import GitHubOauth, CodeRepo
from authServer.pyTools.tools.timeControl import get_now_time
from authServer.pyTools.tools.codeString import request_result


def refresh_repo_list(access_token, git_name, uid, git_uid):
    """ 刷新 github 代码列表 """
    from authServer.common.oauthclient.HubApi import GetGithubRepoList
    retbool, ret_json = GetGithubRepoList(token=access_token, username=git_name)
    if retbool is False:
        return ret_json

    repo_list = list()
    code_repos = list()

    old_repo_name_d = dict()
    old_githubrepo = g.db_session.query(CodeRepo).filter(CodeRepo.uid == str(uid)).all()
    if old_githubrepo is not None:
        for node_repo in old_githubrepo:
            old_repo_name_d[node_repo.repo_id] = node_repo.repo_id

    # print "------------> 01"
    # print ret_json
    # print "------------> 02"
    for node in ret_json:

        repo_id = str(node['id'])
        repo_name = node['name']
        if repo_id in old_repo_name_d:
            g.db_session.query(CodeRepo).filter(CodeRepo.uid == uid, CodeRepo.repo_id == repo_id).update(
                {'repo_name': repo_name,
                 'html_url': node['html_url'],
                 'ssh_url': node['ssh_url'],
                 'url': node['url'],
                 'description': node['description'],
                 }
            )
        else:
            code_repos.append(CodeRepo(
                uid=uid, repo_uid=git_uid, repo_id=repo_id, repo_name=repo_name, update_time=get_now_time(),
                creation_time=get_now_time(), src_type='github', html_url=node['html_url'], ssh_url=node['ssh_url'],
                url=node['url'], description=node['description']
            ))

    g.db_session.add_all(code_repos)
    g.db_session.commit()
    ret = request_result(0, ret=repo_list)
    return ret




from flask import g

from authServer.models.hub_db_meta import GitHubOauth, CodeRepo
from authServer.pyTools.tools.timeControl import get_now_time
from authServer.pyTools.tools.codeString import request_result

# api v3
def refresh_repos(access_token, git_name, uid, git_uid, src_type):
    """ 刷新 github 代码列表 """

    if src_type == 'github':
        from authServer.common.oauthclient.HubApi import GetGithubRepoList, GetGithubALLRepoList
        # # modify liuzhangpei 20170121
        # retbool, ret_json = GetGithubRepoList(token=access_token, username=git_name)
        retbool, ret_json = GetGithubALLRepoList(token=access_token, username=git_name)
        if retbool is False:
            return ret_json
    elif src_type == 'coding':
        from authServer.common.oauthclient.CodingApi import GetRepoList
        code, ret_json = GetRepoList(access_token=access_token)
        if code is False:
            return ret_json
        ret_json = ret_json['data']['list']  # coding 和 github 结构不一样

    repo_list = list()
    code_repos = list()

    old_repo_name_d = dict()
    old_githubrepo = g.db_session.query(CodeRepo).filter(CodeRepo.uid == str(uid), CodeRepo.src_type == src_type).all()
    if old_githubrepo is not None:
        for node_repo in old_githubrepo:
            old_repo_name_d[node_repo.repo_id] = node_repo.repo_id

    # print "------------> 01"
    # print ret_json
    # print "------------> 02"

    # 全部标记已经删除
    g.db_session.query(CodeRepo).filter(
        CodeRepo.uid == uid, CodeRepo.src_type == src_type
    ).update({'deleted': '1',})

    g.db_session.commit()


    # ret_json = ret_json['data']['list']  # coding 和 github 结构不一样
    for node in ret_json:

        # github == coding
        repo_id = str(node['id'])
        description = node['description']
        repo_name = node['name']
        ssh_url = node['ssh_url']
        git_url = node['git_url']


        if src_type == 'github':
            html_url = node['html_url']
        elif src_type == 'coding':
            html_url = node['https_url']

        if repo_id in old_repo_name_d:
            g.db_session.query(CodeRepo).filter(
                CodeRepo.uid == uid, CodeRepo.repo_id == repo_id, CodeRepo.src_type == src_type
            ).update(
                {'repo_name': repo_name,
                 'html_url': html_url,
                 'ssh_url': ssh_url,
                 'url': git_url,
                 'description': description,
                 'deleted': '0',
                 })
        else:
            code_repos.append(CodeRepo(
                uid=uid, repo_uid=git_uid, repo_id=repo_id, repo_name=repo_name, update_time=get_now_time(),
                creation_time=get_now_time(), src_type=src_type, html_url=html_url, ssh_url=ssh_url,
                url=git_url, description=description, deleted='0'
            ))



    g.db_session.add_all(code_repos)
    g.db_session.commit()

    # 真正删除
    try:
        del_repos = g.db_session.query(CodeRepo).filter(CodeRepo.uid == str(uid),
                                                        CodeRepo.src_type == src_type, CodeRepo.deleted == '1').all()

        for del_repo in del_repos:
            g.db_session.delete(del_repo)
            g.db_session.commit()
        print "del is ok"
    except Exception as msg:
        print "del is error"
        print msg.message
        return request_result(100, ret=msg.message)

    return DbGetRepoList(access_token=access_token, git_name=git_name, uid=uid, git_uid=git_uid, src_type=src_type)


def DbGetRepoList(access_token, git_name, uid, git_uid, src_type):
    """ 从数据库中, 获取代码项目 """

    # 用户的 uid, 获取 github_repo 数据   github 项目列表
    ret_github_repo = g.db_session.query(CodeRepo).filter(
        CodeRepo.uid == str(uid),CodeRepo.src_type == src_type).all()

    if ret_github_repo is None or len(ret_github_repo) <= 0:
        # 如果数据不存在，强制刷新(从github请求)
        refresh_repos(access_token, git_name, uid, git_uid, src_type)
        ret_github_repo = g.db_session.query(CodeRepo).filter(
            CodeRepo.uid == str(uid),CodeRepo.src_type == src_type
        ).all()

    repo_list = list()
    for node in ret_github_repo:
        repo_list.append(
            {'repo_name': node.repo_name, 'git_uid': node.repo_uid, 'is_hook': node.is_hook,
             'id': node.id, 'html_url': node.html_url, 'ssh_url': node.ssh_url,
             'url': node.url, 'description': node.description, 'git_name': git_name})

    return request_result(0, ret=repo_list)