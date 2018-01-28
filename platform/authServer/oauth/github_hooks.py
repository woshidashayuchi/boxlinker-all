#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/9/8 下午3:19
"""

import requests



# List pull requests
# /repos/:owner/:repo/pulls
def list_pull_requests(token, owner, repo):
    headers = {
        'authorization': 'token ' + str(token),
        'accept': 'application/json'
    }

    p = {
        'state': 'open',
        'base': 'master',
        'head': 'liuzhangpei',
        'sort': 'created',
        'direction': 'desc'
    }

    # /repos/:owner/:repo/pulls
    payload_url = 'https://api.github.com' + '/repos/{0}/{1}/pulls'.format(owner, repo)
    print payload_url

    response = requests.get(url=payload_url, headers=headers, json=p, data=p)

    print response.json
    print response.json()
    return response.status_code, response.json()






def git_repos_to_db(git_name, access_token):
    from authServer.common.oauthclient.HubApi import GetGithubRepoList
    retbool, ret_json = GetGithubRepoList(token=access_token, username=git_name)

    if retbool is False:
        return ret_json

    repo_list = list()

    for node in ret_json:
        repo_name = node['name']
        clone_url = node['clone_url']
        repo_list.append({'repo_name': repo_name, 'clone_url': clone_url})

    print repo_list



